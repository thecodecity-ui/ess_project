from calendar import monthrange
from django.forms import ValidationError
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import timedelta
from .models import Attendance
from rest_framework import status
from rest_framework.views import APIView
from .serializers import AttendanceCheckoutSerializer, EmployeeMonthlyChartSerializer, ManagerWeeklyAttendanceSerializer, ResetRequestApprovalSerializer, ResetRequestRejectionSerializer, ShiftSerializer, LocationSerializer, AttendanceSerializer, SupervisorAttendanceSerializer, SupervisorCheckoutTimeSerializer, SupervisorMonthlyAttendanceChartSerializer, SupervisorWeeklyAttendanceChartSerializer, WeeklyAttendanceSerializer
from datetime import date
from django.contrib.sessions.models import Session
from .serializers import AttendanceHistorySerializer

from datetime import datetime
from .models import Employee, ResetRequest
from .serializers import ResetRequestSerializer
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from rest_framework.exceptions import ValidationError
from rest_framework.exceptions import NotFound
from django.shortcuts import render
from .serializers import AttendanceSerializer
from rest_framework.response import Response
from .models import Attendance
from .serializers import WeeklyAttendanceSerializer
from .models import Attendance
from .serializers import ManagerWeeklyAttendanceSerializer
from .serializers import AttendanceSerializer

from django.shortcuts import render
from .models import Attendance  
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Attendance
from .serializers import MonthlyAttendanceChartSerializer, AttendanceSerializer
from rest_framework.views import APIView
from rest_framework import status
from .serializers import EmployeeMonthlyChartSerializer
from .serializers import SupervisorAttendanceSerializer
from .models import Location, Supervisor, Shift, Attendance
from rest_framework.exceptions import NotFound
from rest_framework import status
from .serializers import SupervisorAttendanceStatusSerializer

from .serializers import AttendanceSerializer
from rest_framework.views import APIView
from .models import Supervisor, Attendance, ResetRequest
from .models import ResetRequest, Attendance
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from .serializers import ResetRequestApprovalSerializer
from .serializers import ResetRequestRejectionSerializer
from .models import Attendance, Shift
from .serializers import SupervisorCheckoutTimeSerializer
from datetime import datetime, timedelta
from .serializers import ResetRequestSerializer
from .serializers import ResetRequestApprovalSerializer
from .serializers import ResetRequestRejectionSerializer

from .serializers import SupervisorWeeklyAttendanceChartSerializer
from calendar import monthrange
from .serializers import SupervisorMonthlyAttendanceChartSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta
from calendar import monthrange
from leaves.models import  LeaveRequest, SupervisorLeaveRequest, ManagerLeaveRequest
from .serializers import EmployeeMonthlyChartSerializer, EmployeeWeeklyChartSerializer, SupervisorMonthlyChartSerializer, ManagerMonthlyChartSerializer, SupervisorWeeklyChartSerializer, ManagerWeeklyChartSerializer, AttendanceSerializer, ResetRequestSerializer, WeeklyChartDataSerializer, ManagerAttendanceSerializer, AdminManagerWeeklyChartSerializer, EmployeeAttendanceSerializer, SupervisorAttendanceSerializer
from rest_framework.decorators import api_view
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q







@api_view(['GET'])
def calculate_total_present_days(request, employee_id):
    """
    API to calculate total present days for an employee based on total working hours.

    :param employee_id: ID of the employee (passed in the URL)
    :return: JSON response with total present days
    """
    try:
        # Fetch all attendance records for the employee
        attendance_records = Attendance.objects.filter(employee_id=employee_id).exclude(total_working_hours=None)

        # Sum up the total working hours across all records
        total_seconds = sum(
            int(timedelta(
                hours=int(hours.split(':')[0]),
                minutes=int(hours.split(':')[1]),
                seconds=int(hours.split(':')[2])
            ).total_seconds()) for hours in attendance_records.values_list('total_working_hours', flat=True)
        )

        # Convert total seconds to hours
        total_hours = total_seconds / 3600

        # Calculate present days (8 hours = 1 day)
        present_days = total_hours / 8

        # Round and return as JSON
        return Response({"employee_id": employee_id, "total_present_days": round(present_days, 2)})
    
    except Attendance.DoesNotExist:
        return Response({"error": "No attendance records found for the given employee."}, status=404)
    except Exception as e:
        return Response({"error": str(e)}, status=500)



