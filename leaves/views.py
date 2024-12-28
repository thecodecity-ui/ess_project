from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from .models import LeaveRequest, LeaveBalance, Notification, ApplyNotification
from authentication.models import Employee
from .serializers import LeaveRequestSerializer, LeaveBalanceSerializer

@api_view(['POST'])
def apply_leave(request):
    start_date = request.data.get('start_date')
    end_date = request.data.get('end_date')
    leave_type = request.data.get('leave_type')
    leave_proof = request.FILES.get('leave_proof')
    reason = request.data.get('reason')
    user = request.data.get('user')
    user_id = request.data.get('user_id')
    email = request.data.get('email')

    try:
        employee = Employee.objects.get(employee_id=user_id)
    except Employee.DoesNotExist:
        return Response({'error': 'Employee not found.'}, status=status.HTTP_404_NOT_FOUND)

    start_date_obj = timezone.datetime.fromisoformat(start_date).date()
    end_date_obj = timezone.datetime.fromisoformat(end_date).date()

    total_days = (end_date_obj - start_date_obj).days + 1
    sundays = sum(1 for i in range(total_days) if (start_date_obj + timedelta(days=i)).weekday() == 6)
    leave_days_used = total_days - sundays

    leave_balance, _ = LeaveBalance.objects.get_or_create(user=user)

    if leave_balance.total_leave_days >= leave_days_used:
        leave_request = LeaveRequest(
            start_date=start_date_obj,
            end_date=end_date_obj,
            leave_type=leave_type,
            reason=reason,
            leave_proof=leave_proof,
            user=user,
            user_id=user_id,
            email=email,
            employee=employee
        )
        leave_request.save()

        leave_balance.total_leave_days -= leave_days_used
        leave_balance.save()

        ApplyNotification.objects.create(
            user=user,
            date=timezone.now().date(),
            time=timezone.localtime(timezone.now()).time(),
            message=f"Leave requested from {start_date} to {end_date}."
        )

        return Response({'message': 'Leave request submitted successfully!'}, status=status.HTTP_201_CREATED)
    else:
        return Response({'error': 'Insufficient leave balance!'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def leave_history(request):
    user = request.query_params.get('user')
    from_date = request.query_params.get('from_date')
    to_date = request.query_params.get('to_date')
    status_filter = request.query_params.get('status')

    filter_args = {}
    if from_date:
        filter_args['start_date__gte'] = from_date
    if to_date:
        filter_args['end_date__lte'] = to_date
    if status_filter:
        filter_args['status'] = status_filter
    if user:
        filter_args['user'] = user

    leave_requests = LeaveRequest.objects.filter(**filter_args).order_by('-start_date')
    serializer = LeaveRequestSerializer(leave_requests, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST', 'GET'])
def employee_leave_status(request):
    if request.method == 'POST':
        leave_id = request.data.get('leave_id')
        status_update = request.data.get('status')

        if status_update not in ['approved', 'rejected']:
            return Response({'error': 'Invalid status.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            leave_request = LeaveRequest.objects.get(id=leave_id)
        except LeaveRequest.DoesNotExist:
            return Response({'error': 'Leave request not found.'}, status=status.HTTP_404_NOT_FOUND)

        if status_update == 'approved':
            total_days = (leave_request.end_date - leave_request.start_date).days + 1
            sundays = sum(1 for i in range(total_days) if (leave_request.start_date + timedelta(days=i)).weekday() == 6)
            leave_days_used = total_days - sundays

            leave_balance, _ = LeaveBalance.objects.get_or_create(user=leave_request.user)

            if leave_request.leave_type == 'medical':
                if leave_balance.medical_leave >= leave_days_used:
                    leave_balance.medical_leave -= leave_days_used
                else:
                    return Response({'error': 'Insufficient medical leave balance.'}, status=status.HTTP_400_BAD_REQUEST)
            elif leave_request.leave_type == 'vacation':
                if leave_balance.vacation_leave >= leave_days_used:
                    leave_balance.vacation_leave -= leave_days_used
                else:
                    return Response({'error': 'Insufficient vacation leave balance.'}, status=status.HTTP_400_BAD_REQUEST)
            elif leave_request.leave_type == 'personal':
                if leave_balance.personal_leave >= leave_days_used:
                    leave_balance.personal_leave -= leave_days_used
                else:
                    return Response({'error': 'Insufficient personal leave balance.'}, status=status.HTTP_400_BAD_REQUEST)

            leave_balance.total_leave_days = max(0, leave_balance.total_leave_days - leave_days_used)
            leave_balance.update_total_absent_days(leave_days_used)
            leave_balance.save()

        leave_request.status = status_update
        leave_request.save()
        
        # Send notification email
        send_leave_notification(
            leave_request.email,
            status.lower(),
            leave_request.leave_type,
            leave_request.start_date,
            leave_request.end_date,
        )
        leave_request.notification_sent = True
        leave_request.save()

        Notification.objects.create(
            user=leave_request.user,
            date=timezone.now().date(),
            time=timezone.localtime(timezone.now()).time(),
            message=f"Your leave request has been {status_update}."
        )

        return Response({'message': f'Leave request has been {status_update}.'}, status=status.HTTP_200_OK)

    elif request.method == 'GET':
        search_user_id = request.query_params.get('search_user_id', '')
        email = request.query_params.get('email', '')
        search_status = request.query_params.get('search_status', '')
        from_date = request.query_params.get('from_date', '')
        to_date = request.query_params.get('to_date', '')

        leave_requests = LeaveRequest.objects.all()
        if search_user_id:
            leave_requests = leave_requests.filter(user_id=search_user_id)
        if search_status:
            leave_requests = leave_requests.filter(status=search_status)
        if email:
            leave_requests = leave_requests.filter(email=email)
        if from_date:
            leave_requests = leave_requests.filter(start_date__gte=from_date)
        if to_date:
            leave_requests = leave_requests.filter(end_date__lte=to_date)

        serializer = LeaveRequestSerializer(leave_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


from django.core.mail import BadHeaderError
from django.core.mail import send_mail

def send_leave_notification(email, status, leave_type, start_date, end_date):
    subject = f"Leave Request {status.capitalize()}"
    message = (
        f"Dear User,\n\n"
        f"Your leave request for {leave_type} from {start_date} to {end_date} has been {status.lower()}.\n\n"
        f"Thank you for your patience.\n\n"
        f"Best regards,\n"
        f"Your Company"
    )
    try:
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,  # Use the DEFAULT_FROM_EMAIL from settings
            [email],
            fail_silently=False,
        )
    except BadHeaderError:
        # Handle bad header errors (e.g., invalid header values)
        print("Invalid header found.")
    except Exception as e:
        # Handle other exceptions (e.g., network issues, server problems)
        print(f"An error occurred: {e}")
        
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import get_object_or_404
from .models import (
    LeaveRequest,
    Manager,
    ManagerLeaveBalance,
    ManagerLeaveRequest,
    ManagerNotification,
    ManagerApplyNotification
)
from django.core.mail import send_mail
from django.conf import settings


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def employee_leave_calendar_view(request):
    local_events = LeaveRequest.objects.filter(status='approved')
    event_data = [
        {
            'id': event.id,
            'title': str(event.user),
            'start': event.start_date.isoformat(),
            'end': event.end_date.isoformat(),
            'description': event.reason
        }
        for event in local_events
    ]
    return Response({'events': event_data}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def manager_apply_leave(request):
    data = request.data
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    leave_type = data.get('leave_type')
    reason = data.get('reason')
    user = request.user

    manager = get_object_or_404(Manager, manager_id=user.id)

    start_date_obj = timezone.datetime.fromisoformat(start_date).date()
    end_date_obj = timezone.datetime.fromisoformat(end_date).date()

    total_days = (end_date_obj - start_date_obj).days + 1
    sundays = sum(1 for i in range(total_days) if (start_date_obj + timedelta(days=i)).weekday() == 6)
    leave_days_used = total_days - sundays

    leave_balance = ManagerLeaveBalance.objects.get_or_create(user=user)[0]

    if leave_balance.total_leave_days >= leave_days_used:
        leave_request = ManagerLeaveRequest.objects.create(
            start_date=start_date_obj,
            end_date=end_date_obj,
            leave_type=leave_type,
            reason=reason,
            user=user,
            manager=manager,
        )
        leave_balance.total_leave_days -= leave_days_used
        leave_balance.save()

        ManagerApplyNotification.objects.create(
            user=user,
            date=timezone.now().date(),
            time=timezone.localtime(timezone.now()).time(),
            message=f"Leave requested from {start_date} to {end_date}."
        )

        return Response({'message': 'Leave request submitted successfully!'}, status=status.HTTP_201_CREATED)
    return Response({'error': 'Insufficient leave balance!'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def manager_leave_history(request):
    user = request.user
    from_date = request.query_params.get('from_date')
    to_date = request.query_params.get('to_date')
    status_filter = request.query_params.get('status')

    filter_args = {'user': user}
    if from_date:
        filter_args['start_date__gte'] = from_date
    if to_date:
        filter_args['end_date__lte'] = to_date
    if status_filter:
        filter_args['status'] = status_filter

    leave_requests = ManagerLeaveRequest.objects.filter(**filter_args).order_by('-start_date')
    leave_data = [
        {
            'id': leave.id,
            'start_date': leave.start_date,
            'end_date': leave.end_date,
            'leave_type': leave.leave_type,
            'status': leave.status,
            'reason': leave.reason,
        }
        for leave in leave_requests
    ]
    return Response(leave_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def manager_leave_calendar_view(request):
    local_events = ManagerLeaveRequest.objects.filter(status='approved')
    event_data = [
        {
            'id': event.id,
            'title': str(event.user),
            'start': event.start_date.isoformat(),
            'end': event.end_date.isoformat(),
            'description': event.reason
        }
        for event in local_events
    ]
    return Response({'events': event_data}, status=status.HTTP_200_OK)


@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def manager_leave_status(request):
    if request.method == 'POST':
        data = request.data
        leave_id = data.get('leave_id')
        status = data.get('status')

        if status not in ['Approved', 'Rejected']:
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

        leave_request = get_object_or_404(ManagerLeaveRequest, id=leave_id)
        leave_request.status = status
        leave_request.save()

        if status == 'Approved':
            leave_balance = ManagerLeaveBalance.objects.get_or_create(user=leave_request.user)[0]
            leave_balance.total_leave_days -= leave_request.total_days
            leave_balance.save()

        send_manager_leave_notification(
            leave_request.email,
            status.lower(),
            leave_request.leave_type,
            leave_request.start_date,
            leave_request.end_date
        )

        ManagerNotification.objects.create(
            user=leave_request.user,
            date=timezone.now().date(),
            time=timezone.localtime(timezone.now()).time(),
            message=f"Your leave request has been {status.lower()}."
        )

        return Response({'message': f'Leave request has been {status.lower()}.'}, status=status.HTTP_200_OK)

    elif request.method == 'GET':
        search_user_id = request.query_params.get('search_user_id')
        email = request.query_params.get('email')
        search_status = request.query_params.get('search_status')
        from_date = request.query_params.get('from_date')
        to_date = request.query_params.get('to_date')

        leave_requests = ManagerLeaveRequest.objects.all()
        if search_user_id:
            leave_requests = leave_requests.filter(user_id=search_user_id)
        if search_status:
            leave_requests = leave_requests.filter(status=search_status)
        if email:
            leave_requests = leave_requests.filter(email=email)
        if from_date:
            leave_requests = leave_requests.filter(start_date__gte=from_date)
        if to_date:
            leave_requests = leave_requests.filter(end_date__lte=to_date)

        leave_data = [
            {
                'id': leave.id,
                'start_date': leave.start_date,
                'end_date': leave.end_date,
                'leave_type': leave.leave_type,
                'status': leave.status,
                'reason': leave.reason,
            }
            for leave in leave_requests
        ]
        return Response(leave_data, status=status.HTTP_200_OK)


# Utility function for sending email
def send_manager_leave_notification(email, status, leave_type, start_date, end_date):
    subject = f"Leave Request {status.capitalize()}"
    message = (
        f"Your leave request for {leave_type} from {start_date} to {end_date} has been {status}.\n"
        "Thank you for your patience.\n\n"
        "Best regards,\n"
        "Your Company"
    )
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import (
    LeaveBalance, ManagerLeaveBalance, Employee, Manager,
    ApplyNotification, ManagerApplyNotification
)


@api_view(['GET'])
def leave_policies(request):
    leave_balances = LeaveBalance.objects.all()
    leave_data = []

    for leave in leave_balances:
        try:
            employee = Employee.objects.get(username=leave.user)
            leave_data.append({
                'user': employee.employee_name,
                'department': employee.department_name,
                'role': employee.role,
                'leave_balance': {
                    'medical_leave': leave.medical_leave,
                    'vacation_leave': leave.vacation_leave,
                    'personal_leave': leave.personal_leave,
                    'total_leave_days': leave.total_leave_days
                }
            })
        except Employee.DoesNotExist:
            continue

    return Response(leave_data, status=status.HTTP_200_OK)


@api_view(['POST'])
def update_leave_balance(request, user):
    try:
        leave_balance = get_object_or_404(LeaveBalance, user=user)
        medical_leave = request.data.get('medical_leave', leave_balance.medical_leave)
        vacation_leave = request.data.get('vacation_leave', leave_balance.vacation_leave)
        personal_leave = request.data.get('personal_leave', leave_balance.personal_leave)

        # Update fields and recalculate total leave days
        leave_balance.medical_leave = int(medical_leave)
        leave_balance.vacation_leave = int(vacation_leave)
        leave_balance.personal_leave = int(personal_leave)
        leave_balance.recalculate_total_leave_days()
        leave_balance.save()

        return Response({'message': f'Leave balance for {user} updated successfully.'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': f'Error updating leave balance for {user}: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def manager_leave_policies(request):
    manager_balances = ManagerLeaveBalance.objects.all()
    leave_data = []

    for leave in manager_balances:
        try:
            manager = Manager.objects.get(username=leave.user)
            leave_data.append({
                'user': manager.manager_name,
                'department': manager.department_name,
                'role': manager.role,
                'leave_balance': {
                    'total_leave_days': leave.total_leave_days
                }
            })
        except Manager.DoesNotExist:
            continue

    return Response(leave_data, status=status.HTTP_200_OK)


@api_view(['POST'])
def update_manager_leave_balance(request, user):
    try:
        leave_balance = get_object_or_404(ManagerLeaveBalance, user=user)
        new_balance = request.data.get('total_leave_days', leave_balance.total_leave_days)

        # Update leave balance
        leave_balance.total_leave_days = int(new_balance)
        leave_balance.save()

        return Response({'message': f'Manager leave balance for {user} updated successfully.'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': f'Error updating manager leave balance for {user}: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def cancel_notification(request, notification_id):
    try:
        notification = get_object_or_404(ApplyNotification, id=notification_id)
        notification.delete()

        return Response({'message': 'Notification has been canceled successfully.'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': f'Error canceling notification: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def admin_cancel_notification(request, notification_id):
    try:
        notification = get_object_or_404(ApplyNotification, id=notification_id)
        notification.delete()

        return Response({'message': 'Admin notification has been canceled successfully.'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': f'Error canceling admin notification: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def manager_cancel_notification(request, notification_id):
    try:
        notification = get_object_or_404(ManagerApplyNotification, id=notification_id)
        notification.delete()

        return Response({'message': 'Manager notification has been canceled successfully.'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': f'Error canceling manager notification: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
        

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from .models import (
    Supervisor, SupervisorLeaveBalance, SupervisorLeaveRequest,
    SupervisorApplyNotification, SupervisorNotification
)
from datetime import timedelta

@api_view(['POST'])
def supervisor_apply_leave(request):
    """
    API to handle supervisor leave application.
    """
    start_date = request.data.get('start_date')
    end_date = request.data.get('end_date')
    leave_type = request.data.get('leave_type')
    reason = request.data.get('reason')
    user = request.data.get('user')
    user_id = request.data.get('user_id')
    email = request.data.get('email')

    supervisor = get_object_or_404(Supervisor, supervisor_id=user_id)

    start_date_obj = timezone.datetime.fromisoformat(start_date).date()
    end_date_obj = timezone.datetime.fromisoformat(end_date).date()

    total_days = (end_date_obj - start_date_obj).days + 1
    sundays = sum(1 for i in range(total_days) if (start_date_obj + timedelta(days=i)).weekday() == 6)
    leave_days_used = total_days - sundays

    leave_balance, _ = SupervisorLeaveBalance.objects.get_or_create(user=user)

    if leave_balance.total_leave_days >= leave_days_used:
        SupervisorLeaveRequest.objects.create(
            start_date=start_date_obj,
            end_date=end_date_obj,
            leave_type=leave_type,
            reason=reason,
            user=user,
            user_id=user_id,
            email=email,
            supervisor=supervisor
        )
        leave_balance.total_leave_days -= leave_days_used
        leave_balance.save()

        SupervisorApplyNotification.objects.create(
            user=user,
            date=timezone.now().date(),
            time=timezone.localtime(timezone.now()).time(),
            message=f"Leave requested from {start_date} to {end_date}."
        )
        return Response({"message": "Leave request submitted successfully!"}, status=status.HTTP_201_CREATED)
    else:
        return Response({"error": "Insufficient leave balance!"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def supervisor_leave_history(request):
    """
    API to fetch supervisor leave history with optional filters.
    """
    user = request.query_params.get('user')
    from_date = request.query_params.get('from_date')
    to_date = request.query_params.get('to_date')
    status_filter = request.query_params.get('status')

    filters = {}
    if user:
        filters['user'] = user
    if from_date:
        filters['start_date__gte'] = from_date
    if to_date:
        filters['end_date__lte'] = to_date
    if status_filter:
        filters['status'] = status_filter

    leave_requests = SupervisorLeaveRequest.objects.filter(**filters).order_by('-start_date')

    leave_data = [
        {
            'id': req.id,
            'user': req.user,
            'start_date': req.start_date,
            'end_date': req.end_date,
            'leave_type': req.leave_type,
            'reason': req.reason,
            'status': req.status,
        }
        for req in leave_requests
    ]

    return Response(leave_data, status=status.HTTP_200_OK)


@api_view(['GET'])
def supervisor_leave_calendar_view(request):
    """
    API to fetch approved leave requests for calendar view.
    """
    approved_leaves = SupervisorLeaveRequest.objects.filter(status='approved')
    events = [
        {
            'id': leave.id,
            'title': f"{leave.user}",
            'start': leave.start_date.isoformat(),
            'end': leave.end_date.isoformat(),
            'description': leave.reason
        }
        for leave in approved_leaves
    ]

    return Response(events, status=status.HTTP_200_OK)


@api_view(['POST'])
def supervisor_leave_status(request):
    """
    API to update leave request status (Approve/Reject).
    """
    leave_id = request.data.get('leave_id')
    status_update = request.data.get('status')

    if status_update not in ['Approved', 'Rejected']:
        return Response({"error": "Invalid status."}, status=status.HTTP_400_BAD_REQUEST)

    leave_request = get_object_or_404(SupervisorLeaveRequest, id=leave_id)

    if status_update == 'Approved':
        leave_balance, _ = SupervisorLeaveBalance.objects.get_or_create(user=leave_request.user)
        leave_balance.total_leave_days -= leave_request.total_days
        leave_balance.save()

    leave_request.status = status_update
    leave_request.save()

    try:
        send_supervisor_leave_notification(
            leave_request.email,
            status_update.lower(),
            leave_request.leave_type,
            leave_request.start_date,
            leave_request.end_date
        )

        SupervisorNotification.objects.create(
            user=leave_request.user,
            date=timezone.now().date(),
            time=timezone.localtime(timezone.now()).time(),
            message=f"Your leave request has been {status_update.lower()}."
        )

        return Response({"message": f"Leave request {status_update.lower()} successfully and notification sent."}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": f"Failed to send notification: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def send_supervisor_leave_notification(email, status, leave_type, start_date, end_date):
    """
    Helper function to send notification email for leave requests.
    """
    subject = f"Leave Request {status.capitalize()}"
    message = (
        f"Your leave request for {leave_type} from {start_date} to {end_date} has been {status.lower()}.\n"
        "Thank you for your patience.\n\n"
        "Best regards,\n"
        "Your Company"
    )
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import SupervisorLeaveBalance, Supervisor, SupervisorApplyNotification

@api_view(['GET'])
def supervisor_leave_policies(request):
    """
    Retrieve leave balances for supervisors.
    """
    supervisor_balances = SupervisorLeaveBalance.objects.all()
    leave_data = []

    for leave in supervisor_balances:
        try:
            supervisor = Supervisor.objects.get(username=leave.user)
            leave_data.append({
                'user': supervisor.supervisor_name,
                'department': supervisor.department_name,
                'role': supervisor.role,
                'leave_balance': {
                    'total_leave_days': leave.total_leave_days,
                    'medical_leave': leave.medical_leave,
                    'vacation_leave': leave.vacation_leave,
                    'personal_leave': leave.personal_leave
                },
                'is_supervisor': True
            })
        except Supervisor.DoesNotExist:
            continue

    return Response({'leave_data': leave_data}, status=status.HTTP_200_OK)

@api_view(['POST'])
def update_supervisor_leave_balance(request, user):
    """
    Update the leave balance for a specific supervisor.
    """
    new_balance = request.data.get('leave_balance')

    if not new_balance:
        return Response({'error': 'Leave balance is required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        leave_balance = get_object_or_404(SupervisorLeaveBalance, user=user)
        leave_balance.total_leave_days = new_balance
        leave_balance.save()
        return Response({'message': f'Supervisor leave balance for {user} updated successfully.'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': f'Error updating supervisor leave balance for {user}: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def supervisor_cancel_notification(request, notification_id):
    """
    Cancel a supervisor's leave notification.
    """
    try:
        notification = get_object_or_404(SupervisorApplyNotification, id=notification_id)
        notification.delete()
        return Response({'message': 'Notification has been canceled successfully.'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': f'Error canceling notification: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