@api_view(['GET'])
def employee_attendance_form_api(request):
    """
    API to retrieve data for the employee attendance form.

    :param request: HTTP request object
    :return: JSON response with locations, shift, and attendance details
    """
    # Retrieve user ID from session
    user_id = request.session.get('user_id')
    if not user_id:
        return Response({"error": "User is not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        # Fetch employee details
        employee = Employee.objects.get(employee_id=user_id)
        assigned_shift = employee.shift
        shift = Shift.objects.get(shift_number=assigned_shift.shift_number)

        # Fetch locations
        locations = Location.objects.all()

        # Get today's date
        today = datetime.now().strftime('%Y-%m-%d')

        # Retrieve today's attendance record
        last_attendance = Attendance.objects.filter(
            employee=employee,
            date=today
        ).first()

        # Determine checkout and message status
        show_checkout = False
        thank_you_message = ""
        error_message = ""

        if last_attendance and last_attendance.time_out is None:
            show_checkout = True
            thank_you_message = "Thanks for today"
        elif last_attendance and last_attendance.time_out is not None:
            error_message = "You have already checked out for today. Please try again tomorrow."

        # Prepare response data
        response_data = {
            "locations": [{"id": loc.id, "name": loc.name} for loc in locations],
            "shift": {
                "shift_number": shift.shift_number,
                "start_time": shift.start_time.strftime('%H:%M:%S'),
                "end_time": shift.end_time.strftime('%H:%M:%S')
            },
            "attendance_status": {
                "show_checkout": show_checkout,
                "thank_you_message": thank_you_message,
                "error_message": error_message
            }
        }

        return Response(response_data, status=status.HTTP_200_OK)

    except Employee.DoesNotExist:
        return Response({"error": "Employee not found."}, status=status.HTTP_404_NOT_FOUND)
    except Shift.DoesNotExist:
        return Response({"error": "Shift not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




@api_view(['POST'])
def submit_employee_attendance_api(request):
    """
    API endpoint for submitting employee attendance (check-in/check-out).
    """
    user_id = request.session.get('user_id')
    if not user_id:
        return Response({"error": "User not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

    # Restrict check-in on Sundays
    if datetime.now().weekday() == 6:
        return Response({"error": "Check-in is not allowed on Sundays."}, status=status.HTTP_400_BAD_REQUEST)

    # Check leave status
    try:
        leave_request = LeaveRequest.objects.filter(
            employee__employee_id=user_id,
            status='Approved'
        ).latest('start_date')

        current_date = datetime.now().date()
        if leave_request.start_date <= current_date <= leave_request.end_date:
            return Response({"error": "You are on leave. Please check in after your leave ends."}, status=status.HTTP_400_BAD_REQUEST)
    except LeaveRequest.DoesNotExist:
        pass  # No leave request found, continue

    # Check-in process
    action = request.data.get('action')  # Either 'check_in' or 'check_out'
    if action == 'check_in':
        shift_number = request.data.get('shift')
        location_name = request.data.get('location')
        notes = request.data.get('notes', '')
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')

        try:
            shift = Shift.objects.get(shift_number=shift_number)
            location = Location.objects.get(location_name=location_name)
            employee = Employee.objects.get(employee_id=user_id)
        except (Shift.DoesNotExist, Location.DoesNotExist, Employee.DoesNotExist):
            return Response({"error": "Shift, location, or employee not found."}, status=status.HTTP_404_NOT_FOUND)

        shift_start_time = shift.shift_start_time
        shift_end_time = shift.shift_end_time
        current_time = datetime.now().time()

        if current_time > shift_end_time:
            return Response({"error": "You cannot check in after the shift end time."}, status=status.HTTP_400_BAD_REQUEST)

        today = datetime.now().strftime('%Y-%m-%d')
        if Attendance.objects.filter(employee=employee, date=today).exists():
            return Response({"error": "You have already checked in for today."}, status=status.HTTP_400_BAD_REQUEST)

        # Determine check-in status
        shift_start_datetime = datetime.combine(datetime.today(), shift_start_time)
        early_threshold = shift_start_datetime - timedelta(minutes=10)
        late_threshold = shift_start_datetime + timedelta(minutes=10)
        current_datetime = datetime.combine(datetime.today(), current_time)

        if early_threshold <= current_datetime <= late_threshold:
            in_status = 'On time'
        elif current_datetime < early_threshold:
            in_status = 'Early'
        else:
            in_status = 'Late'

        time_in = datetime.now().strftime('%H:%M:%S')
        Attendance.objects.create(
            date=today,
            shift=shift,
            location=location,
            notes=notes,
            time_in=time_in,
            time_out=None,
            in_status=in_status,
            out_status=None,
            overtime=None,
            total_working_hours=None,
            latitude=latitude,
            longitude=longitude,
            employee=employee,
        )
        return Response({"success": "Checked in successfully.", "status": in_status}, status=status.HTTP_200_OK)

    elif action == 'check_out':
        today = datetime.now().strftime('%Y-%m-%d')
        current_time = datetime.now().time()
        time_out = datetime.now().strftime('%H:%M:%S')

        try:
            last_attendance = Attendance.objects.get(
                employee__employee_id=user_id,
                date=today,
                time_out__isnull=True
            )
            shift = last_attendance.shift
        except Attendance.DoesNotExist:
            return Response({"error": "No check-in found for today."}, status=status.HTTP_400_BAD_REQUEST)

        shift_end_time = shift.shift_end_time
        overtime_start_time = (datetime.combine(datetime.today(), shift_end_time) + timedelta(minutes=10)).time()

        if current_time < shift_end_time:
            out_status = 'Early'
            overtime_str = '00:00:00'
        elif shift_end_time <= current_time <= overtime_start_time:
            out_status = 'On time'
            overtime_str = '00:00:00'
            time_out = shift_end_time.strftime('%H:%M:%S')
        else:
            out_status = 'Overtime'
            overtime = datetime.combine(datetime.today(), current_time) - datetime.combine(datetime.today(), overtime_start_time)
            overtime_str = str(overtime)

        time_in = datetime.strptime(last_attendance.time_in, '%H:%M:%S').time()
        total_working_time = datetime.combine(datetime.today(), current_time) - datetime.combine(datetime.today(), time_in)
        total_working_hours = str(total_working_time)

        # Update attendance record
        last_attendance.time_out = time_out
        last_attendance.out_status = out_status
        last_attendance.overtime = overtime_str
        last_attendance.total_working_hours = total_working_hours
        last_attendance.save()

        return Response({"success": "Checked out successfully.", "status": out_status, "total_working_hours": total_working_hours}, status=status.HTTP_200_OK)

    return Response({"error": "Invalid action."}, status=status.HTTP_400_BAD_REQUEST)


# views.py


class EmployeeAttendanceHistoryAPIView(APIView):
    def get(self, request):
        user_id = request.session.get('user_id')  # Assuming employee ID is stored in the session

        if not user_id:
            return Response({'error': 'User not logged in.'}, status=status.HTTP_400_BAD_REQUEST)

        # Get the date range from the request
        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')

        # Initialize the query to fetch all attendance records for the logged-in employee
        query = Attendance.objects.filter(employee__employee_id=user_id)

        if from_date and to_date:
            try:
                # Parse the from_date and to_date
                from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
                to_date = datetime.strptime(to_date, '%Y-%m-%d').date()

                if from_date > to_date:
                    return Response({'error': 'From date cannot be after to date.'}, status=status.HTTP_400_BAD_REQUEST)

                # Filter the records based on the date range
                query = query.filter(date__range=[from_date, to_date])

            except ValueError:
                return Response({'error': 'Invalid date format. Please use YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch the filtered (or unfiltered) records
        attendance_records = query.select_related('shift', 'location')

        if attendance_records.exists():
            serializer = AttendanceHistorySerializer(attendance_records, many=True)
            return Response(serializer.data)
        else:
            return Response({'message': 'No attendance records found for the selected dates.'}, status=status.HTTP_404_NOT_FOUND)



class ManagerAttendanceFormAPI(APIView):
    def get(self, request):
        user_id = request.session.get('user_id')  # Assuming manager ID is stored in session

        if not user_id:
            return Response({'error': 'User not logged in.'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            manager = Manager.objects.get(manager_id=user_id)
            assigned_shift = manager.shift
            shift = Shift.objects.get(shift_number=assigned_shift.shift_number)
        except Manager.DoesNotExist:
            return Response({'error': 'Manager not found. Please contact support.'}, status=status.HTTP_404_NOT_FOUND)
        except Shift.DoesNotExist:
            return Response({'error': 'Assigned shift not found. Please contact HR.'}, status=status.HTTP_404_NOT_FOUND)

        today = date.today()

        # Check if attendance exists for today
        last_attendance = Attendance.objects.filter(manager=manager, date=today).first()

        # Prepare response data
        response_data = {
            'locations': LocationSerializer(Location.objects.all(), many=True).data,
            'shift': ShiftSerializer(shift).data,
            'show_checkout': False,
            'thank_you_message': '',
        }

        if last_attendance:
            if last_attendance.time_out is None:
                response_data['show_checkout'] = True
                response_data['thank_you_message'] = 'Thanks for today!'
            else:
                return Response({'message': 'You have already checked out for today. Please try again tomorrow.'}, status=status.HTTP_200_OK)
        else:
            response_data['thank_you_message'] = 'Welcome! Please check in.'

        return Response(response_data, status=status.HTTP_200_OK)

# 
# views.py


class SubmitManagerAttendanceAPI(APIView):
    def post(self, request):
        user_id = request.session.get('user_id')  # Assuming manager ID is stored in session

        # Restrict check-in on Sundays
        if datetime.now().weekday() == 6:
            return Response({'error': 'Check-in is not allowed on Sundays.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check for leave status
        try:
            leave_request = ManagerLeaveRequest.objects.filter(manager__manager_id=user_id, status='Approved').latest('start_date')
            current_date = datetime.now().date()
            if leave_request.start_date <= current_date <= leave_request.end_date:
                return Response({'error': 'You are on leave. Please check in after your leave ends.'}, status=status.HTTP_400_BAD_REQUEST)
        except ManagerLeaveRequest.DoesNotExist:
            # No leave request found, proceed with attendance check
            pass

        if 'check_in' in request.data:
            shift_number = request.data.get('shift')
            location_name = request.data.get('location')
            notes = request.data.get('notes')

            try:
                shift = Shift.objects.get(shift_number=shift_number)
                location = Location.objects.get(location_name=location_name)
                manager = Manager.objects.get(manager_id=user_id)
            except (Shift.DoesNotExist, Location.DoesNotExist, Manager.DoesNotExist):
                return Response({'error': 'Shift, location, or manager not found.'}, status=status.HTTP_404_NOT_FOUND)

            shift_start_time = shift.shift_start_time
            shift_end_time = shift.shift_end_time
            current_time = datetime.now().time()

            if current_time > shift_end_time:
                return Response({'error': 'You cannot check in after the shift end time.'}, status=status.HTTP_400_BAD_REQUEST)

            today = datetime.now().strftime('%Y-%m-%d')
            existing_attendance = Attendance.objects.filter(manager=manager, date=today).first()

            if existing_attendance:
                return Response({'error': 'You have already checked in for today.'}, status=status.HTTP_400_BAD_REQUEST)

            shift_start_datetime = datetime.combine(datetime.today(), shift_start_time)
            early_threshold = shift_start_datetime - timedelta(minutes=10)
            late_threshold = shift_start_datetime + timedelta(minutes=10)
            current_datetime = datetime.combine(datetime.today(), current_time)

            if early_threshold <= current_datetime <= late_threshold:
                in_status = 'On time'
                time_in = shift_start_time.strftime('%H:%M:%S')
            elif current_datetime < early_threshold:
                in_status = 'Early'
                time_in = shift_start_time.strftime('%H:%M:%S')
            else:
                in_status = 'Late'
                time_in = current_datetime.strftime('%H:%M:%S')

            attendance = Attendance.objects.create(
                date=today,
                shift=shift,
                location=location,
                notes=notes,
                time_in=time_in,
                time_out=None,
                in_status=in_status,
                out_status=None,
                overtime=None,
                total_working_hours=None,
                manager=manager,
            )

            return Response({'message': 'Checked in successfully.'}, status=status.HTTP_200_OK)

        elif 'check_out' in request.data:
            current_time = datetime.now().time()
            today = datetime.now().strftime('%Y-%m-%d')
            time_out = datetime.now().strftime('%H:%M:%S')

            try:
                last_attendance = Attendance.objects.get(manager__manager_id=user_id, date=today, time_out=None)
                shift = last_attendance.shift
            except Attendance.DoesNotExist:
                return Response({'error': 'No check-in found for today.'}, status=status.HTTP_400_BAD_REQUEST)

            shift_end_time = shift.shift_end_time
            overtime_start_time = (datetime.combine(datetime.today(), shift_end_time) + timedelta(minutes=10)).time()

            if current_time < shift_end_time:
                out_status = 'Early'
                overtime_str = '00:00:00'
            elif shift_end_time <= current_time <= overtime_start_time:
                out_status = 'On time'
                overtime_str = '00:00:00'
                time_out = shift_end_time
            else:
                out_status = 'Overtime'
                overtime = datetime.combine(datetime.today(), current_time) - datetime.combine(datetime.today(), overtime_start_time)
                overtime_hours = overtime.seconds // 3600
                overtime_minutes = (overtime.seconds % 3600) // 60
                overtime_seconds = overtime.seconds % 60
                overtime_str = f"{overtime_hours:02}:{overtime_minutes:02}:{overtime_seconds:02}"

            time_in = last_attendance.time_in
            total_working_time = datetime.combine(datetime.today(), current_time) - datetime.combine(datetime.today(), time_in)
            total_hours = total_working_time.seconds // 3600
            total_minutes = (total_working_time.seconds % 3600) // 60
            total_seconds = total_working_time.seconds % 60
            total_working_hours = f"{total_hours:02}:{total_minutes:02}:{total_seconds:02}"

            last_attendance.time_out = time_out
            last_attendance.out_status = out_status
            last_attendance.overtime = overtime_str
            last_attendance.total_working_hours = total_working_hours
            last_attendance.save()

            return Response({'message': f'Checked out successfully. Status: {out_status}'}, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid action. Use check_in or check_out.'}, status=status.HTTP_400_BAD_REQUEST)





class ManagerAttendanceHistory(APIView):
    def get(self, request, format=None):
        user_id = request.session.get('user_id')  # Assuming manager ID is stored in session

        if not user_id:
            return Response({"detail": "User not logged in."}, status=status.HTTP_401_UNAUTHORIZED)

        # Get the date range from the request
        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')

        # Initialize the query to fetch all attendance records for the logged-in manager
        query = Attendance.objects.filter(manager__manager_id=user_id)

        if from_date and to_date:
            try:
                # Parse the from_date and to_date
                from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
                to_date = datetime.strptime(to_date, '%Y-%m-%d').date()

                if from_date > to_date:
                    return Response({"detail": "From date cannot be after to date."}, status=status.HTTP_400_BAD_REQUEST)

                # Filter the records based on the date range
                query = query.filter(date__range=[from_date, to_date])

            except ValueError:
                return Response({"detail": "Invalid date format. Please use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch the filtered records
        attendance_records = query.select_related('shift', 'location')

        if not attendance_records.exists():
            return Response({"detail": "No attendance records found for the selected dates."}, status=status.HTTP_404_NOT_FOUND)

        # Serialize the data
        serializer = AttendanceSerializer(attendance_records, many=True)

        return Response({
            "attendance_records": serializer.data,
            "from_date": from_date if from_date else None,
            "to_date": to_date if to_date else None,
        }, status=status.HTTP_200_OK)

##
# attendance/views.py



class ShowEmployeeAttendanceHistory(APIView):
    def post(self, request, format=None):
        # Get employee ID and date range from the request
        employee_id = request.data.get('employee_id')
        from_date = request.data.get('from_date')
        to_date = request.data.get('to_date')

        if not employee_id or not from_date or not to_date:
            return Response({"detail": "Missing employee_id, from_date, or to_date."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Convert string dates to datetime objects
            from_date = datetime.strptime(from_date, '%Y-%m-%d')
            to_date = datetime.strptime(to_date, '%Y-%m-%d')
        except ValueError:
            return Response({"detail": "Invalid date format. Please use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Get the employee object from the database
            employee = Employee.objects.get(employee_id=employee_id)
        except Employee.DoesNotExist:
            return Response({"detail": f"No employee found with ID {employee_id}."}, status=status.HTTP_404_NOT_FOUND)

        # Query attendance records for the selected employee and date range
        attendance_records = Attendance.objects.filter(
            employee=employee,
            date__gte=from_date,
            date__lte=to_date
        )

        if attendance_records.exists():
            # Serialize the attendance records
            serializer = AttendanceSerializer(attendance_records, many=True)
            return Response({
                "attendance_records": serializer.data,
                "employee_id": employee_id,
                "from_date": from_date.strftime('%Y-%m-%d'),
                "to_date": to_date.strftime('%Y-%m-%d')
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "detail": f"No attendance records found for employee ID {employee_id} in the selected date range."
            }, status=status.HTTP_404_NOT_FOUND)


# attendance/views.py



class EmployeeRequestCheckOutReset(APIView):
    def post(self, request, format=None):
        # Retrieve employee_id from session (assumed to be in session)
        user_id = request.session.get('user_id')
        if not user_id:
            return Response({"detail": "Employee not logged in."}, status=status.HTTP_400_BAD_REQUEST)

        today = datetime.today()  # Get today's date

        try:
            # Get employee object
            employee = Employee.objects.get(employee_id=user_id)
        except Employee.DoesNotExist:
            return Response({"detail": "Employee not found."}, status=status.HTTP_404_NOT_FOUND)
        
        # Check if the employee has checked in today
        last_attendance = Attendance.objects.filter(
            employee=employee,
            date=today,
            time_in__isnull=False
        ).first()

        if not last_attendance:
            # Employee has not checked in today
            return Response({"detail": "You can't reset the checkout time before check-in."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if a reset request has already been made for today
        existing_request = ResetRequest.objects.filter(
            employee=employee,
            date=today,
            status='Pending'
        ).exists()

        if existing_request:
            # A reset request has already been submitted
            return Response({"detail": "You have already sent the request. Please wait till the checkout time is reset."}, status=status.HTTP_400_BAD_REQUEST)

        # Process the reset request
        request_type = request.data.get('request_type')
        request_description = request.data.get('request_description')

        if not request_type or not request_description:
            return Response({"detail": "Request type and description are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new reset request
        reset_request = ResetRequest(
            employee=employee,
            date=today,
            request_type=request_type,
            request_description=request_description,
            status='Pending',
            created_at=datetime.now()
        )
        reset_request.save()

        # Serialize the reset request and return the response
        serializer = ResetRequestSerializer(reset_request)

        return Response({
            "detail": "Your reset request has been submitted successfully.",
            "reset_request": serializer.data
        }, status=status.HTTP_201_CREATED)

# attendance/views.py



class ManagerResetRequests(APIView):
    def get(self, request, format=None):
        # Fetch all pending reset requests
        reset_requests = ResetRequest.objects.filter(status='Pending', employee__isnull=False)

        reset_requests_list = []

        for reset_request in reset_requests:
            try:
                # Fetch the related attendance record
                employee_attendance = Attendance.objects.get(
                    employee=reset_request.employee,
                    date=reset_request.date
                )
                
                # Prepare the data for the response
                reset_requests_list.append({
                    'id': reset_request.id,
                    'employee_id': reset_request.employee.employee_id,  # Ensure this field exists in Employee model
                    'username': reset_request.employee.username,  # Ensure this field exists in Employee model
                    'request_type': reset_request.request_type,
                    'request_description': reset_request.request_description,
                    'date': reset_request.date,
                    'shift': employee_attendance.shift.shift_number,  # Ensure this field exists in Shift model
                    'time_in': employee_attendance.time_in,
                    'time_out': employee_attendance.time_out,
                    'in_status': employee_attendance.in_status,
                    'out_status': employee_attendance.out_status,
                    'notes': employee_attendance.notes,
                    'status': reset_request.status
                })
            except Attendance.DoesNotExist:
                # If no related attendance is found, we can skip this reset request
                continue

        return Response({
            'reset_requests': reset_requests_list
        }, status=status.HTTP_200_OK)




class ApproveResetRequestAPI(APIView):
    def post(self, request, request_id):
        # Find the reset request
        reset_request = get_object_or_404(ResetRequest, id=request_id)

        # Update the reset request's status to "Approved"
        reset_request.status = 'Approved'
        reset_request.save()

        # Prepare response data
        employee_id = reset_request.employee.id
        date = reset_request.date

        return Response({
            "message": "Reset request approved successfully.",
            "employee_id": employee_id,
            "date": date,
            "redirect_url": f"/reset_checkout_time/{employee_id}/{date}/"
        }, status=status.HTTP_200_OK)





class ResetCheckoutTimeAPI(APIView):
    def post(self, request, employee_id, date):
        clear_checkout = request.data.get('clear_checkout')
        checkout_time_str = request.data.get('checkout_time')

        try:
            # Get the attendance record
            attendance_record = get_object_or_404(Attendance, employee_id=employee_id, date=date)

            if clear_checkout:
                # Clear the checkout time
                attendance_record.time_out = None
                attendance_record.out_status = None
                attendance_record.overtime = None
                attendance_record.total_working_hours = None
            else:
                # Set the new checkout time
                if checkout_time_str:
                    # Validate and convert checkout time
                    checkout_time = datetime.strptime(checkout_time_str, '%H:%M:%S').time()
                    attendance_record.time_out = checkout_time
                    attendance_record.out_status = 'Updated by Manager'

                    # Calculate total working hours
                    time_in = datetime.strptime(str(attendance_record.time_in), '%H:%M:%S').time()
                    time_out = checkout_time

                    # Convert to datetime for calculation
                    today = datetime.today()
                    time_in_datetime = datetime.combine(today, time_in)
                    time_out_datetime = datetime.combine(today, time_out)

                    total_working_time = time_out_datetime - time_in_datetime
                    total_hours = total_working_time.seconds // 3600
                    total_minutes = (total_working_time.seconds % 3600) // 60
                    total_seconds = total_working_time.seconds % 60
                    attendance_record.total_working_hours = f"{total_hours:02}:{total_minutes:02}:{total_seconds:02}"

                    # Calculate overtime
                    shift_end_time = attendance_record.shift.shift_end_time
                    shift_end_datetime = datetime.combine(today, shift_end_time)
                    overtime_start_time = shift_end_datetime + timedelta(minutes=10)

                    if time_out_datetime > overtime_start_time:
                        overtime = time_out_datetime - overtime_start_time
                        overtime_hours = overtime.seconds // 3600
                        overtime_minutes = (overtime.seconds % 3600) // 60
                        overtime_seconds = overtime.seconds % 60
                        attendance_record.overtime = f"{overtime_hours:02}:{overtime_minutes:02}:{overtime_seconds:02}"
                    else:
                        attendance_record.overtime = "00:00:00"

            attendance_record.save()
            return Response({"message": "Checkout time updated successfully."}, status=status.HTTP_200_OK)

        except ValueError:
            return Response({"error": "Invalid time format. Please use HH:MM:SS."}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, employee_id, date):
        # Fetch the attendance record and return relevant details
        attendance_record = get_object_or_404(Attendance, employee_id=employee_id, date=date)
        return Response({
            "employee_id": employee_id,
            "date": date,
            "time_out": attendance_record.time_out,
            "total_working_hours": attendance_record.total_working_hours,
            "overtime": attendance_record.overtime,
        }, status=status.HTTP_200_OK)



class RejectResetRequestAPI(APIView):
    def post(self, request, request_id):
        # Find the reset request
        reset_request = get_object_or_404(ResetRequest, id=request_id)

        # Update the status to "Rejected"
        reset_request.status = 'Rejected'
        reset_request.save()

        return Response({"message": "Request rejected successfully."}, status=status.HTTP_200_OK)

# 


class ManagerCheckOutResetRequestAPI(APIView):
    def post(self, request):
        user_id = request.session.get('user_id')  # Retrieve manager_id from session
        today = datetime.today()

        # Check if the manager exists
        manager = get_object_or_404(Manager, manager_id=user_id)

        # Check if the manager has checked in today
        last_attendance = Attendance.objects.filter(
            manager=manager,
            date=today,
            time_in__isnull=False
        ).first()

        if not last_attendance:
            return Response(
                {"error": "You can't reset the checkout time before check-in."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if a reset request already exists for today
        if ResetRequest.objects.filter(manager=manager, date=today, status='Pending').exists():
            return Response(
                {"error": "You have already sent the request. Please wait for the reset."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate input using serializer
        serializer = ResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            # Create the reset request
            reset_request = ResetRequest.objects.create(
                manager=manager,
                date=today,
                request_type=serializer.validated_data.get('request_type'),
                request_description=serializer.validated_data.get('request_description'),
                status='Pending',
                created_at=datetime.now()
            )
            reset_request.save()

            return Response(
                {"message": "Your reset request has been submitted successfully."},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 


class AdminManagerResetRequestsAPI(APIView):
    def get(self, request):
        # Fetch all pending reset requests for managers
        reset_requests = ResetRequest.objects.filter(status='Pending', manager__isnull=False)
        serializer = ResetRequestSerializer(reset_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)




class AdminApproveManagerResetRequestAPI(APIView):
    def post(self, request, request_id):
        # Find the reset request for the manager
        reset_request = get_object_or_404(ResetRequest, id=request_id)

        # Update the reset request's status to "Approved"
        reset_request.status = 'Approved'
        reset_request.save()

        # Prepare the response data
        response_data = {
            'message': 'Reset request approved successfully.',
            'manager_id': reset_request.manager.id,
            'date': reset_request.date,
            'status': reset_request.status,
        }

        return Response(response_data, status=status.HTTP_200_OK)




class AdminRejectManagerResetRequestAPI(APIView):
    def post(self, request, request_id):
        # Find the reset request using the request_id
        reset_request = get_object_or_404(ResetRequest, id=request_id)

        # Update the status of the reset request to 'Rejected'
        reset_request.status = 'Rejected'
        reset_request.save()

        # Prepare response data
        response_data = {
            'message': 'The reset request has been rejected successfully.',
            'request_id': reset_request.id,
            'status': reset_request.status,
        }

        return Response(response_data, status=status.HTTP_200_OK)




class AdminResetManagerCheckoutTimeAPI(APIView):
    def post(self, request, manager_id, date):
        clear_checkout = request.data.get('clear_checkout')
        checkout_time_str = request.data.get('checkout_time')

        try:
            # Get the attendance record for the manager
            attendance_record = get_object_or_404(Attendance, manager_id=manager_id, date=date)
            shift = attendance_record.shift

            if clear_checkout:
                # Clear the checkout time
                attendance_record.time_out = None
                attendance_record.out_status = None
                attendance_record.overtime = None
                attendance_record.total_working_hours = None
            else:
                # Set the new checkout time
                if checkout_time_str:
                    # Validate and convert checkout time
                    checkout_time = datetime.strptime(checkout_time_str, '%H:%M:%S').time()
                    attendance_record.time_out = checkout_time
                    attendance_record.out_status = 'Updated by Admin'

                    # Calculate total working hours
                    time_in = datetime.strptime(str(attendance_record.time_in), '%H:%M:%S').time()
                    time_out = checkout_time

                    # Convert to datetime for calculation
                    today = datetime.today()
                    time_in_datetime = datetime.combine(today, time_in)
                    time_out_datetime = datetime.combine(today, time_out)

                    total_working_time = time_out_datetime - time_in_datetime
                    total_hours = total_working_time.seconds // 3600
                    total_minutes = (total_working_time.seconds % 3600) // 60
                    total_seconds = total_working_time.seconds % 60
                    attendance_record.total_working_hours = f"{total_hours:02}:{total_minutes:02}:{total_seconds:02}"

                    # Calculate overtime
                    shift_end_time = shift.shift_end_time
                    shift_end_datetime = datetime.combine(today, shift_end_time)
                    overtime_start_time = shift_end_datetime + timedelta(minutes=10)

                    if time_out_datetime > overtime_start_time:
                        overtime = time_out_datetime - overtime_start_time
                        overtime_hours = overtime.seconds // 3600
                        overtime_minutes = (overtime.seconds % 3600) // 60
                        overtime_seconds = overtime.seconds % 60
                        attendance_record.overtime = f"{overtime_hours:02}:{overtime_minutes:02}:{overtime_seconds:02}"
                    else:
                        attendance_record.overtime = "00:00:00"

            # Save the updated attendance record
            attendance_record.save()

            return Response({
                'message': 'Checkout time updated successfully.',
                'manager_id': manager_id,
                'date': date,
                'time_out': str(attendance_record.time_out),
                'total_working_hours': attendance_record.total_working_hours,
                'overtime': attendance_record.overtime
            }, status=status.HTTP_200_OK)

        except ValueError:
            return Response({
                'error': 'Invalid time format. Please use HH:MM:SS.'
            }, status=status.HTTP_400_BAD_REQUEST)

# views.py


class AdminEmployeeResetRequestsAPIView(APIView):
    def get(self, request):
        # Fetch all pending reset requests for employees
        reset_requests = ResetRequest.objects.filter(status='Pending', employee__isnull=False)
        serializer = ResetRequestSerializer(reset_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# views.py


class AdminApproveEmployeeResetRequestAPIView(APIView):
    def post(self, request, request_id):
        # Find the reset request using the request_id
        reset_request = get_object_or_404(ResetRequest, id=request_id)

        # Update the reset request's status to "Approved"
        reset_request.status = 'Approved'
        reset_request.save()

        # Prepare the response data (optionally include updated data)
        serializer = ResetRequestApprovalSerializer(reset_request)

        # Optionally, redirect to the reset checkout time page if needed
        # return redirect('admin_reset_employee_checkout_time', employee_id=reset_request.employee.id, date=reset_request.date)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

# views.py


class AdminRejectEmployeeResetRequestAPIView(APIView):
    def post(self, request, request_id):
        # Find the reset request using the request_id
        reset_request = get_object_or_404(ResetRequest, id=request_id)

        # Update the reset request's status to "Rejected"
        reset_request.status = 'Rejected'
        reset_request.save()

        # Prepare the response data (optionally include updated data)
        serializer = ResetRequestApprovalSerializer(reset_request)

        # Return the updated reset request data in the response
        return Response(serializer.data, status=status.HTTP_200_OK)


# views.py


class AdminResetEmployeeCheckoutTimeAPIView(APIView):
    def post(self, request, employee_id, date):
        clear_checkout = request.data.get('clear_checkout')
        checkout_time_str = request.data.get('checkout_time')

        try:
            # Get the attendance record for the employee and date
            attendance_record = get_object_or_404(Attendance, employee_id=employee_id, date=date)
            shift = attendance_record.shift

            if clear_checkout:
                # Clear the checkout time
                attendance_record.time_out = None
                attendance_record.out_status = None
                attendance_record.overtime = None
                attendance_record.total_working_hours = None
            else:
                # Set the new checkout time
                if checkout_time_str:
                    # Validate and convert checkout time
                    checkout_time = datetime.strptime(checkout_time_str, '%H:%M:%S').time()
                    attendance_record.time_out = checkout_time
                    attendance_record.out_status = 'Updated by Admin'

                    # Calculate total working hours
                    time_in = datetime.strptime(str(attendance_record.time_in), '%H:%M:%S').time()
                    time_out = checkout_time

                    # Convert to datetime for calculation
                    today = datetime.today()
                    time_in_datetime = datetime.combine(today, time_in)
                    time_out_datetime = datetime.combine(today, time_out)

                    total_working_time = time_out_datetime - time_in_datetime
                    total_hours = total_working_time.seconds // 3600
                    total_minutes = (total_working_time.seconds % 3600) // 60
                    total_seconds = total_working_time.seconds % 60
                    attendance_record.total_working_hours = f"{total_hours:02}:{total_minutes:02}:{total_seconds:02}"

                    # Calculate overtime
                    shift_end_time = shift.shift_end_time
                    shift_end_datetime = datetime.combine(today, shift_end_time)
                    overtime_start_time = shift_end_datetime + timedelta(minutes=10)

                    if time_out_datetime > overtime_start_time:
                        overtime = time_out_datetime - overtime_start_time
                        overtime_hours = overtime.seconds // 3600
                        overtime_minutes = (overtime.seconds % 3600) // 60
                        overtime_seconds = overtime.seconds % 60
                        attendance_record.overtime = f"{overtime_hours:02}:{overtime_minutes:02}:{overtime_seconds:02}"
                    else:
                        attendance_record.overtime = "00:00:00"

            attendance_record.save()

            # Serialize and return the updated attendance record
            serializer = AttendanceCheckoutSerializer(attendance_record)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ValueError:
            return Response({"error": "Invalid time format. Please use HH:MM:SS."}, status=status.HTTP_400_BAD_REQUEST)


# md and employee reset request
# views.py


class MdEmployeeResetRequestsAPIView(APIView):
    def get(self, request):
        # Fetch all pending reset requests for employees handled by the manager
        reset_requests = ResetRequest.objects.filter(status='Pending', employee__isnull=False)

        reset_requests_list = []

        for reset_request in reset_requests:
            try:
                # Fetch the related attendance record for the employee
                employee_attendance = Attendance.objects.get(
                    employee=reset_request.employee,
                    date=reset_request.date
                )

                # Prepare the data to be passed to the response
                reset_requests_list.append({
                    'id': reset_request.id, 
                    'employee_id': reset_request.employee.employee_id,  
                    'username': reset_request.employee.username, 
                    'request_type': reset_request.request_type,
                    'request_description': reset_request.request_description,
                    'date': reset_request.date,
                    'shift': employee_attendance.shift.shift_number, 
                    'time_in': employee_attendance.time_in,
                    'time_out': employee_attendance.time_out,
                    'in_status': employee_attendance.in_status,
                    'out_status': employee_attendance.out_status,
                    'notes': employee_attendance.notes,
                    'status': reset_request.status
                })
            except Attendance.DoesNotExist:
                continue

        return Response(reset_requests_list, status=status.HTTP_200_OK)


# views.py


class MdApproveEmployeeResetRequestAPIView(APIView):
    def post(self, request, request_id):
        # Find the reset request for the employee
        reset_request = get_object_or_404(ResetRequest, id=request_id)

        # Update the reset request's status to "Approved"
        reset_request.status = 'Approved'
        reset_request.save()

        # Serialize the reset request to return relevant details
        serializer = ResetRequestSerializer(reset_request)

        # Return the serialized data along with a success message
        return Response({
            'message': 'Reset request approved successfully.',
            'reset_request': serializer.data
        }, status=status.HTTP_200_OK)


# views.py


class MdRejectEmployeeResetRequestAPIView(APIView):
    def post(self, request, request_id):
        # Find the reset request for the employee
        reset_request = get_object_or_404(ResetRequest, id=request_id)

        # Update the reset request's status to "Rejected"
        reset_request.status = 'Rejected'
        reset_request.save()

        # Serialize the reset request to return relevant details
        serializer = ResetRequestSerializer(reset_request)

        # Return the serialized data along with a success message
        return Response({
            'message': 'Reset request rejected successfully.',
            'reset_request': serializer.data
        }, status=status.HTTP_200_OK)


# views.py


class MdResetEmployeeCheckoutTimeAPIView(APIView):
    def get(self, request, employee_id, date):
        # Get the attendance record for the employee and date
        attendance_record = get_object_or_404(Attendance, employee_id=employee_id, date=date)

        # Serialize and return the attendance data
        serializer = AttendanceSerializer(attendance_record)
        return Response(serializer.data)

    def post(self, request, employee_id, date):
        # Get the attendance record for the employee and date
        attendance_record = get_object_or_404(Attendance, employee_id=employee_id, date=date)

        clear_checkout = request.data.get('clear_checkout', False)
        checkout_time_str = request.data.get('checkout_time')

        try:
            if clear_checkout:
                # Clear the checkout time
                attendance_record.time_out = None
                attendance_record.out_status = None
                attendance_record.overtime = None
                attendance_record.total_working_hours = None
            else:
                # Set the new checkout time
                if checkout_time_str:
                    # Validate and convert checkout time
                    checkout_time = datetime.strptime(checkout_time_str, '%H:%M:%S').time()
                    attendance_record.time_out = checkout_time
                    attendance_record.out_status = 'Updated by MD'

                    # Calculate total working hours
                    time_in = datetime.strptime(str(attendance_record.time_in), '%H:%M:%S').time()
                    time_out = checkout_time

                    # Convert to datetime for calculation
                    today = datetime.today()
                    time_in_datetime = datetime.combine(today, time_in)
                    time_out_datetime = datetime.combine(today, time_out)

                    total_working_time = time_out_datetime - time_in_datetime
                    total_hours = total_working_time.seconds // 3600
                    total_minutes = (total_working_time.seconds % 3600) // 60
                    total_seconds = total_working_time.seconds % 60
                    attendance_record.total_working_hours = f"{total_hours:02}:{total_minutes:02}:{total_seconds:02}"

                    # Calculate overtime
                    shift_end_time = attendance_record.shift.shift_end_time
                    shift_end_datetime = datetime.combine(today, shift_end_time)
                    overtime_start_time = shift_end_datetime + timedelta(minutes=10)

                    if time_out_datetime > overtime_start_time:
                        overtime = time_out_datetime - overtime_start_time
                        overtime_hours = overtime.seconds // 3600
                        overtime_minutes = (overtime.seconds % 3600) // 60
                        overtime_seconds = overtime.seconds % 60
                        attendance_record.overtime = f"{overtime_hours:02}:{overtime_minutes:02}:{overtime_seconds:02}"
                    else:
                        attendance_record.overtime = "00:00:00"

            # Save the updated attendance record
            attendance_record.save()

            # Serialize the updated attendance record and return response
            serializer = AttendanceSerializer(attendance_record)
            return Response({
                'message': 'Checkout time updated successfully.',
                'attendance': serializer.data
            }, status=status.HTTP_200_OK)

        except ValueError:
            raise ValidationError('Invalid time format. Please use HH:MM:SS.')


# md & manager reset checkout time
# views.py

class MdManagerResetRequestsAPIView(APIView):
    def get(self, request):
        # Fetch all pending reset requests for managers
        reset_requests = ResetRequest.objects.filter(status='Pending', manager__isnull=False)

        reset_requests_list = []

        for reset_request in reset_requests:
            try:
                # Fetch the related attendance record for the manager
                manager_attendance = Attendance.objects.get(
                    manager=reset_request.manager,
                    date=reset_request.date
                )
                
                # Append the request data to the list
                reset_requests_list.append({
                    'id': reset_request.id,
                    'manager_id': reset_request.manager.manager_id,
                    'username': reset_request.manager.username,
                    'request_type': reset_request.request_type,
                    'request_description': reset_request.request_description,
                    'date': reset_request.date,
                    'shift': manager_attendance.shift.shift_number,
                    'time_in': manager_attendance.time_in,
                    'time_out': manager_attendance.time_out,
                    'in_status': manager_attendance.in_status,
                    'out_status': manager_attendance.out_status,
                    'notes': manager_attendance.notes,
                    'status': reset_request.status
                })
            except Attendance.DoesNotExist:
                continue

        # Return the list of reset requests in the response
        return Response({'reset_requests': reset_requests_list}, status=status.HTTP_200_OK)

# views.py


class MdApproveManagerResetRequestAPIView(APIView):
    def post(self, request, request_id):
        # Find the reset request for the manager
        reset_request = get_object_or_404(ResetRequest, id=request_id)

        # Update the reset request's status to "Approved"
        reset_request.status = 'Approved'
        reset_request.save()

        # Optionally, you can serialize the reset request object to return it in the response
        serializer = ResetRequestSerializer(reset_request)

        # Prepare the response data
        response_data = {
            'message': 'Reset request approved successfully.',
            'reset_request': serializer.data,
        }

        # Return a JSON response with the approval status and the serialized data
        return JsonResponse(response_data, status=status.HTTP_200_OK)



@api_view(['POST'])
def md_reject_manager_reset_request_api(request, request_id):
    try:
        reset_request = ResetRequest.objects.get(id=request_id)
    except ResetRequest.DoesNotExist:
        return Response({"detail": "Reset request not found."}, status=status.HTTP_404_NOT_FOUND)

    # Using the serializer to update the status
    serializer = ResetRequestSerializer(reset_request, data={"status": "Rejected"}, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"detail": "Reset request rejected successfully."}, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
def md_reset_manager_checkout_time_api(request, manager_id, date):
    try:
        attendance_record = Attendance.objects.get(manager_id=manager_id, date=date)
    except Attendance.DoesNotExist:
        return Response({"detail": "Attendance record not found."}, status=status.HTTP_404_NOT_FOUND)

    clear_checkout = request.data.get('clear_checkout')
    checkout_time_str = request.data.get('checkout_time')

    if clear_checkout:
        # Clear the checkout time
        attendance_record.time_out = None
        attendance_record.out_status = None
        attendance_record.overtime = None
        attendance_record.total_working_hours = None
    else:
        if checkout_time_str:
            try:
                # Validate and convert checkout time
                checkout_time = datetime.strptime(checkout_time_str, '%H:%M:%S').time()
                attendance_record.time_out = checkout_time
                attendance_record.out_status = 'Updated by MD'

                # Calculate total working hours
                time_in = datetime.strptime(str(attendance_record.time_in), '%H:%M:%S').time()
                time_out = checkout_time

                # Convert to datetime for calculation
                today = datetime.today()
                time_in_datetime = datetime.combine(today, time_in)
                time_out_datetime = datetime.combine(today, time_out)

                total_working_time = time_out_datetime - time_in_datetime
                total_hours = total_working_time.seconds // 3600
                total_minutes = (total_working_time.seconds % 3600) // 60
                total_seconds = total_working_time.seconds % 60
                attendance_record.total_working_hours = f"{total_hours:02}:{total_minutes:02}:{total_seconds:02}"

                # Calculate overtime
                shift_end_time = attendance_record.shift.shift_end_time
                shift_end_datetime = datetime.combine(today, shift_end_time)
                overtime_start_time = shift_end_datetime + timedelta(minutes=10)

                if time_out_datetime > overtime_start_time:
                    overtime = time_out_datetime - overtime_start_time
                    overtime_hours = overtime.seconds // 3600
                    overtime_minutes = (overtime.seconds % 3600) // 60
                    overtime_seconds = overtime.seconds % 60
                    attendance_record.overtime = f"{overtime_hours:02}:{overtime_minutes:02}:{overtime_seconds:02}"
                else:
                    attendance_record.overtime = "00:00:00"
            except ValueError:
                return Response({"detail": "Invalid time format. Please use HH:MM:SS."}, status=status.HTTP_400_BAD_REQUEST)

    # Save the attendance record
    attendance_record.save()
    return Response({"detail": "Checkout time updated successfully."}, status=status.HTTP_200_OK)


#####################################################################################################################







#manager_weekly_attenance_chart


@api_view(['GET'])
def manager_weekly_attendance_chart_api(request):
    user_id = request.session.get('user_id')  # Assuming manager ID is in the session
    
    # Get the current week offset from GET parameters (how many weeks to move forward/backward)
    week_offset = int(request.GET.get('week_offset', 0))
    
    today = datetime.now().date()
    start_of_week = today - timedelta(days=today.weekday()) + timedelta(weeks=week_offset)  # Adjust the week by the offset
    end_of_week = start_of_week + timedelta(days=6)

    # Initialize a dictionary to store total hours per day with the date
    weekly_hours = {}
    labels = []
    
    # Variables to store total hours for the week and total overtime
    total_hours = 0
    total_overtime = 0
    daily_working_hours = 8  # Standard working hours per day

    for i in range(7):  # Monday to Sunday
        day_date = start_of_week + timedelta(days=i)
        day_label = day_date.strftime('%a %b %d')  # Format: "Mon Sep 11"
        labels.append(day_label)
        weekly_hours[day_label] = 0  # Initialize the hours for each day as 0

    # Get all attendance entries for the selected week
    attendance_records = Attendance.objects.filter(
        manager__manager_id=user_id,
        date__range=[start_of_week, end_of_week]
    )

    # Get all approved leave requests for the selected week
    approved_leaves = ManagerLeaveRequest.objects.filter(
        manager__manager_id=user_id,
        start_date__lte=end_of_week,
        end_date__gte=start_of_week,
        status='approved'
    )

    leave_days = set()
    for leave in approved_leaves:
        # Iterate through the leave days within the week
        leave_start = max(leave.start_date, start_of_week)
        leave_end = min(leave.end_date, end_of_week)
        for i in range((leave_end - leave_start).days + 1):
            leave_day = (leave_start + timedelta(days=i)).strftime('%a %b %d')
            leave_days.add(leave_day)

    # Calculate total working hours and overtime for each day
    for record in attendance_records:
        if record.time_in and record.time_out:
            # Convert time_in and time_out to datetime and calculate work duration
            work_duration = (datetime.combine(datetime.today(), record.time_out) - 
                             datetime.combine(datetime.today(), record.time_in)).total_seconds() / 3600
            day_label = record.date.strftime('%a %b %d')  # Ensure record.date is also handled as date
            if day_label in weekly_hours:
                weekly_hours[day_label] += work_duration

            # Calculate total hours and overtime
            total_hours += work_duration
            if work_duration > daily_working_hours:
                total_overtime += work_duration - daily_working_hours

    total_hours = round(total_hours, 2)
    total_overtime = round(total_overtime, 2)

    # Get the current month
    current_month = start_of_week.strftime('%B')

    work_data = list(weekly_hours.values())
    leave_data = [daily_working_hours if label in leave_days else 0 for label in labels]

    # Prepare the response data
    data = {
        'labels': labels,
        'data': work_data,
        'leave_data': leave_data,
        'total_hours': total_hours,
        'total_overtime': total_overtime,
        'month': current_month,
        'week_offset': week_offset,
    }

    # Return the response using the serializer
    serializer = ManagerWeeklyAttendanceSerializer(data)
    return Response(serializer.data)

# views.py


class ShowEmployeeWeeklyChartAPIView(APIView):

    def get(self, request):
        employee_id = request.GET.get('employee_id')
        if not employee_id:
            return Response({'error': 'Employee ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Get the current week offset from GET parameters (how many weeks to move forward/backward)
        week_offset = int(request.GET.get('week_offset', 0))

        today = datetime.now().date()
        start_of_week = today - timedelta(days=today.weekday()) + timedelta(weeks=week_offset)  # Adjust the week by the offset
        end_of_week = start_of_week + timedelta(days=6)

        # Initialize a dictionary to store total hours per day with the date
        weekly_hours = {}
        labels = []

        # Variables to store total hours for the week and total overtime
        total_hours = 0
        total_overtime = 0
        daily_working_hours = 8  # Standard working hours per day

        for i in range(6):  # Monday to Saturday
            day_date = start_of_week + timedelta(days=i)
            day_label = day_date.strftime('%a %b %d')  # Format: "Mon Sep 11"
            labels.append(day_label)
            weekly_hours[day_label] = 0  # Initialize the hours for each day as 0

        # Get all attendance entries for the selected week
        attendance_records = Attendance.objects.filter(
            employee__employee_id=employee_id,  # Filter by the Employee ID
            date__range=[start_of_week, end_of_week]
        )

        # Get approved leave requests overlapping with the selected week
        approved_leaves = LeaveRequest.objects.filter(
            employee__employee_id=employee_id,
            status='approved',
            start_date__lte=end_of_week,
            end_date__gte=start_of_week
        )

        leave_days = set()
        for leave in approved_leaves:
            leave_start = max(leave.start_date, start_of_week)
            leave_end = min(leave.end_date, end_of_week)
            for i in range((leave_end - leave_start).days + 1):
                leave_day = (leave_start + timedelta(days=i)).strftime('%a %b %d')
                leave_days.add(leave_day)

        # Calculate total working hours and overtime for each day
        for record in attendance_records:
            if record.time_in and record.time_out:
                work_duration = (datetime.combine(datetime.today(), record.time_out) - 
                                 datetime.combine(datetime.today(), record.time_in)).total_seconds() / 3600
                day_label = record.date.strftime('%a %b %d')  # 'Mon Sep 11', etc.
                if day_label in weekly_hours:
                    weekly_hours[day_label] += work_duration

                total_hours += work_duration
                if work_duration > daily_working_hours:
                    total_overtime += work_duration - daily_working_hours

        total_hours = round(total_hours, 2)
        total_overtime = round(total_overtime, 2)

        # Get the current month
        current_month = start_of_week.strftime('%B')

        work_data = list(weekly_hours.values())
        leave_data = [daily_working_hours if label in leave_days else 0 for label in labels]

        # Prepare response data
        response_data = {
            'labels': labels,
            'data': work_data,
            'leave_data': leave_data,
            'month': current_month,
            'week_offset': week_offset,
            'total_hours': total_hours,
            'total_overtime': total_overtime,
            'employee_id': employee_id,
        }

        return Response(response_data, status=status.HTTP_200_OK)





@api_view(['GET'])
def manager_monthly_attendance_chart_api(request):
    user_id = request.session.get('user_id')  # Assuming manager ID is stored in the session

    month_offset = int(request.GET.get('month_offset', 0))

    today = datetime.now()
    current_month = today.month + month_offset
    current_year = today.year

    if current_month < 1:
        current_month += 12
        current_year -= 1
    elif current_month > 12:
        current_month -= 12
        current_year += 1

    start_of_month = datetime(current_year, current_month, 1)
    last_day = monthrange(current_year, current_month)[1]
    end_of_month = datetime(current_year, current_month, last_day)

    weekly_hours = [0, 0, 0, 0]
    working_days_per_week = [0, 0, 0, 0]
    week_labels = ["Week 1", "Week 2", "Week 3", "Week 4"]
    total_hours = 0
    total_overtime = 0
    daily_working_hours = 8

    attendance_records = Attendance.objects.filter(
        manager__manager_id=user_id,
        date__range=[start_of_month, end_of_month]
    )

    for record in attendance_records:
        if record.time_in and record.time_out:
            work_duration = datetime.combine(datetime.today(), record.time_out) - datetime.combine(datetime.today(), record.time_in)
            hours_worked = work_duration.total_seconds() / 3600

            week_num = (record.date.day - 1) // 7
            if week_num < 4:
                weekly_hours[week_num] += hours_worked
                working_days_per_week[week_num] += 1

            total_hours += hours_worked
            if hours_worked > daily_working_hours:
                total_overtime += hours_worked - daily_working_hours

    total_hours = round(total_hours, 3)
    total_overtime = round(total_overtime, 3)

    average_hours_per_week = []
    for week_num in range(4):
        if working_days_per_week[week_num] > 0:
            avg_hours = weekly_hours[week_num] / working_days_per_week[week_num]
        else:
            avg_hours = 0
        average_hours_per_week.append(round(avg_hours, 2))

    week_avg_data = list(zip(week_labels, average_hours_per_week))

    current_month_name = start_of_month.strftime('%B')

    data = {
        'month': current_month_name,
        'week_avg_data': week_avg_data,
        'total_hours': total_hours,
        'total_overtime': total_overtime,
        'month_offset': month_offset,
    }

    return Response(data)


# show employees monthly chart from manager perspective

# views.py

 # type: ignore

class EmployeeMonthlyChartAPIView(APIView):
    
    def get(self, request):
        employee_id = request.GET.get('employee_id')
        month_offset = int(request.GET.get('month_offset', 0))
        
        if not employee_id:
            return Response({'error': 'Employee ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        today = datetime.now().date()
        current_month = today.month + month_offset
        current_year = today.year

        if current_month < 1:
            current_month += 12
            current_year -= 1
        elif current_month > 12:
            current_month -= 12
            current_year += 1

        start_of_month = datetime(current_year, current_month, 1)
        last_day = monthrange(current_year, current_month)[1]
        end_of_month = datetime(current_year, current_month, last_day)

        weekly_hours = [0] * 4  # For 4 weeks in a month
        leave_weeks = [0] * 4   # To track leave days per week
        week_labels = ["Week 1", "Week 2", "Week 3", "Week 4"]

        total_hours = 0
        total_overtime = 0
        daily_working_hours = 8

        # Get attendance records for the employee during the selected month
        attendance_records = Attendance.objects.filter(
            employee__employee_id=employee_id,
            date__range=[start_of_month.date(), end_of_month.date()]
        )

        # Calculate total working hours and overtime for each week
        for record in attendance_records:
            if record.time_in and record.time_out:
                work_duration = (datetime.combine(datetime.today(), record.time_out) - 
                                 datetime.combine(datetime.today(), record.time_in)).total_seconds() / 3600
                week_num = (record.date.day - 1) // 7
                if week_num < 4:
                    weekly_hours[week_num] += work_duration

                total_hours += work_duration
                if work_duration > daily_working_hours:
                    total_overtime += work_duration - daily_working_hours

        total_hours = round(total_hours, 2)
        total_overtime = round(total_overtime, 2)

        # Calculate weekly averages
        weekly_averages = [0] * 4
        for week_num in range(4):
            if leave_weeks[week_num] == 0 and weekly_hours[week_num] > 0:
                # Count the working days in that week
                working_days = Attendance.objects.filter(
                    employee__employee_id=employee_id,
                    date__range=[start_of_month.date() + timedelta(weeks=week_num),
                                 start_of_month.date() + timedelta(weeks=week_num + 1) - timedelta(days=1)],
                    time_in__isnull=False,
                    time_out__isnull=False
                ).count()
                if working_days > 0:
                    weekly_averages[week_num] = round(weekly_hours[week_num] / working_days, 2)

        current_month_name = start_of_month.strftime('%B')

        work_data = weekly_hours

        context = {
            'labels': week_labels,
            'data': work_data,
            'month': current_month_name,
            'month_offset': month_offset,
            'total_hours': total_hours,
            'total_overtime': total_overtime,
            'employee_id': employee_id,
        }

        # Serialize the data
        serializer = EmployeeMonthlyChartSerializer(context)
        return Response(serializer.data)


from authentication.models import Manager, Supervisor

# views.py



class SupervisorAttendanceFormAPIView(APIView):
    
    def get(self, request):
        user_id = request.session.get('user_id')  # Assuming manager ID is stored in session

        try:
            supervisor = Supervisor.objects.get(supervisor_id=user_id)
            assigned_shift = supervisor.shift
            shift = Shift.objects.get(shift_number=assigned_shift.shift_number)
        except Supervisor.DoesNotExist or Shift.DoesNotExist:
            raise NotFound('Supervisor or shift not found.')

        locations = Location.objects.all()
        today = datetime.now().strftime('%Y-%m-%d')

        last_attendance = Attendance.objects.filter(
            supervisor=supervisor,
            date=today
        ).first()

        show_checkout = False
        thank_you_message = ''

        if last_attendance and last_attendance.time_out is None:
            show_checkout = True
            thank_you_message = 'Thanks for today'
        elif last_attendance and last_attendance.time_out is not None:
            raise NotFound('You have already checked out for today. Please try again tomorrow.')

        context = {
            'locations': [location.name for location in locations],  # Assuming Location has a 'name' field
            'shift': shift.shift_name,  # Assuming Shift has a 'shift_name' field
            'show_checkout': show_checkout,
            'thank_you_message': thank_you_message,
        }

        # Serialize and return the response
        serializer = SupervisorAttendanceSerializer(context)
        return Response(serializer.data)


from leaves.models import LeaveRequest, SupervisorLeaveRequest
# views.py


class SubmitSupervisorAttendanceAPIView(APIView):

    def post(self, request):
        user_id = request.session.get('user_id')

        # Restrict check-in on Sundays
        if datetime.now().weekday() == 6:
            return Response({'message': 'Check-in is not allowed on Sundays.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check for leave status
        try:
            leave_request = SupervisorLeaveRequest.objects.filter(supervisor__supervisor_id=user_id, status='Approved').latest('start_date')

            # Check if the current date is within the leave period
            current_date = datetime.now().date()
            if leave_request.start_date <= current_date <= leave_request.end_date:
                return Response({'message': 'You are on leave. Please check in after your leave ends.'}, status=status.HTTP_400_BAD_REQUEST)
        except SupervisorLeaveRequest.DoesNotExist:
            # No leave request found, proceed with attendance check
            pass

        # Check if the supervisor is checking in or out
        if 'check_in' in request.data:
            shift_number = request.data.get('shift')
            location_name = request.data.get('location')
            notes = request.data.get('notes')

            try:
                shift = Shift.objects.get(shift_number=shift_number)
                location = Location.objects.get(location_name=location_name)
                supervisor = Supervisor.objects.get(supervisor_id=user_id)
            except (Shift.DoesNotExist, Location.DoesNotExist, Supervisor.DoesNotExist):
                return Response({'message': 'Shift, location, or supervisor not found.'}, status=status.HTTP_404_NOT_FOUND)

            shift_start_time = shift.shift_start_time
            shift_end_time = shift.shift_end_time
            current_time = datetime.now().time()

            if current_time > shift_end_time:
                return Response({'message': 'You cannot check in after the shift end time.'}, status=status.HTTP_400_BAD_REQUEST)

            today = datetime.now().strftime('%Y-%m-%d')
            existing_attendance = Attendance.objects.filter(
                supervisor=supervisor,
                date=today
            ).first()

            if existing_attendance:
                return Response({'message': 'You have already checked in for today.'}, status=status.HTTP_400_BAD_REQUEST)

            shift_start_datetime = datetime.combine(datetime.today(), shift_start_time)
            early_threshold = shift_start_datetime - timedelta(minutes=10)
            late_threshold = shift_start_datetime + timedelta(minutes=10)
            current_datetime = datetime.combine(datetime.today(), current_time)

            if early_threshold <= current_datetime <= late_threshold:
                in_status = 'On time'
                time_in = shift_start_time.strftime('%H:%M:%S')
            elif current_datetime < early_threshold:
                in_status = 'Early'
                time_in = shift_start_time.strftime('%H:%M:%S')
            else:
                in_status = 'Late'
                time_in = current_datetime.strftime('%H:%M:%S')

            Attendance.objects.create(
                date=today,
                shift=shift,
                location=location,
                notes=notes,
                time_in=time_in,
                time_out=None,
                in_status=in_status,
                out_status=None,
                overtime=None,
                total_working_hours=None,
                supervisor=supervisor,
            )

            return Response({'message': 'Checked in successfully.', 'status': in_status}, status=status.HTTP_201_CREATED)

        elif 'check_out' in request.data:
            current_time = datetime.now().time()
            today = datetime.now().strftime('%Y-%m-%d')
            time_out = datetime.now().strftime('%H:%M:%S')

            try:
                last_attendance = Attendance.objects.get(
                    supervisor__supervisor_id=user_id,
                    date=today,
                    time_out=None
                )
                shift = last_attendance.shift
            except Attendance.DoesNotExist:
                return Response({'message': 'No check-in found for today.'}, status=status.HTTP_400_BAD_REQUEST)

            shift_end_time = shift.shift_end_time
            overtime_start_time = (datetime.combine(datetime.today(), shift_end_time) + timedelta(minutes=10)).time()

            if current_time < shift_end_time:
                out_status = 'Early'
                overtime_str = '00:00:00'
            elif shift_end_time <= current_time <= overtime_start_time:
                out_status = 'On time'
                overtime_str = '00:00:00'
                time_out = shift_end_time
            else:
                out_status = 'Overtime'
                overtime = datetime.combine(datetime.today(), current_time) - datetime.combine(datetime.today(), overtime_start_time)
                overtime_hours = overtime.seconds // 3600
                overtime_minutes = (overtime.seconds % 3600) // 60
                overtime_seconds = overtime.seconds % 60
                overtime_str = f"{overtime_hours:02}:{overtime_minutes:02}:{overtime_seconds:02}"

            # Directly use time_in from the database without conversion
            time_in = last_attendance.time_in
            total_working_time = datetime.combine(datetime.today(), current_time) - datetime.combine(datetime.today(), time_in)
            total_hours = total_working_time.seconds // 3600
            total_minutes = (total_working_time.seconds % 3600) // 60
            total_seconds = total_working_time.seconds % 60
            total_working_hours = f"{total_hours:02}:{total_minutes:02}:{total_seconds:02}"

            last_attendance.time_out = time_out
            last_attendance.out_status = out_status
            last_attendance.overtime = overtime_str
            last_attendance.total_working_hours = total_working_hours
            last_attendance.save()

            return Response({'message': f'Checked out successfully. Status: {out_status}', 'status': out_status, 'overtime': overtime_str, 'total_working_hours': total_working_hours}, status=status.HTTP_200_OK)

        return Response({'message': 'Invalid request.'}, status=status.HTTP_400_BAD_REQUEST)


# views.py


class SupervisorAttendanceHistory(APIView):

    def get(self, request):
        user_id = request.session.get('user_id')  # Assuming manager ID is stored in session

        if not user_id:
            return Response({'error': 'User not logged in.'}, status=status.HTTP_400_BAD_REQUEST)

        # Get the date range from the request
        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')

        # Initialize the query to fetch all attendance records for the logged-in supervisor
        query = Attendance.objects.filter(supervisor__supervisor_id=user_id)

        if from_date and to_date:
            try:
                # Parse the from_date and to_date
                from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
                to_date = datetime.strptime(to_date, '%Y-%m-%d').date()

                if from_date > to_date:
                    return Response({'error': 'From date cannot be after to date.'}, status=status.HTTP_400_BAD_REQUEST)

                # Filter the records based on the date range
                query = query.filter(date__range=[from_date, to_date])

            except ValueError:
                return Response({'error': 'Invalid date format. Please use YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch the filtered records
        attendance_records = query.select_related('shift', 'location')

        # Serialize the records
        serializer = AttendanceSerializer(attendance_records, many=True)

        # Return the serialized data
        return Response({'attendance_records': serializer.data}, status=status.HTTP_200_OK)

# views.py


class SupervisorRequestCheckOutReset(APIView):

    def post(self, request):
        user_id = request.session.get('user_id')
        today = datetime.today().date()

        # Check if supervisor is logged in
        if not user_id:
            return Response({'error': 'User not logged in.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if supervisor exists
        try:
            supervisor = Supervisor.objects.get(supervisor_id=user_id)
        except Supervisor.DoesNotExist:
            return Response({'error': 'Supervisor not found.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if supervisor has checked in today
        last_attendance = Attendance.objects.filter(
            supervisor=supervisor,
            date=today,
            time_in__isnull=False
        ).first()

        if not last_attendance:
            return Response({'error': "You can't reset the checkout time before check-in."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if a reset request is already pending for today
        existing_request = ResetRequest.objects.filter(
            supervisor=supervisor,
            date=today,
            status='Pending'
        ).exists()

        if existing_request:
            return Response({'error': 'You have already sent the request. Please wait for the reset.'}, status=status.HTTP_400_BAD_REQUEST)

        # Process the reset request
        request_type = request.data.get('request_type')
        request_description = request.data.get('request_description')

        if not request_type or not request_description:
            return Response({'error': 'Request type and description are required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new reset request
        reset_request = ResetRequest(
            supervisor=supervisor,
            date=today,
            request_type=request_type,
            request_description=request_description,
            status='Pending',
            created_at=datetime.now()
        )
        reset_request.save()

        # Serialize the reset request data
        serializer = ResetRequestSerializer(reset_request)

        return Response({'message': 'Your reset request has been submitted successfully.', 'data': serializer.data}, status=status.HTTP_201_CREATED)


# views.py


class AdminSupervisorResetRequests(APIView):
    def get(self, request):
        # Fetch all pending reset requests
        reset_requests = ResetRequest.objects.filter(status='Pending', supervisor__isnull=False)

        reset_requests_list = []

        for reset_request in reset_requests:
            try:
                # Fetch the related attendance record
                supervisor_attendance = Attendance.objects.get(
                    supervisor=reset_request.supervisor,
                    date=reset_request.date
                )

                # Add the reset request data along with attendance information
                reset_requests_list.append({
                    'id': reset_request.id, 
                    'supervisor_id': reset_request.supervisor.supervisor_id,  
                    'username': reset_request.supervisor.username, 
                    'request_type': reset_request.request_type,
                    'request_description': reset_request.request_description,
                    'date': reset_request.date,
                    'shift': supervisor_attendance.shift.shift_number, 
                    'time_in': supervisor_attendance.time_in,
                    'time_out': supervisor_attendance.time_out,
                    'in_status': supervisor_attendance.in_status,
                    'out_status': supervisor_attendance.out_status,
                    'notes': supervisor_attendance.notes,
                    'status': reset_request.status
                })
            except Attendance.DoesNotExist:
                # Optionally log this error or handle it differently
                continue

        return Response({'reset_requests': reset_requests_list}, status=status.HTTP_200_OK)


# views.py


class AdminApproveSupervisorResetRequest(APIView):
    def post(self, request, request_id):
        # Find the reset request for the supervisor
        reset_request = get_object_or_404(ResetRequest, id=request_id)

        # Update the reset request's status to "Approved"
        reset_request.status = 'Approved'
        reset_request.save()

        # Optional: Serialize the updated reset request to include in response if needed
        serializer = ResetRequestApprovalSerializer(reset_request)

        supervisor_id = reset_request.supervisor.id
        date = reset_request.date

        # Return response after the approval, redirect can be handled on the front-end
        return Response({
            'message': 'Reset request approved successfully.',
            'supervisor_id': supervisor_id,
            'date': date,
            'reset_request': serializer.data
        }, status=status.HTTP_200_OK)

# views.py


class AdminRejectSupervisorResetRequest(APIView):
    def post(self, request, request_id):
        # Find the reset request using the request_id
        reset_request = get_object_or_404(ResetRequest, id=request_id)

        # Update the status of the reset request to 'Rejected'
        reset_request.status = 'Rejected'
        reset_request.save()

        # Optionally, serialize the updated reset request to include in the response
        serializer = ResetRequestRejectionSerializer(reset_request)

        # Return a response after rejecting the reset request
        return Response({
            'message': 'The reset request has been rejected successfully.',
            'reset_request': serializer.data
        }, status=status.HTTP_200_OK)


# views.py


class AdminResetSupervisorCheckoutTime(APIView):
    def post(self, request, supervisor_id, date):
        # Get the attendance record for the supervisor
        attendance_record = get_object_or_404(Attendance, supervisor_id=supervisor_id, date=date)
        shift = attendance_record.shift

        # Deserialize the request data
        serializer = SupervisorCheckoutTimeSerializer(data=request.data)

        if serializer.is_valid():
            clear_checkout = serializer.validated_data.get('clear_checkout', False)
            checkout_time_str = serializer.validated_data.get('checkout_time')

            if clear_checkout:
                # Clear the checkout time
                attendance_record.time_out = None
                attendance_record.out_status = None
                attendance_record.overtime = None
                attendance_record.total_working_hours = None
            elif checkout_time_str:
                # Set the new checkout time
                checkout_time = datetime.strptime(checkout_time_str, '%H:%M:%S').time()
                attendance_record.time_out = checkout_time
                attendance_record.out_status = 'Updated by Admin'

                # Calculate total working hours
                time_in = datetime.strptime(str(attendance_record.time_in), '%H:%M:%S').time()
                time_out = checkout_time

                # Convert to datetime for calculation
                today = datetime.today()
                time_in_datetime = datetime.combine(today, time_in)
                time_out_datetime = datetime.combine(today, time_out)

                total_working_time = time_out_datetime - time_in_datetime
                total_hours = total_working_time.seconds // 3600
                total_minutes = (total_working_time.seconds % 3600) // 60
                total_seconds = total_working_time.seconds % 60
                attendance_record.total_working_hours = f"{total_hours:02}:{total_minutes:02}:{total_seconds:02}"

                # Calculate overtime
                shift_end_time = shift.shift_end_time
                shift_end_datetime = datetime.combine(today, shift_end_time)
                overtime_start_time = shift_end_datetime + timedelta(minutes=10)

                if time_out_datetime > overtime_start_time:
                    overtime = time_out_datetime - overtime_start_time
                    overtime_hours = overtime.seconds // 3600
                    overtime_minutes = (overtime.seconds % 3600) // 60
                    overtime_seconds = overtime.seconds % 60
                    attendance_record.overtime = f"{overtime_hours:02}:{overtime_minutes:02}:{overtime_seconds:02}"
                else:
                    attendance_record.overtime = "00:00:00"

            # Save the updated attendance record
            attendance_record.save()

            return Response({
                'message': 'Checkout time updated successfully.',
                'attendance_record': {
                    'id': attendance_record.id,
                    'time_out': attendance_record.time_out,
                    'out_status': attendance_record.out_status,
                    'total_working_hours': attendance_record.total_working_hours,
                    'overtime': attendance_record.overtime,
                }
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# views.py


class MdSupervisorResetRequests(APIView):
    def get(self, request):
        # Fetch all pending reset requests for supervisors
        reset_requests = ResetRequest.objects.filter(status='Pending', supervisor__isnull=False)

        # Serialize the reset requests data
        serializer = ResetRequestSerializer(reset_requests, many=True)
        
        # Return the serialized data as a response
        return Response(serializer.data, status=status.HTTP_200_OK)


# views.py



class MDApproveSupervisorResetRequest(APIView):
    def put(self, request, request_id):
        reset_request = get_object_or_404(ResetRequest, id=request_id)

        # Update the status to 'Approved'
        serializer = ResetRequestApprovalSerializer(reset_request, data={'status': 'Approved'}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# views.py



class MDRejectSupervisorResetRequest(APIView):
    def put(self, request, request_id):
        reset_request = get_object_or_404(ResetRequest, id=request_id)

        # Update the status to 'Rejected'
        serializer = ResetRequestRejectionSerializer(reset_request, data={'status': 'Rejected'}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# views.py


class MDResetSupervisorCheckoutTime(APIView):
    def post(self, request, supervisor_id, date):
        # Get the attendance record for the supervisor and date
        attendance_record = get_object_or_404(Attendance, supervisor_id=supervisor_id, date=date)

        clear_checkout = request.data.get('clear_checkout')
        checkout_time_str = request.data.get('checkout_time')

        try:
            if clear_checkout:
                # Clear the checkout time
                attendance_record.time_out = None
                attendance_record.out_status = None
                attendance_record.overtime = None
                attendance_record.total_working_hours = None
            else:
                # Set the new checkout time
                if checkout_time_str:
                    # Validate and convert checkout time
                    checkout_time = datetime.strptime(checkout_time_str, '%H:%M:%S').time()
                    attendance_record.time_out = checkout_time
                    attendance_record.out_status = 'Updated by MD'

                    # Calculate total working hours
                    time_in = datetime.strptime(str(attendance_record.time_in), '%H:%M:%S').time()
                    time_out = checkout_time

                    # Convert to datetime for calculation
                    today = datetime.today()
                    time_in_datetime = datetime.combine(today, time_in)
                    time_out_datetime = datetime.combine(today, time_out)

                    total_working_time = time_out_datetime - time_in_datetime
                    total_hours = total_working_time.seconds // 3600
                    total_minutes = (total_working_time.seconds % 3600) // 60
                    total_seconds = total_working_time.seconds % 60
                    attendance_record.total_working_hours = f"{total_hours:02}:{total_minutes:02}:{total_seconds:02}"

                    # Calculate overtime
                    shift_end_time = attendance_record.shift.shift_end_time
                    shift_end_datetime = datetime.combine(today, shift_end_time)
                    overtime_start_time = shift_end_datetime + timedelta(minutes=10)

                    if time_out_datetime > overtime_start_time:
                        overtime = time_out_datetime - overtime_start_time
                        overtime_hours = overtime.seconds // 3600
                        overtime_minutes = (overtime.seconds % 3600) // 60
                        overtime_seconds = overtime.seconds % 60
                        attendance_record.overtime = f"{overtime_hours:02}:{overtime_minutes:02}:{overtime_seconds:02}"
                    else:
                        attendance_record.overtime = "00:00:00"

            attendance_record.save()
            return Response({'message': 'Checkout time updated successfully.'}, status=status.HTTP_200_OK)
        except ValueError:
            return Response({'error': 'Invalid time format. Please use HH:MM:SS.'}, status=status.HTTP_400_BAD_REQUEST)


# views.py



class SupervisorWeeklyAttendanceChart(APIView):
    def get(self, request):
        user_id = request.session.get('user_id')  # Assuming employee ID is in the session
        
        # Get the current week offset from GET parameters (how many weeks to move forward/backward)
        week_offset = int(request.GET.get('week_offset', 0))
        
        today = datetime.now().date()
        start_of_week = today - timedelta(days=today.weekday()) + timedelta(weeks=week_offset)  # Adjust the week by the offset
        end_of_week = start_of_week + timedelta(days=6)

        # Initialize a dictionary to store total hours per day with the date
        weekly_hours = {}
        labels = []
        
        # Variables to store total hours for the week and total overtime
        total_hours = 0
        total_overtime = 0
        daily_working_hours = 8  # Standard working hours per day


        for i in range(6):  # Monday to Saturday
            day_date = start_of_week + timedelta(days=i)
            day_label = day_date.strftime('%a %b %d')  # Format: "Mon Sep 11"
            labels.append(day_label)
            weekly_hours[day_label] = 0  # Initialize the hours for each day as 0

        # Get all attendance entries for the selected week
        attendance_records = Attendance.objects.filter(
            manager__manager_id=user_id,
            date__range=[start_of_week, end_of_week]
        )


        # Get all approved leave requests for the selected week
        approved_leaves = SupervisorLeaveRequest.objects.filter(
            supervisor__supervisor_id=user_id,
            start_date__lte=end_of_week,
            end_date__gte=start_of_week,
            status='approved'
        )

        leave_days = set()
        for leave in approved_leaves:
            # Iterate through the leave days within the week
            leave_start = max(leave.start_date, start_of_week)
            leave_end = min(leave.end_date, end_of_week)
            for i in range((leave_end - leave_start).days + 1):
                leave_day = (leave_start + timedelta(days=i)).strftime('%a %b %d')
                leave_days.add(leave_day)

        # Calculate total working hours and overtime for each day
        for record in attendance_records:
            if record.time_in and record.time_out:
                # Convert time_in and time_out to datetime and calculate work duration
                work_duration = (datetime.combine(datetime.today(), record.time_out) - 
                                 datetime.combine(datetime.today(), record.time_in)).total_seconds() / 3600
                day_label = record.date.strftime('%a %b %d')  # Ensure record.date is also handled as date
                if day_label in weekly_hours:
                    weekly_hours[day_label] += work_duration

                # Calculate total hours and overtime
                total_hours += work_duration
                if work_duration > daily_working_hours:
                    total_overtime += work_duration - daily_working_hours

        total_hours = round(total_hours, 2)
        total_overtime = round(total_overtime, 2)

        # Get the current month
        current_month = start_of_week.strftime('%B')

        work_data = list(weekly_hours.values())
        leave_data = [daily_working_hours if label in leave_days else 0 for label in labels]


        # Prepare response data
        response_data = {
            'labels': labels,  # List of days with their respective dates
            'data': work_data,  # Corresponding hours worked
            'month': current_month,
            'leave_data': leave_data,  # Pass the leave data for each day
            'week_offset': week_offset,  # Pass the current week offset to the template for navigation
            'total_hours': total_hours,  # Total hours worked in the week
            'total_overtime': total_overtime,  # Total overtime worked in the week
        }

        # Serialize the data using the created serializer
        serializer = SupervisorWeeklyAttendanceChartSerializer(data=response_data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# views.py


class SupervisorMonthlyAttendanceChartAPIView(APIView):
    def get(self, request):
        user_id = request.session.get('user_id')  # Assuming supervisor ID is in the session

        # Get the current month offset from GET parameters
        month_offset = int(request.GET.get('month_offset', 0))

        today = datetime.now()
        current_month = today.month + month_offset
        current_year = today.year

        # Handle year overflow/underflow when adjusting months
        if current_month < 1:
            current_month += 12
            current_year -= 1
        elif current_month > 12:
            current_month -= 12
            current_year += 1

        # Determine the first and last day of the month
        start_of_month = datetime(current_year, current_month, 1)
        last_day = monthrange(current_year, current_month)[1]
        end_of_month = datetime(current_year, current_month, last_day)

        # Initialize data structures for the week calculations
        weekly_hours = [0, 0, 0, 0]  # For 4 weeks
        working_days_per_week = [0, 0, 0, 0]  # Number of working days per week
        week_labels = ["Week 1", "Week 2", "Week 3", "Week 4"]

        total_hours = 0
        total_overtime = 0
        daily_working_hours = 8  # Standard working hours per day

        # Get all attendance records for the selected month
        attendance_records = Attendance.objects.filter(
            supervisor__supervisor_id=user_id,
            date__range=[start_of_month, end_of_month]
        )

        # Calculate total working hours and overtime
        for record in attendance_records:
            if record.time_in and record.time_out:
                work_duration = datetime.combine(datetime.today(), record.time_out) - datetime.combine(datetime.today(), record.time_in)
                hours_worked = work_duration.total_seconds() / 3600  # Convert seconds to hours

                # Determine the week number (1-7 = Week 1, etc.)
                week_num = (record.date.day - 1) // 7
                if week_num < 4:  # Ensure we don't go beyond Week 4
                    weekly_hours[week_num] += hours_worked
                    working_days_per_week[week_num] += 1

                total_hours += hours_worked
                if hours_worked > daily_working_hours:
                    total_overtime += hours_worked - daily_working_hours

        total_hours = round(total_hours, 3)
        total_overtime = round(total_overtime, 3)

        # Calculate average hours per week
        average_hours_per_week = []
        for week_num in range(4):
            if working_days_per_week[week_num] > 0:
                avg_hours = weekly_hours[week_num] / working_days_per_week[week_num]
            else:
                avg_hours = 0
            average_hours_per_week.append(round(avg_hours, 2))

        # Zip the week labels with the average working hours
        week_avg_data = list(zip(week_labels, average_hours_per_week))

        # Get the month name for display
        current_month_name = start_of_month.strftime('%B')

        # Prepare the response data
        data = {
            'month': current_month_name,
            'week_avg_data': week_avg_data,
            'total_hours': total_hours,
            'total_overtime': total_overtime,
            'month_offset': month_offset
        }

        # Serialize the response data
        serializer = SupervisorMonthlyAttendanceChartSerializer(data)
        
        return Response(serializer.data)
    


####################################################

class AdminManagerAttendanceHistoryAPIView(APIView):
    def post(self, request, *args, **kwargs):
        manager_id = request.data.get('manager_id')
        from_date = request.data.get('from_date')
        to_date = request.data.get('to_date')

        # Filter attendance records where the manager is not null
        attendance_records = Attendance.objects.filter(manager__isnull=False)

        if manager_id:
            attendance_records = attendance_records.filter(manager__manager_id=manager_id)

        if from_date and to_date:
            attendance_records = attendance_records.filter(date__range=[from_date, to_date])

        if attendance_records.exists():
            serializer = ManagerAttendanceSerializer(attendance_records, many=True)
            return Response({
                "message": f"Found {attendance_records.count()} attendance record(s) for manager ID {manager_id} from {from_date} to {to_date}.",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "message": f"No attendance records found for Manager ID {manager_id} in the selected date range.",
                "data": []
            }, status=status.HTTP_404_NOT_FOUND)





class AdminSupervisorAttendanceHistoryAPIView(APIView):
    def post(self, request, *args, **kwargs):
        supervisor_id = request.data.get('supervisor_id')
        from_date = request.data.get('from_date')
        to_date = request.data.get('to_date')

        # Filter attendance records where the supervisor is not null
        attendance_records = Attendance.objects.filter(supervisor__isnull=False)

        if supervisor_id:
            attendance_records = attendance_records.filter(supervisor__supervisor_id=supervisor_id)

        if from_date and to_date:
            attendance_records = attendance_records.filter(date__range=[from_date, to_date])

        if attendance_records.exists():
            serializer = SupervisorAttendanceSerializer(attendance_records, many=True)
            return Response({
                "message": f"Found {attendance_records.count()} attendance record(s) for supervisor ID {supervisor_id} from {from_date} to {to_date}.",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "message": f"No attendance records found for Supervisor ID {supervisor_id} in the selected date range.",
                "data": []
            }, status=status.HTTP_404_NOT_FOUND)





class AdminEmployeeAttendanceHistoryAPIView(APIView):
    def post(self, request, *args, **kwargs):
        employee_id = request.data.get('employee_id')
        from_date = request.data.get('from_date')
        to_date = request.data.get('to_date')

        # Filter attendance records where the employee is not null
        attendance_records = Attendance.objects.filter(employee__isnull=False)

        if employee_id:
            attendance_records = attendance_records.filter(employee__employee_id=employee_id)

        if from_date and to_date:
            attendance_records = attendance_records.filter(date__range=[from_date, to_date])

        if attendance_records.exists():
            serializer = EmployeeAttendanceSerializer(attendance_records, many=True)
            return Response({
                "message": f"Found {attendance_records.count()} attendance record(s) for employee ID {employee_id} from {from_date} to {to_date}.",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "message": f"No attendance records found for Employee ID {employee_id} in the selected date range.",
                "data": []
            }, status=status.HTTP_404_NOT_FOUND)




class AdminManagerWeeklyChartAPIView(APIView):
    def get(self, request):
        manager_id = request.GET.get('manager_id')
        if not manager_id:
            raise ValidationError({'error': 'Manager ID is required.'})

        week_offset = int(request.GET.get('week_offset', 0))
        today = datetime.now().date()
        start_of_week = today - timedelta(days=today.weekday()) + timedelta(weeks=week_offset)
        end_of_week = start_of_week + timedelta(days=6)

        weekly_hours = {}
        labels = []
        total_hours = 0
        total_overtime = 0
        daily_working_hours = 8

        for i in range(6):
            day_date = start_of_week + timedelta(days=i)
            day_label = day_date.strftime('%a %b %d')
            labels.append(day_label)
            weekly_hours[day_label] = 0

        attendance_records = Attendance.objects.filter(
            manager__manager_id=manager_id,
            date__range=[start_of_week, end_of_week]
        )

        approved_leaves = ManagerLeaveRequest.objects.filter(
            manager__manager_id=manager_id,
            start_date__lte=end_of_week,
            end_date__gte=start_of_week,
            status='approved'
        )

        leave_days = set()
        for leave in approved_leaves:
            leave_start = max(leave.start_date, start_of_week)
            leave_end = min(leave.end_date, end_of_week)
            for i in range((leave_end - leave_start).days + 1):
                leave_day = (leave_start + timedelta(days=i)).strftime('%a %b %d')
                leave_days.add(leave_day)

        for record in attendance_records:
            if record.time_in and record.time_out:
                work_duration = (datetime.combine(datetime.today(), record.time_out) - 
                                 datetime.combine(datetime.today(), record.time_in)).total_seconds() / 3600
                day_label = record.date.strftime('%a %b %d')
                if day_label in weekly_hours:
                    weekly_hours[day_label] += work_duration
                total_hours += work_duration
                if work_duration > daily_working_hours:
                    total_overtime += work_duration - daily_working_hours

        work_data = list(weekly_hours.values())
        leave_data = [daily_working_hours if label in leave_days else 0 for label in labels]

        data = {
            'manager_id': manager_id,
            'labels': labels,
            'data': work_data,
            'leave_data': leave_data,
            'month': start_of_week.strftime('%B'),
            'week_offset': week_offset,
            'total_hours': round(total_hours, 2),
            'total_overtime': round(total_overtime, 2),
        }

        serializer = AdminManagerWeeklyChartSerializer(data)
        return Response(serializer.data)




class AdminSupervisorWeeklyChartAPI(APIView):
    def get(self, request):
        supervisor_id = request.GET.get('supervisor_id')
        week_offset = int(request.GET.get('week_offset', 0))
        
        if not supervisor_id:
            return Response({'error': 'Supervisor ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        today = datetime.now().date()
        start_of_week = today - timedelta(days=today.weekday()) + timedelta(weeks=week_offset)
        end_of_week = start_of_week + timedelta(days=6)
        
        daily_working_hours = 8
        weekly_hours = {}
        labels = []
        total_hours = 0
        total_overtime = 0
        leave_days = set()

        for i in range(6):  # Monday to Saturday
            day_date = start_of_week + timedelta(days=i)
            day_label = day_date.strftime('%a %b %d')
            labels.append(day_label)
            weekly_hours[day_label] = 0

        attendance_records = Attendance.objects.filter(
            supervisor__supervisor_id=supervisor_id,
            date__range=[start_of_week, end_of_week]
        )

        approved_leaves = SupervisorLeaveRequest.objects.filter(
            supervisor__supervisor_id=supervisor_id,
            start_date__lte=end_of_week,
            end_date__gte=start_of_week,
            status='approved'
        )

        for leave in approved_leaves:
            leave_start = max(leave.start_date, start_of_week)
            leave_end = min(leave.end_date, end_of_week)
            for i in range((leave_end - leave_start).days + 1):
                leave_day = (leave_start + timedelta(days=i)).strftime('%a %b %d')
                leave_days.add(leave_day)

        for record in attendance_records:
            if record.time_in and record.time_out:
                work_duration = (datetime.combine(datetime.today(), record.time_out) -
                                 datetime.combine(datetime.today(), record.time_in)).total_seconds() / 3600
                day_label = record.date.strftime('%a %b %d')
                if day_label in weekly_hours:
                    weekly_hours[day_label] += work_duration
                
                total_hours += work_duration
                if work_duration > daily_working_hours:
                    total_overtime += work_duration - daily_working_hours

        total_hours = round(total_hours, 2)
        total_overtime = round(total_overtime, 2)
        
        work_data = list(weekly_hours.values())
        leave_data = [daily_working_hours if label in leave_days else 0 for label in labels]
        
        return Response({
            'supervisor_id': supervisor_id,
            'labels': labels,
            'work_data': work_data,
            'leave_data': leave_data,
            'total_hours': total_hours,
            'total_overtime': total_overtime
        }, status=status.HTTP_200_OK)


# views.py


class AdminManagerMonthlyChartAPIView(APIView):
    def get(self, request):
        manager_id = request.GET.get('manager_id')
        month_offset = int(request.GET.get('month_offset', 0))

        # Check if manager_id is provided
        if not manager_id:
            return Response({'error': 'Manager ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        today = datetime.now().date()
        current_month = today.month + month_offset
        current_year = today.year

        if current_month < 1:
            current_month += 12
            current_year -= 1
        elif current_month > 12:
            current_month -= 12
            current_year += 1

        start_of_month = datetime(current_year, current_month, 1)
        last_day = monthrange(current_year, current_month)[1]
        end_of_month = datetime(current_year, current_month, last_day)

        weekly_hours = [0] * 4
        leave_weeks = [0] * 4
        week_labels = ["Week 1", "Week 2", "Week 3", "Week 4"]

        total_hours = 0
        total_overtime = 0
        daily_working_hours = 8

        attendance_records = Attendance.objects.filter(
            manager__manager_id=manager_id,
            date__range=[start_of_month.date(), end_of_month.date()]
        )

        for record in attendance_records:
            if record.time_in and record.time_out:
                work_duration = (datetime.combine(datetime.today(), record.time_out) - 
                                 datetime.combine(datetime.today(), record.time_in)).total_seconds() / 3600
                week_num = (record.date.day - 1) // 7
                if week_num < 4:
                    weekly_hours[week_num] += work_duration

                total_hours += work_duration
                if work_duration > daily_working_hours:
                    total_overtime += work_duration - daily_working_hours

        total_hours = round(total_hours, 2)
        total_overtime = round(total_overtime, 2)

        weekly_averages = [0] * 4
        for week_num in range(4):
            if leave_weeks[week_num] == 0 and weekly_hours[week_num] > 0:
                working_days = Attendance.objects.filter(
                    manager__manager_id=manager_id,
                    date__range=[start_of_month.date() + timedelta(weeks=week_num),
                                 start_of_month.date() + timedelta(weeks=week_num + 1) - timedelta(days=1)],
                    time_in__isnull=False,
                    time_out__isnull=False
                ).count()
                if working_days > 0:
                    weekly_averages[week_num] = round(weekly_hours[week_num] / working_days, 2)

        current_month_name = start_of_month.strftime('%B')

        data = {
            'manager_id': manager_id,
            'month': current_month_name,
            'total_hours': total_hours,
            'total_overtime': total_overtime,
            'weekly_hours': weekly_hours,
            'weekly_averages': weekly_averages,
            'week_labels': week_labels,
            'average_hours_per_week': total_hours / 4 if total_hours else 0
        }

        serializer = ManagerAttendanceSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)





class AdminSupervisorMonthlyChartAPIView(APIView):
    def get(self, request):
        supervisor_id = request.query_params.get('supervisor_id')
        if not supervisor_id:
            return Response({"error": "Supervisor ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        month_offset = int(request.query_params.get('month_offset', 0))
        
        # Get today's date and adjust the month by the offset
        today = datetime.now().date()
        current_month = today.month + month_offset
        current_year = today.year

        # Handle year overflow/underflow
        if current_month < 1:
            current_month += 12
            current_year -= 1
        elif current_month > 12:
            current_month -= 12
            current_year += 1

        # Determine the first and last day of the month
        start_of_month = datetime(current_year, current_month, 1)
        last_day = monthrange(current_year, current_month)[1]
        end_of_month = datetime(current_year, current_month, last_day)

        weekly_hours = [0] * 4  # For 4 weeks in a month
        leave_weeks = [0] * 4   # To track leave days per week
        week_labels = ["Week 1", "Week 2", "Week 3", "Week 4"]
        
        total_hours = 0
        total_overtime = 0
        daily_working_hours = 8  # Standard working hours per day

        attendance_records = Attendance.objects.filter(
            supervisor__supervisor_id=supervisor_id,
            date__range=[start_of_month.date(), end_of_month.date()]
        )

        for record in attendance_records:
            if record.time_in and record.time_out:
                work_duration = (datetime.combine(datetime.today(), record.time_out) - 
                                 datetime.combine(datetime.today(), record.time_in)).total_seconds() / 3600
                week_num = (record.date.day - 1) // 7
                if week_num < 4:
                    weekly_hours[week_num] += work_duration

                total_hours += work_duration
                if work_duration > daily_working_hours:
                    total_overtime += work_duration - daily_working_hours

        total_hours = round(total_hours, 2)
        total_overtime = round(total_overtime, 2)

        weekly_averages = [0] * 4
        for week_num in range(4):
            if leave_weeks[week_num] == 0 and weekly_hours[week_num] > 0:
                working_days = Attendance.objects.filter(
                    supervisor__supervisor_id=supervisor_id,
                    date__range=[start_of_month.date() + timedelta(weeks=week_num),
                                 start_of_month.date() + timedelta(weeks=week_num + 1) - timedelta(days=1)],
                    time_in__isnull=False,
                    time_out__isnull=False
                ).count()
                if working_days > 0:
                    weekly_averages[week_num] = round(weekly_hours[week_num] / working_days, 2)

        current_month_name = start_of_month.strftime('%B')

        work_data = weekly_hours

        response_data = {
            'labels': week_labels,
            'data': work_data,
            'month': current_month_name,
            'month_offset': month_offset,
            'total_hours': total_hours,
            'total_overtime': total_overtime,
            'supervisor_id': supervisor_id,
            'average_hours_per_week': total_hours / 4 if total_hours else 0,
            'weekly_averages': weekly_averages,
        }

        serializer = SupervisorMonthlyChartSerializer(response_data)
        return Response(serializer.data, status=status.HTTP_200_OK)


# views.py


class AdminEmployeeWeeklyChartAPI(APIView):
    def get(self, request, *args, **kwargs):
        employee_id = request.query_params.get('employee_id')
        week_offset = int(request.query_params.get('week_offset', 0))
        
        if not employee_id:
            return Response({'error': 'Employee ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        today = datetime.now().date()
        start_of_week = today - timedelta(days=today.weekday()) + timedelta(weeks=week_offset)
        end_of_week = start_of_week + timedelta(days=6)

        weekly_hours = {}
        labels = []
        total_hours = 0
        total_overtime = 0
        daily_working_hours = 8

        for i in range(6):
            day_date = start_of_week + timedelta(days=i)
            day_label = day_date.strftime('%a %b %d')
            labels.append(day_label)
            weekly_hours[day_label] = 0

        attendance_records = Attendance.objects.filter(
            employee__employee_id=employee_id,
            date__range=[start_of_week, end_of_week]
        )

        approved_leaves = LeaveRequest.objects.filter(
            employee__employee_id=employee_id,
            status='approved',
            start_date__lte=end_of_week,
            end_date__gte=start_of_week
        )

        leave_days = set()
        for leave in approved_leaves:
            leave_start = max(leave.start_date, start_of_week)
            leave_end = min(leave.end_date, end_of_week)
            for i in range((leave_end - leave_start).days + 1):
                leave_day = (leave_start + timedelta(days=i)).strftime('%a %b %d')
                leave_days.add(leave_day)

        for record in attendance_records:
            if record.time_in and record.time_out:
                work_duration = (datetime.combine(datetime.today(), record.time_out) - 
                                 datetime.combine(datetime.today(), record.time_in)).total_seconds() / 3600
                day_label = record.date.strftime('%a %b %d')
                if day_label in weekly_hours:
                    weekly_hours[day_label] += work_duration

                total_hours += work_duration
                if work_duration > daily_working_hours:
                    total_overtime += work_duration - daily_working_hours

        total_hours = round(total_hours, 2)
        total_overtime = round(total_overtime, 2)

        current_month = start_of_week.strftime('%B')

        work_data = list(weekly_hours.values())
        leave_data = [daily_working_hours if label in leave_days else 0 for label in labels]

        weekly_data = [
            {
                'day_label': label,
                'hours_worked': work_data[i],
                'overtime_hours': leave_data[i] if leave_data[i] == 0 else 0,
                'is_leave': label in leave_days
            }
            for i, label in enumerate(labels)
        ]

        response_data = {
            'employee_id': employee_id,
            'total_hours': total_hours,
            'total_overtime': total_overtime,
            'weekly_data': weekly_data,
            'month': current_month,
            'week_offset': week_offset
        }

        return Response(response_data, status=status.HTTP_200_OK)




class AdminEmployeeMonthlyChartAPI(APIView):
    def get(self, request, *args, **kwargs):
        employee_id = request.query_params.get('employee_id')
        if not employee_id:
            return Response({'error': 'Employee ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        month_offset = int(request.query_params.get('month_offset', 0))
        today = datetime.now().date()
        current_month = today.month + month_offset
        current_year = today.year

        if current_month < 1:
            current_month += 12
            current_year -= 1
        elif current_month > 12:
            current_month -= 12
            current_year += 1

        start_of_month = datetime(current_year, current_month, 1)
        last_day = monthrange(current_year, current_month)[1]
        end_of_month = datetime(current_year, current_month, last_day)

        weekly_hours = [0] * 4
        leave_weeks = [0] * 4
        week_labels = ["Week 1", "Week 2", "Week 3", "Week 4"]
        total_hours = 0
        total_overtime = 0
        daily_working_hours = 8

        attendance_records = Attendance.objects.filter(
            employee__employee_id=employee_id,
            date__range=[start_of_month.date(), end_of_month.date()]
        )

        for record in attendance_records:
            if record.time_in and record.time_out:
                work_duration = (datetime.combine(datetime.today(), record.time_out) - 
                                 datetime.combine(datetime.today(), record.time_in)).total_seconds() / 3600
                week_num = (record.date.day - 1) // 7
                if week_num < 4:
                    weekly_hours[week_num] += work_duration

                total_hours += work_duration
                if work_duration > daily_working_hours:
                    total_overtime += work_duration - daily_working_hours

        total_hours = round(total_hours, 2)
        total_overtime = round(total_overtime, 2)

        weekly_averages = [0] * 4
        for week_num in range(4):
            if leave_weeks[week_num] == 0 and weekly_hours[week_num] > 0:
                working_days = Attendance.objects.filter(
                    employee__employee_id=employee_id,
                    date__range=[start_of_month.date() + timedelta(weeks=week_num),
                                 start_of_month.date() + timedelta(weeks=week_num + 1) - timedelta(days=1)],
                    time_in__isnull=False,
                    time_out__isnull=False
                ).count()
                if working_days > 0:
                    weekly_averages[week_num] = round(weekly_hours[week_num] / working_days, 2)

        current_month_name = start_of_month.strftime('%B')

        chart_data = {
            'labels': week_labels,
            'data': weekly_hours,
            'month': current_month_name,
            'month_offset': month_offset,
            'total_hours': total_hours,
            'total_overtime': total_overtime,
            'employee_id': employee_id,
            'average_hours_per_week': total_hours / 4 if total_hours else 0,
            'weekly_averages': weekly_averages
        }

        serializer = EmployeeMonthlyChartSerializer(chart_data)
        return Response(serializer.data, status=status.HTTP_200_OK)


#Checkout time reset part functions


class EmployeeRequestCheckOutResetAPI(APIView):
    def post(self, request, *args, **kwargs):
        user_id = request.session.get('user_id')
        today = timezone.now().date()

        if not user_id:
            return Response({'error': 'User not authenticated.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            employee = Employee.objects.get(employee_id=user_id)
        except Employee.DoesNotExist:
            return Response({'error': 'Employee not found.'}, status=status.HTTP_404_NOT_FOUND)

        last_attendance = Attendance.objects.filter(
            employee=employee,
            date=today,
            time_in__isnull=False
        ).first()

        if not last_attendance:
            return Response({'error': "You can't reset the checkout time before checkin."}, status=status.HTTP_400_BAD_REQUEST)

        existing_request = ResetRequest.objects.filter(
            employee=employee,
            date=today,
            status='Pending'
        ).exists()

        if existing_request:
            return Response({'error': "You have already sent the request. Please wait until the checkout time is reset."}, 
                            status=status.HTTP_400_BAD_REQUEST)

        request_type = request.data.get('request_type')
        request_description = request.data.get('request_description')

        if not request_type or not request_description:
            return Response({'error': 'Request type and description are required.'}, status=status.HTTP_400_BAD_REQUEST)

        reset_request = ResetRequest(
            employee=employee,
            date=today,
            request_type=request_type,
            request_description=request_description,
            status='Pending',
            created_at=timezone.now()
        )
        reset_request.save()

        serializer = ResetRequestSerializer(reset_request)

        return Response({'message': 'Your reset request has been submitted successfully.', 'reset_request': serializer.data},
                        status=status.HTTP_201_CREATED)




class MdManagerAttendanceHistoryAPI(APIView):
    def post(self, request, *args, **kwargs):
        # Get filter parameters from the request
        manager_id = request.data.get('manager_id')
        from_date = request.data.get('from_date')
        to_date = request.data.get('to_date')

        # Filter attendance records based on manager ID and date range
        attendance_records = Attendance.objects.filter(manager__isnull=False)

        if manager_id:
            attendance_records = attendance_records.filter(manager__manager_id=manager_id)

        if from_date and to_date:
            attendance_records = attendance_records.filter(date__range=[from_date, to_date])

        # Serialize the filtered attendance records
        serializer = AttendanceSerializer(attendance_records, many=True)

        # Return response with attendance records data
        if attendance_records.exists():
            return Response({
                'message': f"Found {attendance_records.count()} attendance record(s).",
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'message': "No attendance records found for the given filters.",
                'data': []
            }, status=status.HTTP_404_NOT_FOUND)




class MdSupervisorAttendanceHistoryAPI(APIView):
    def post(self, request, *args, **kwargs):
        # Get filter parameters from the request
        supervisor_id = request.data.get('supervisor_id')
        from_date = request.data.get('from_date')
        to_date = request.data.get('to_date')

        # Filter attendance records based on supervisor ID and date range
        attendance_records = Attendance.objects.filter(supervisor__isnull=False)

        if supervisor_id:
            attendance_records = attendance_records.filter(supervisor__supervisor_id=supervisor_id)

        if from_date and to_date:
            attendance_records = attendance_records.filter(date__range=[from_date, to_date])

        # Serialize the filtered attendance records
        serializer = AttendanceSerializer(attendance_records, many=True)

        # Return response with attendance records data
        if attendance_records.exists():
            return Response({
                'message': f"Found {attendance_records.count()} attendance record(s).",
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'message': "No attendance records found for the given filters.",
                'data': []
            }, status=status.HTTP_404_NOT_FOUND)




class MdEmployeeAttendanceHistoryAPI(APIView):
    def post(self, request, *args, **kwargs):
        # Get filter parameters from the request
        employee_id = request.data.get('employee_id')
        from_date = request.data.get('from_date')
        to_date = request.data.get('to_date')

        # Filter attendance records based on employee ID and date range
        attendance_records = Attendance.objects.filter(employee__isnull=False)

        if employee_id:
            attendance_records = attendance_records.filter(employee__employee_id=employee_id)

        if from_date and to_date:
            attendance_records = attendance_records.filter(date__range=[from_date, to_date])

        # Serialize the filtered attendance records
        serializer = AttendanceSerializer(attendance_records, many=True)

        # Return response with attendance records data
        if attendance_records.exists():
            return Response({
                'message': f"Found {attendance_records.count()} attendance record(s).",
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'message': "No attendance records found for the given filters.",
                'data': []
            }, status=status.HTTP_404_NOT_FOUND)




@api_view(['GET'])
def md_manager_weekly_chart_api(request):
    manager_id = request.GET.get('manager_id')
    week_offset = int(request.GET.get('week_offset', 0))

    if not manager_id:
        return Response({'error': 'Manager ID is required.'}, status=400)

    today = datetime.now().date()
    start_of_week = today - timedelta(days=today.weekday()) + timedelta(weeks=week_offset)
    end_of_week = start_of_week + timedelta(days=6)

    weekly_hours = {}
    labels = []
    total_hours = 0
    total_overtime = 0
    daily_working_hours = 8

    for i in range(7):
        day_date = start_of_week + timedelta(days=i)
        day_label = day_date.strftime('%a %b %d')
        labels.append(day_label)
        weekly_hours[day_label] = 0

    attendance_records = Attendance.objects.filter(
        manager__manager_id=manager_id,
        date__range=[start_of_week, end_of_week]
    )

    approved_leaves = ManagerLeaveRequest.objects.filter(
        manager__manager_id=manager_id,
        start_date__lte=end_of_week,
        end_date__gte=start_of_week,
        status='approved'
    )

    leave_days = set()
    for leave in approved_leaves:
        leave_start = max(leave.start_date, start_of_week)
        leave_end = min(leave.end_date, end_of_week)
        for i in range((leave_end - leave_start).days + 1):
            leave_day = (leave_start + timedelta(days=i)).strftime('%a %b %d')
            leave_days.add(leave_day)

    for record in attendance_records:
        if record.time_in and record.time_out:
            work_duration = (datetime.combine(datetime.today(), record.time_out) - 
                             datetime.combine(datetime.today(), record.time_in))
            hours_worked = work_duration.total_seconds() / 3600

            day_label = record.date.strftime('%a %b %d')
            if day_label in weekly_hours:
                weekly_hours[day_label] += hours_worked

            total_hours += hours_worked
            if hours_worked > daily_working_hours:
                total_overtime += hours_worked - daily_working_hours

    total_hours = round(total_hours, 2)
    total_overtime = round(total_overtime, 2)
    current_month = start_of_week.strftime('%B')

    work_data = list(weekly_hours.values())
    leave_data = [daily_working_hours if label in leave_days else 0 for label in labels]

    response_data = {
        'manager_id': manager_id,
        'labels': labels,
        'data': work_data,
        'leave_data': leave_data,
        'month': current_month,
        'week_offset': week_offset,
        'total_hours': total_hours,
        'total_overtime': total_overtime,
    }

    return Response(response_data)



# views.py



class MdSupervisorWeeklyChartAPI(APIView):
    def get(self, request):
        supervisor_id = request.GET.get('supervisor_id')
        if not supervisor_id:
            return Response({'error': 'supervisor ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        week_offset = int(request.GET.get('week_offset', 0))
        
        today = datetime.now().date()
        start_of_week = today - timedelta(days=today.weekday()) + timedelta(weeks=week_offset)
        end_of_week = start_of_week + timedelta(days=6)

        weekly_hours = {}
        labels = []

        total_hours = 0
        total_overtime = 0
        daily_working_hours = 8

        for i in range(7):
            day_date = start_of_week + timedelta(days=i)
            day_label = day_date.strftime('%a %b %d')
            labels.append(day_label)
            weekly_hours[day_label] = 0

        attendance_records = Attendance.objects.filter(
            supervisor__supervisor_id=supervisor_id,
            date__range=[start_of_week, end_of_week]
        )

        approved_leaves = SupervisorLeaveRequest.objects.filter(
            supervisor__supervisor_id=supervisor_id,
            start_date__lte=end_of_week,
            end_date__gte=start_of_week,
            status='approved'
        )

        leave_days = set()
        for leave in approved_leaves:
            leave_start = max(leave.start_date, start_of_week)
            leave_end = min(leave.end_date, end_of_week)
            for i in range((leave_end - leave_start).days + 1):
                leave_day = (leave_start + timedelta(days=i)).strftime('%a %b %d')
                leave_days.add(leave_day)

        for record in attendance_records:
            if record.time_in and record.time_out:
                work_duration = (datetime.combine(datetime.today(), record.time_out) -
                                 datetime.combine(datetime.today(), record.time_in))
                hours_worked = work_duration.total_seconds() / 3600

                day_label = record.date.strftime('%a %b %d')
                if day_label in weekly_hours:
                    weekly_hours[day_label] += hours_worked

                total_hours += hours_worked
                if hours_worked > daily_working_hours:
                    total_overtime += hours_worked - daily_working_hours

        total_hours = round(total_hours, 2)
        total_overtime = round(total_overtime, 2)

        current_month = start_of_week.strftime('%B')

        work_data = list(weekly_hours.values())
        leave_data = [daily_working_hours if label in leave_days else 0 for label in labels]

        data = {
            'supervisor_id': supervisor_id,
            'labels': labels,
            'data': work_data,
            'leave_data': leave_data,
            'month': current_month,
            'week_offset': week_offset,
            'total_hours': total_hours,
            'total_overtime': total_overtime,
        }

        serializer = SupervisorWeeklyChartSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)






class ManagerMonthlyChartAPI(APIView):

    def get(self, request, *args, **kwargs):
        # Retrieve manager ID and month offset
        manager_id = request.GET.get('manager_id')
        if not manager_id:
            return Response({'error': 'Manager ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Get the current month offset from GET parameters (default is 0)
        month_offset = int(request.GET.get('month_offset', 0))
        
        # Get today's date and adjust the month by the offset
        today = datetime.now().date()
        current_month = today.month + month_offset
        current_year = today.year

        # Handle year overflow/underflow
        if current_month < 1:
            current_month += 12
            current_year -= 1
        elif current_month > 12:
            current_month -= 12
            current_year += 1

        # Determine the first and last day of the month
        start_of_month = datetime(current_year, current_month, 1)
        last_day = monthrange(current_year, current_month)[1]
        end_of_month = datetime(current_year, current_month, last_day)

        # Initialize variables
        weekly_hours = [0] * 4  # For 4 weeks in a month
        leave_weeks = [0] * 4   # To track leave days per week
        week_labels = ["Week 1", "Week 2", "Week 3", "Week 4"]
        total_hours = 0
        total_overtime = 0
        daily_working_hours = 8  # Standard working hours per day

        # Get all attendance entries for the selected month
        attendance_records = Attendance.objects.filter(
            manager__manager_id=manager_id,
            date__range=[start_of_month.date(), end_of_month.date()]
        )
        
        # Calculate total working hours and overtime for each week
        for record in attendance_records:
            if record.time_in and record.time_out:
                work_duration = (datetime.combine(datetime.today(), record.time_out) - 
                                 datetime.combine(datetime.today(), record.time_in)).total_seconds() / 3600
                week_num = (record.date.day - 1) // 7
                if week_num < 4:
                    weekly_hours[week_num] += work_duration

                total_hours += work_duration
                if work_duration > daily_working_hours:
                    total_overtime += work_duration - daily_working_hours

        total_hours = round(total_hours, 2)
        total_overtime = round(total_overtime, 2)

        # Calculate weekly averages
        weekly_averages = [0] * 4
        for week_num in range(4):
            if leave_weeks[week_num] == 0 and weekly_hours[week_num] > 0:
                # Count the working days in that week
                working_days = Attendance.objects.filter(
                    manager__manager_id=manager_id,
                    date__range=[start_of_month.date() + timedelta(weeks=week_num),
                                 start_of_month.date() + timedelta(weeks=week_num + 1) - timedelta(days=1)],
                    time_in__isnull=False,
                    time_out__isnull=False
                ).count()
                if working_days > 0:
                    weekly_averages[week_num] = round(weekly_hours[week_num] / working_days, 2)

        current_month_name = start_of_month.strftime('%B')

        # Prepare data for the chart
        work_data = weekly_hours

        # Prepare response data
        response_data = {
            'labels': week_labels,
            'data': work_data,
            'month': current_month_name,
            'month_offset': month_offset,
            'total_hours': total_hours,
            'total_overtime': total_overtime,
            'manager_id': manager_id,
            'average_hours_per_week': total_hours / 4 if total_hours else 0,
            'weekly_averages': weekly_averages
        }

        # Serialize data
        serializer = ManagerMonthlyChartSerializer(response_data)

        return Response(serializer.data, status=status.HTTP_200_OK)





class SupervisorMonthlyChartAPI(APIView):
    def get(self, request):
        supervisor_id = request.GET.get('supervisor_id')
        if not supervisor_id:
            return Response({'error': 'supervisor ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        month_offset = int(request.GET.get('month_offset', 0))
        
        # Get today's date and adjust the month by the offset
        today = datetime.now().date()
        current_month = today.month + month_offset
        current_year = today.year

        # Handle year overflow/underflow
        if current_month < 1:
            current_month += 12
            current_year -= 1
        elif current_month > 12:
            current_month -= 12
            current_year += 1

        # Determine the first and last day of the month
        start_of_month = datetime(current_year, current_month, 1)
        last_day = monthrange(current_year, current_month)[1]
        end_of_month = datetime(current_year, current_month, last_day)

        # Initialize weekly data
        weekly_hours = [0] * 4  # For 4 weeks in a month
        leave_weeks = [0] * 4   # To track leave days per week
        week_labels = ["Week 1", "Week 2", "Week 3", "Week 4"]
        
        # Variables for total hours and overtime
        total_hours = 0
        total_overtime = 0
        daily_working_hours = 8  # Standard working hours per day

        # Get all attendance entries for the selected month
        attendance_records = Attendance.objects.filter(
            supervisor__supervisor_id=supervisor_id,
            date__range=[start_of_month.date(), end_of_month.date()]
        )
        
        # Calculate total working hours and overtime for each week
        for record in attendance_records:
            if record.time_in and record.time_out:
                work_duration = (datetime.combine(datetime.today(), record.time_out) - 
                                 datetime.combine(datetime.today(), record.time_in)).total_seconds() / 3600
                week_num = (record.date.day - 1) // 7
                if week_num < 4:
                    weekly_hours[week_num] += work_duration

                total_hours += work_duration
                if work_duration > daily_working_hours:
                    total_overtime += work_duration - daily_working_hours

        total_hours = round(total_hours, 2)
        total_overtime = round(total_overtime, 2)

        # Calculate weekly averages
        weekly_averages = [0] * 4
        for week_num in range(4):
            if leave_weeks[week_num] == 0 and weekly_hours[week_num] > 0:
                working_days = Attendance.objects.filter(
                    supervisor__supervisor_id=supervisor_id,
                    date__range=[start_of_month.date() + timedelta(weeks=week_num),
                                 start_of_month.date() + timedelta(weeks=week_num + 1) - timedelta(days=1)],
                    time_in__isnull=False,
                    time_out__isnull=False
                ).count()
                if working_days > 0:
                    weekly_averages[week_num] = round(weekly_hours[week_num] / working_days, 2)

        # Get the month name for display
        current_month_name = start_of_month.strftime('%B')
        
        # Prepare data for the response
        data = {
            'week_labels': week_labels,
            'work_data': weekly_hours,
            'month': current_month_name,
            'month_offset': month_offset,
            'total_hours': total_hours,
            'total_overtime': total_overtime,
            'supervisor_id': supervisor_id,
            'average_hours_per_week': total_hours / 4 if total_hours else 0,
            'weekly_averages': weekly_averages
        }

        # Return the response with serialized data
        serializer = SupervisorMonthlyChartSerializer(data)
        return Response(serializer.data)



# views.py



@api_view(['GET', 'POST'])
def md_employee_weekly_chart_api(request):
    if request.method == 'POST':
        employee_id = request.data.get('employee_id')
    else:
        employee_id = request.GET.get('employee_id')

    if not employee_id:
        return Response({'error': 'Employee ID is required.'}, status=400)
    
    week_offset = int(request.GET.get('week_offset', 0))
    today = datetime.now().date()
    start_of_week = today - timedelta(days=today.weekday()) + timedelta(weeks=week_offset)
    end_of_week = start_of_week + timedelta(days=6)

    weekly_hours = {}
    labels = []
    
    total_hours = 0
    total_overtime = 0
    daily_working_hours = 8  # Standard working hours per day

    for i in range(7):  # Loop to include Sunday as well
        day_date = start_of_week + timedelta(days=i)
        day_label = day_date.strftime('%a %b %d')
        labels.append(day_label)
        weekly_hours[day_label] = 0  # Initialize the hours for each day as 0

    attendance_records = Attendance.objects.filter(
        employee__employee_id=employee_id,  
        date__range=[start_of_week, end_of_week]
    )

    approved_leaves = LeaveRequest.objects.filter(
        employee__employee_id=employee_id,
        status='approved',
        start_date__lte=end_of_week,
        end_date__gte=start_of_week
    )

    leave_days = set()
    for leave in approved_leaves:
        leave_start = max(leave.start_date, start_of_week)
        leave_end = min(leave.end_date, end_of_week)
        for i in range((leave_end - leave_start).days + 1):
            leave_day = (leave_start + timedelta(days=i)).strftime('%a %b %d')
            leave_days.add(leave_day)

    for record in attendance_records:
        if record.time_in and record.time_out:
            work_duration = (datetime.combine(datetime.today(), record.time_out) - 
                             datetime.combine(datetime.today(), record.time_in)).total_seconds() / 3600
            day_label = record.date.strftime('%a %b %d')
            if day_label in weekly_hours:
                weekly_hours[day_label] += work_duration

            total_hours += work_duration
            if work_duration > daily_working_hours:
                total_overtime += work_duration - daily_working_hours

    total_hours = round(total_hours, 2)
    total_overtime = round(total_overtime, 2)

    current_month = start_of_week.strftime('%B')

    work_data = list(weekly_hours.values())
    leave_data = [daily_working_hours if label in leave_days else 0 for label in labels]

    data = {
        'labels': labels,
        'data': work_data,
        'leave_data': leave_data,
        'month': current_month,
        'week_offset': week_offset,
        'total_hours': total_hours,
        'total_overtime': total_overtime,
        'employee_id': employee_id,
    }

    serializer = EmployeeWeeklyChartSerializer(data)
    return Response(serializer.data)



class MdEmployeeMonthlyChartAPIView(APIView):
    
    def get(self, request):
        # Get parameters
        employee_id = request.GET.get('employee_id')
        month_offset = int(request.GET.get('month_offset', 0))
        
        # Check if employee_id is provided
        if not employee_id:
            return Response({'error': 'Employee ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Get today's date and adjust the month by the offset
        today = datetime.now().date()
        current_month = today.month + month_offset
        current_year = today.year

        # Handle year overflow/underflow
        if current_month < 1:
            current_month += 12
            current_year -= 1
        elif current_month > 12:
            current_month -= 12
            current_year += 1

        # Determine the first and last day of the month
        start_of_month = datetime(current_year, current_month, 1)
        last_day = monthrange(current_year, current_month)[1]
        end_of_month = datetime(current_year, current_month, last_day)

        # Initialize data structures to store weekly hours and leave information
        weekly_hours = [0, 0, 0, 0]  # For 4 weeks
        leave_weeks = [0, 0, 0, 0]  # To track the number of working days per week
        week_labels = ["Week 1", "Week 2", "Week 3", "Week 4"]  # Week labels
        
        total_hours = 0
        total_overtime = 0
        daily_working_hours = 8  # Standard working hours per day

        # Get attendance records for the employee during the selected month
        attendance_records = Attendance.objects.filter(
            employee__employee_id=employee_id,
            date__range=[start_of_month.date(), end_of_month.date()]
        )

        # Calculate total working hours and overtime for each week
        for record in attendance_records:
            if record.time_in and record.time_out:
                work_duration = (datetime.combine(datetime.today(), record.time_out) - 
                                 datetime.combine(datetime.today(), record.time_in)).total_seconds() / 3600
                week_num = (record.date.day - 1) // 7
                if week_num < 4:
                    weekly_hours[week_num] += work_duration

                total_hours += work_duration
                if work_duration > daily_working_hours:
                    total_overtime += work_duration - daily_working_hours
        
        total_hours = round(total_hours, 2)
        total_overtime = round(total_overtime, 2)

        # Calculate weekly averages
        weekly_averages = [0] * 4
        for week_num in range(4):
            if leave_weeks[week_num] == 0 and weekly_hours[week_num] > 0:
                # Count the working days in that week
                working_days = Attendance.objects.filter(
                    employee__employee_id=employee_id,
                    date__range=[start_of_month.date() + timedelta(weeks=week_num),
                                 start_of_month.date() + timedelta(weeks=week_num + 1) - timedelta(days=1)],
                    time_in__isnull=False,
                    time_out__isnull=False
                ).count()
                if working_days > 0:
                    weekly_averages[week_num] = round(weekly_hours[week_num] / working_days, 2)

        # Get the month name for display
        current_month_name = start_of_month.strftime('%B')

        # Prepare data for the chart
        work_data = weekly_hours

        # Prepare the response data
        data = {
            'employee_id': employee_id,
            'month_offset': month_offset,
            'total_hours': total_hours,
            'total_overtime': total_overtime,
            'average_hours_per_week': total_hours / 4 if total_hours else 0,
            'weekly_averages': weekly_averages,
            'labels': week_labels,
            'data': work_data,
            'month': current_month_name,
        }

        # Serialize and return the response
        serializer = EmployeeMonthlyChartSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from datetime import datetime, timedelta
from calendar import monthrange
from .models import Attendance  # Assuming LeaveRequest is in a leave app


class EmployeeWeeklyAttendanceChartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.user.id  # Assuming user is authenticated
        week_offset = int(request.query_params.get('week_offset', 0))

        today = datetime.now().date()
        start_of_week = today - timedelta(days=today.weekday()) + timedelta(weeks=week_offset)
        end_of_week = start_of_week + timedelta(days=6)

        labels = []
        weekly_hours = {}
        total_hours = 0
        total_overtime = 0
        daily_working_hours = 8

        for i in range(7):
            day_date = start_of_week + timedelta(days=i)
            day_label = day_date.strftime('%a %b %d')
            labels.append(day_label)
            weekly_hours[day_label] = 0

        attendance_records = Attendance.objects.filter(
            employee__employee_id=user_id,
            date__range=[start_of_week, end_of_week]
        )
        permission_records = PermissionHour.objects.filter(
            employee__employee_id=user_id,
            date__range=[start_of_week, end_of_week],
            status='Approved'
        )
        approved_leaves = LeaveRequest.objects.filter(
            employee__employee_id=user_id,
            status='approved',
            start_date__lte=end_of_week,
            end_date__gte=start_of_week
        )

        leave_days = set()
        for leave in approved_leaves:
            leave_start = max(leave.start_date, start_of_week)
            leave_end = min(leave.end_date, end_of_week)
            for i in range((leave_end - leave_start).days + 1):
                leave_day = (leave_start + timedelta(days=i)).strftime('%a %b %d')
                leave_days.add(leave_day)

        for record in attendance_records:
            if record.time_in and record.time_out:
                work_duration = (datetime.combine(datetime.today(), record.time_out) - 
                                 datetime.combine(datetime.today(), record.time_in)).total_seconds() / 3600
                day_label = record.date.strftime('%a %b %d')
                if day_label in weekly_hours:
                    weekly_hours[day_label] += work_duration

                total_hours += work_duration
                if work_duration > daily_working_hours:
                    total_overtime += work_duration - daily_working_hours

        permission_hours = {label: 0 for label in labels}
        for permission in permission_records:
            permission_duration = (
                datetime.combine(datetime.today(), permission.end_time) - 
                datetime.combine(datetime.today(), permission.start_time)
            ).total_seconds() / 3600
            day_label = permission.date.strftime('%a %b %d')
            if day_label in permission_hours:
                permission_hours[day_label] += permission_duration

        work_data = list(weekly_hours.values())
        permission_data = list(permission_hours.values())
        leave_data = [daily_working_hours if label in leave_days else 0 for label in labels]

        return Response({
            'labels': labels,
            'work_data': work_data,
            'permission_data': permission_data,
            'leave_data': leave_data,
            'total_hours': round(total_hours, 2),
            'total_overtime': round(total_overtime, 2)
        })


class EmployeeMonthlyAttendanceChartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.user.id
        month_offset = int(request.query_params.get('month_offset', 0))

        today = datetime.now()
        current_month = today.month + month_offset
        current_year = today.year

        if current_month < 1:
            current_month += 12
            current_year -= 1
        elif current_month > 12:
            current_month -= 12
            current_year += 1

        start_of_month = datetime(current_year, current_month, 1)
        last_day = monthrange(current_year, current_month)[1]
        end_of_month = datetime(current_year, current_month, last_day)

        labels = [f"Week {i + 1}" for i in range(4)]
        weekly_hours = [0, 0, 0, 0]
        permission_hours = [0, 0, 0, 0]
        leave_days = [0, 0, 0, 0]

        total_hours = 0
        total_overtime = 0
        daily_working_hours = 8

        attendance_records = Attendance.objects.filter(
            employee__employee_id=user_id,
            date__range=[start_of_month, end_of_month]
        )
        permission_records = PermissionHour.objects.filter(
            employee__employee_id=user_id,
            date__range=[start_of_month, end_of_month],
            status='Approved'
        )
        approved_leaves = LeaveRequest.objects.filter(
            employee__employee_id=user_id,
            status='approved',
            start_date__lte=end_of_month,
            end_date__gte=start_of_month
        )

        for record in attendance_records:
            if record.time_in and record.time_out:
                work_duration = (datetime.combine(datetime.today(), record.time_out) - 
                                 datetime.combine(datetime.today(), record.time_in)).total_seconds() / 3600
                week_num = (record.date.day - 1) // 7
                if week_num < 4:
                    weekly_hours[week_num] += work_duration
                total_hours += work_duration
                if work_duration > daily_working_hours:
                    total_overtime += work_duration - daily_working_hours

        for permission in permission_records:
            week_num = (permission.date.day - 1) // 7
            permission_duration = (
                datetime.combine(datetime.today(), permission.end_time) - 
                datetime.combine(datetime.today(), permission.start_time)
            ).total_seconds() / 3600
            if week_num < 4:
                permission_hours[week_num] += permission_duration

        for leave in approved_leaves:
            leave_start = max(leave.start_date, start_of_month.date())
            leave_end = min(leave.end_date, end_of_month.date())
            while leave_start <= leave_end:
                week_num = (leave_start.day - 1) // 7
                if week_num < 4:
                    leave_days[week_num] += 1
                leave_start += timedelta(days=1)

        return Response({
            'labels': labels,
            'work_data': weekly_hours,
            'permission_data': permission_hours,
            'leave_data': leave_days,
            'total_hours': round(total_hours, 2),
            'total_overtime': round(total_overtime, 2)
        })


class EmployeeYearlyAttendanceChartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.user.id
        year_offset = int(request.query_params.get('year_offset', 0))
        today = datetime.now()
        current_year = today.year + year_offset

        monthly_hours = [0] * 12
        monthly_permission_hours = [0] * 12
        monthly_leave_days = [0] * 12
        month_labels = [datetime(current_year, i + 1, 1).strftime('%B') for i in range(12)]

        total_hours = 0
        total_overtime = 0
        daily_working_hours = 8

        attendance_records = Attendance.objects.filter(
            employee__employee_id=user_id,
            date__year=current_year
        )
        permission_records = PermissionHour.objects.filter(
            employee__employee_id=user_id,
            date__year=current_year,
            status='Approved'
        )
        approved_leaves = LeaveRequest.objects.filter(
            employee__employee_id=user_id,
            status='approved',
            start_date__year=current_year
        )

        for record in attendance_records:
            if record.time_in and record.time_out:
                work_duration = datetime.combine(datetime.today(), record.time_out) - datetime.combine(datetime.today(), record.time_in)
                hours_worked = work_duration.total_seconds() / 3600
                month_num = record.date.month - 1

                monthly_hours[month_num] += hours_worked
                total_hours += hours_worked
                if hours_worked > daily_working_hours:
                    total_overtime += hours_worked - daily_working_hours

        for permission in permission_records:
            month_num = permission.date.month - 1
            permission_duration = (
                datetime.combine(datetime.today(), permission.end_time) - 
                datetime.combine(datetime.today(), permission.start_time)
            ).total_seconds() / 3600
            monthly_permission_hours[month_num] += permission_duration

        for leave in approved_leaves:
            leave_start = leave.start_date
            leave_end = leave.end_date
            while leave_start <= leave_end:
                if leave_start.year == current_year:
                    month_num = leave_start.month - 1
                    monthly_leave_days[month_num] += 1
                leave_start += timedelta(days=1)

        return Response({
            'labels': month_labels,
            'monthly_hours': monthly_hours,
            'monthly_permission_hours': monthly_permission_hours,
            'monthly_leave_days': monthly_leave_days,
            'total_hours': round(total_hours, 2),
            'total_overtime': round(total_overtime, 2)
        })


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import PermissionHour, Employee
from .serializers import PermissionHourSerializer
from django.core.mail import send_mail

class RequestPermissionHourView(APIView):
    """
    API view to handle permission hour requests.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        employee_id = request.user.employee.employee_id  # Assuming a User-Employee relationship
        data = request.data

        # Validate start_time and end_time
        if data['start_time'] >= data['end_time']:
            return Response({'error': 'Start time must be before end time.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            employee = Employee.objects.get(employee_id=employee_id)
            permission_hour = PermissionHour.objects.create(
                employee=employee,
                date=data['date'],
                start_time=data['start_time'],
                end_time=data['end_time'],
                reason=data['reason'],
                status='Pending'
            )
            serializer = PermissionHourSerializer(permission_hour)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Employee.DoesNotExist:
            return Response({'error': 'Employee not found. Please log in again.'}, status=status.HTTP_404_NOT_FOUND)


class ApprovePermissionHourView(APIView):
    """
    API view to approve or reject permission hour requests.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, permission_id):
        action = request.data.get('action')
        try:
            permission = PermissionHour.objects.get(id=permission_id)
        except PermissionHour.DoesNotExist:
            return Response({'error': 'Permission request not found.'}, status=status.HTTP_404_NOT_FOUND)

        if action == 'approve':
            permission.status = 'Approved'

            # Calculate the duration
            start_time = datetime.combine(datetime.min, permission.start_time)
            end_time = datetime.combine(datetime.min, permission.end_time)
            permission_duration = end_time - start_time

            # Save the duration
            permission.duration = permission_duration

            # Send email notification
            send_mail(
                'Permission Request Approved',
                f'Your permission request for {permission_duration} hours on {permission.date} has been approved.',
                'admin@example.com',
                [permission.employee.email]
            )
        elif action == 'reject':
            permission.status = 'Rejected'

            # Send rejection email
            send_mail(
                'Permission Request Rejected',
                f'Your permission request on {permission.date} has been rejected.',
                'admin@example.com',
                [permission.employee.email]
            )
        else:
            return Response({'error': 'Invalid action.'}, status=status.HTTP_400_BAD_REQUEST)

        permission.save()
        return Response({'message': f'Permission request has been {permission.status.lower()}.'}, status=status.HTTP_200_OK)


class ManagePermissionHoursView(APIView):
    """
    API view to list pending permission hour requests.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        pending_requests = PermissionHour.objects.filter(status='Pending')
        serializer = PermissionHourSerializer(pending_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Schedule, DepartmentActiveJob, CalendarEvent, Offer, Shift_attendance
from .serializers import (
    ScheduleSerializer,
    DepartmentActiveJobSerializer,
    CalendarEventSerializer,
    OfferSerializer,
    ShiftAttendanceSerializer,
)


# Schedule API
class ScheduleListCreateAPIView(APIView):
    def get(self, request):
        schedules = Schedule.objects.all()
        serializer = ScheduleSerializer(schedules, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ScheduleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ScheduleDetailAPIView(APIView):
    def get(self, request, pk):
        schedule = Schedule.objects.get(pk=pk)
        serializer = ScheduleSerializer(schedule)
        return Response(serializer.data)

    def put(self, request, pk):
        schedule = Schedule.objects.get(pk=pk)
        serializer = ScheduleSerializer(schedule, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        schedule = Schedule.objects.get(pk=pk)
        schedule.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Department Active Jobs API
class DepartmentActiveJobListCreateAPIView(APIView):
    def get(self, request):
        jobs = DepartmentActiveJob.objects.all()
        serializer = DepartmentActiveJobSerializer(jobs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DepartmentActiveJobSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DepartmentActiveJobDetailAPIView(APIView):
    def get(self, request, pk):
        job = DepartmentActiveJob.objects.get(pk=pk)
        serializer = DepartmentActiveJobSerializer(job)
        return Response(serializer.data)

    def put(self, request, pk):
        job = DepartmentActiveJob.objects.get(pk=pk)
        serializer = DepartmentActiveJobSerializer(job, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        job = DepartmentActiveJob.objects.get(pk=pk)
        job.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Calendar Event API
class CalendarEventListCreateAPIView(APIView):
    def get(self, request):
        events = CalendarEvent.objects.all()
        serializer = CalendarEventSerializer(events, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CalendarEventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CalendarEventDetailAPIView(APIView):
    def get(self, request, pk):
        event = CalendarEvent.objects.get(pk=pk)
        serializer = CalendarEventSerializer(event)
        return Response(serializer.data)

    def put(self, request, pk):
        event = CalendarEvent.objects.get(pk=pk)
        serializer = CalendarEventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        event = CalendarEvent.objects.get(pk=pk)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Offer API
class OfferListCreateAPIView(APIView):
    def get(self, request):
        offers = Offer.objects.all()
        serializer = OfferSerializer(offers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OfferSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OfferDetailAPIView(APIView):
    def get(self, request, pk):
        offer = Offer.objects.get(pk=pk)
        serializer = OfferSerializer(offer)
        return Response(serializer.data)

    def put(self, request, pk):
        offer = Offer.objects.get(pk=pk)
        serializer = OfferSerializer(offer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        offer = Offer.objects.get(pk=pk)
        offer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Shift Attendance API
class ShiftAttendanceListCreateAPIView(APIView):
    def get(self, request):
        shifts = Shift_attendance.objects.all()
        serializer = ShiftAttendanceSerializer(shifts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ShiftAttendanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShiftAttendanceDetailAPIView(APIView):
    def get(self, request, pk):
        shift = Shift_attendance.objects.get(pk=pk)
        serializer = ShiftAttendanceSerializer(shift)
        return Response(serializer.data)

    def put(self, request, pk):
        shift = Shift_attendance.objects.get(pk=pk)
        serializer = ShiftAttendanceSerializer(shift, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        shift = Shift_attendance.objects.get(pk=pk)
        shift.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
