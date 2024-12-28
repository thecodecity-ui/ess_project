from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum
from django.utils.timezone import now
from datetime import datetime
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from authentication.models import Employee, Supervisor
from attendance.models import Attendance
from .models import PayrollManagement, PayrollNotification, SupervisorPayrollNotification
from .serializers import PayrollManagementSerializer, SupervisorPayrollNotificationSerializer


def create_payslip_pdf(payroll):
    file_path = f'payslips/{payroll.user_id}_{payroll.month.strftime("%Y_%m")}.pdf'
    c = canvas.Canvas(file_path, pagesize=letter)
    width, height = letter

    c.drawString(100, height - 100, f'Payslip for {payroll.user} - {payroll.month.strftime("%B %Y")}')
    c.drawString(100, height - 120, f'User ID: {payroll.user_id}')
    c.drawString(100, height - 140, f'Base Salary: {payroll.base_salary}')
    c.drawString(100, height - 160, f'Total Working Hours: {payroll.total_working_hours}')
    c.drawString(100, height - 180, f'Total Overtime Hours: {payroll.overtime_hours}')
    c.drawString(100, height - 200, f'Net Salary: {payroll.net_salary}')
    c.drawString(100, height - 220, 'Thank you for your hard work!')
    c.drawString(100, height - 280, 'Best regards')
    c.drawString(100, height - 300, 'Your Company')
    c.save()
    return file_path


class ProcessPayrollAPIView(APIView):
    """
    Handles payroll processing for employees.
    """
    def post(self, request, *args, **kwargs):
        month_str = request.data.get('month')
        base_salary = request.data.get('base_salary')
        employee_id = request.data.get('employee_id')

        try:
            month = datetime.strptime(month_str, "%Y-%m")
            employee = Employee.objects.get(employee_id=employee_id)
        except (Employee.DoesNotExist, ValueError):
            return Response({'success': False, 'message': 'Invalid employee ID or month format.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check for existing payroll
        if PayrollManagement.objects.filter(user_id=employee.employee_id, month=month).exists():
            return Response({'success': False, 'message': 'Payslip for this month has already been generated.'}, status=status.HTTP_400_BAD_REQUEST)

        # Calculate working hours and overtime
        total_hours = Attendance.objects.filter(employee=employee, date__month=month.month, date__year=month.year).aggregate(
            Sum('total_working_hours')
        )['total_working_hours__sum'] or 0

        overtime_hours = Attendance.objects.filter(employee=employee, date__month=month.month, date__year=month.year).aggregate(
            Sum('overtime')
        )['overtime__sum'] or 0

        base_salary = float(base_salary)
        total_days = total_hours / 8
        per_day_rate = base_salary / 30
        per_hour_rate = per_day_rate / 8
        net_salary = float(per_day_rate * total_days)
        overtime_salary = float(overtime_hours * per_hour_rate)

        # Create payroll entry
        payroll = PayrollManagement.objects.create(
            user=employee.username,
            user_id=employee.employee_id,
            month=month,
            email=employee.email,
            base_salary=base_salary,
            net_salary=net_salary,
            total_working_hours=total_hours,
            overtime_hours=overtime_hours,
            overtime_pay=overtime_salary,
        )

        # Generate PDF
        pdf_path = create_payslip_pdf(payroll)
        payroll.pdf_path = pdf_path
        payroll.save()

        # Send email with payslip
        subject = f'Your Payslip for {month.strftime("%B %Y")}'
        html_message = render_to_string('payroll/payslip_view.html', {'payroll': payroll})
        plain_message = strip_tags(html_message)
        from_email = 'sudhakar.ibacustech@gmail.com'
        to_email = employee.email

        email = EmailMessage(subject, plain_message, from_email, [to_email])
        email.attach_file(pdf_path)
        email.send()

        # Create notification
        PayrollNotification.objects.create(
            user=employee.username,
            user_id=employee.employee_id,
            date=now().date(),
            time=now().time(),
            message=f"Your payslip for {month.strftime('%B %Y')} has been generated and sent to your email."
        )

        return Response({'success': True, 'payroll_id': payroll.id, 'pdf_path': pdf_path}, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        """
        List all processed payrolls.
        """
        payrolls = PayrollManagement.objects.all()
        serializer = PayrollManagementSerializer(payrolls, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import PayrollManagement
from .serializers import PayrollManagementSerializer
from django.utils import timezone
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from reportlab.pdfgen import canvas
from datetime import datetime
from .models import ManagerPayrollNotification
from attendance.models import Attendance
from authentication.models import Employee, Manager

def manager_calculate_net_salary(per_day_rate, total_days):
    return (float(per_day_rate) * float(total_days))

class ManagerProcessPayrollAPIView(APIView):
    def post(self, request, *args, **kwargs):
        month_str = request.data.get('month')
        base_salary = request.data.get('base_salary')
        manager_id = request.data.get('manager_id')

        month = datetime.strptime(month_str, "%Y-%m")

        managers = Manager.objects.filter(manager_id=manager_id)

        for manager in managers:
            existing_payroll = PayrollManagement.objects.filter(user_id=manager.manager_id, month=month).first()
            if existing_payroll:
                return Response({'success': False, 'message': 'Payslip for this month has already been generated.'}, status=status.HTTP_400_BAD_REQUEST)

            total_hours = Attendance.objects.filter(
                manager=manager,
                date__month=month.month,
                date__year=month.year
            ).aggregate(Sum('total_working_hours'))['total_working_hours__sum'] or 0
            
            overtime_hours = Attendance.objects.filter(
                manager=manager,
                date__month=month.month,
                date__year=month.year
            ).aggregate(Sum('overtime'))['overtime__sum'] or 0

            base_salary = float(base_salary)
            total_days = total_hours / 8
            per_day_rate = base_salary / 30
            per_hour_rate = per_day_rate / 8
            net_salary = manager_calculate_net_salary(per_day_rate, total_days)
            overtime_salary = overtime_hours * per_hour_rate
            
            payroll = PayrollManagement.objects.create(
                user=manager.username,
                user_id=manager.manager_id,
                month=month,
                email=manager.email,
                base_salary=base_salary,
                net_salary=net_salary,
                total_working_hours=total_hours,
                overtime_hours=overtime_hours,
                overtime_pay=overtime_salary,
            )

            pdf_path = create_payslip_pdf(payroll)
            payroll.pdf_path = pdf_path
            payroll.save()

            subject = f'Your Payslip for {month.strftime("%B %Y")}'
            html_message = render_to_string('payroll/manager_payslip_view.html', {'payroll': payroll})
            plain_message = strip_tags(html_message)
            from_email = 'sudhakar.ibacustech@gmail.com'  # Use the same email as in settings
            to_email = manager.email
            email = EmailMessage(subject, plain_message, from_email, [to_email])
            email.attach_file(pdf_path)
            email.send()

            ManagerPayrollNotification.objects.create(
                user=manager.username,
                user_id=manager.manager_id,
                date=timezone.now().date(),
                time=timezone.localtime(timezone.now()).time(),
                message=f"Your payslip has been generated successfully and sent to your email."
            )

        return Response({'success': True, 'message': f'Payroll processed for {len(managers)} managers.'}, status=status.HTTP_200_OK)

from rest_framework import generics
from .models import PayrollManagement
from .serializers import PayrollManagementSerializer
from rest_framework.filters import OrderingFilter
from django_filters import rest_framework as filters

class PayrollManagementFilter(filters.FilterSet):
    user = filters.CharFilter(field_name='user', lookup_expr='icontains')
    month = filters.DateFilter(field_name='month', lookup_expr='month')

    class Meta:
        model = PayrollManagement
        fields = ['user', 'month']

class PayrollHistoryAPIView(generics.ListAPIView):
    queryset = PayrollManagement.objects.all()
    serializer_class = PayrollManagementSerializer
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    filterset_class = PayrollManagementFilter
    ordering_fields = ['month']

class ManagerPayrollHistoryAPIView(generics.ListAPIView):
    queryset = PayrollManagement.objects.all()
    serializer_class = PayrollManagementSerializer
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    filterset_class = PayrollManagementFilter
    ordering_fields = ['month']

def download_pdf(request, pdf_path):
    # Serve the PDF file
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{pdf_path}"'
    
    # Open the PDF file in binary mode
    with open(pdf_path, 'rb') as pdf:
        response.write(pdf.read())
    
    return response

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import PayrollManagement, PayrollNotification, ManagerPayrollNotification
from .serializers import PayrollManagementSerializer, PayrollNotificationSerializer, ManagerPayrollNotificationSerializer

class PayrollNotificationView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def get(self, request):
        user = request.user.username  # Access the logged-in user's username
        
        # Filter the payrolls and notifications for the logged-in user
        payrolls = PayrollManagement.objects.filter(user=user)
        notifications = PayrollNotification.objects.filter(user=user).order_by('-date', '-time')
        
        # Serialize the data
        payrolls_serializer = PayrollManagementSerializer(payrolls, many=True)
        notifications_serializer = PayrollNotificationSerializer(notifications, many=True)
        
        # Return the serialized data as a JSON response
        return Response({
            'payrolls': payrolls_serializer.data,
            'notifications': notifications_serializer.data
        })

class ManagerPayrollNotificationView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def get(self, request):
        user = request.user.username  # Access the logged-in user's username
        
        # Filter the payrolls and notifications for the logged-in user (manager)
        payrolls = PayrollManagement.objects.filter(user=user)
        notifications = ManagerPayrollNotification.objects.filter(user=user).order_by('-date', '-time')
        
        # Serialize the data
        payrolls_serializer = PayrollManagementSerializer(payrolls, many=True)
        notifications_serializer = ManagerPayrollNotificationSerializer(notifications, many=True)
        
        # Return the serialized data as a JSON response
        return Response({
            'payrolls': payrolls_serializer.data,
            'notifications': notifications_serializer.data
        })

def supervisor_calculate_net_salary(per_day_rate, total_days):
    return (float(per_day_rate) * float(total_days))

class SupervisorProcessPayrollAPIView(APIView):
    def post(self, request, *args, **kwargs):
        month_str = request.data.get('month')
        base_salary = request.data.get('base_salary')
        supervisor_id = request.data.get('supervisor_id')

        month = datetime.strptime(month_str, "%Y-%m")

        supervisors = Supervisor.objects.filter(supervisor_id=supervisor_id)

        for supervisor in supervisors:
            existing_payroll = PayrollManagement.objects.filter(user_id=supervisor.supervisor_id, month=month).first()
            if existing_payroll:
                return Response({'success': False, 'message': 'Payslip for this month has already been generated.'}, status=status.HTTP_400_BAD_REQUEST)

            total_hours = Attendance.objects.filter(
                supervisor=supervisor,
                date__month=month.month,
                date__year=month.year
            ).aggregate(Sum('total_working_hours'))['total_working_hours__sum'] or 0
            
            overtime_hours = Attendance.objects.filter(
                supervisor=supervisor,
                date__month=month.month,
                date__year=month.year
            ).aggregate(Sum('overtime'))['overtime__sum'] or 0

            base_salary = float(base_salary)
            total_days = total_hours / 8
            per_day_rate = base_salary / 30
            per_hour_rate = per_day_rate / 8
            net_salary = supervisor_calculate_net_salary(per_day_rate, total_days)
            overtime_salary = overtime_hours * per_hour_rate
            
            payroll = PayrollManagement.objects.create(
                user=supervisor.username,
                user_id=supervisor.supervisor_id,
                month=month,
                email=supervisor.email,
                base_salary=base_salary,
                net_salary=net_salary,
                total_working_hours=total_hours,
                overtime_hours=overtime_hours,
                overtime_pay=overtime_salary,
            )

            pdf_path = create_payslip_pdf(payroll)
            payroll.pdf_path = pdf_path
            payroll.save()

            subject = f'Your Payslip for {month.strftime("%B %Y")}'
            html_message = render_to_string('payroll/supervisor_payslip_view.html', {'payroll': payroll})
            plain_message = strip_tags(html_message)
            from_email = 'sudhakar.ibacustech@gmail.com'  # Use the same email as in settings
            to_email = supervisor.email
            email = EmailMessage(subject, plain_message, from_email, [to_email])
            email.attach_file(pdf_path)
            email.send()

            SupervisorPayrollNotification.objects.create(
                user=supervisor.username,
                user_id=supervisor.supervisor_id,
                date=timezone.now().date(),
                time=timezone.localtime(timezone.now()).time(),
                message=f"Your payslip has been generated successfully and sent to your email."
            )

        return Response({'success': True, 'message': f'Payroll processed for {len(supervisors)} supervisors.'}, status=status.HTTP_200_OK)
    
class SupervisorPayrollHistoryAPIView(generics.ListAPIView):
    queryset = PayrollManagement.objects.all()
    serializer_class = PayrollManagementSerializer
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    filterset_class = PayrollManagementFilter
    ordering_fields = ['month']
    
class SupervisorPayrollNotificationView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def get(self, request):
        user = request.user.username  # Access the logged-in user's username
        
        # Filter the payrolls and notifications for the logged-in user (manager)
        payrolls = PayrollManagement.objects.filter(user=user)
        notifications = SupervisorPayrollNotification.objects.filter(user=user).order_by('-date', '-time')
        
        # Serialize the data
        payrolls_serializer = PayrollManagementSerializer(payrolls, many=True)
        notifications_serializer = SupervisorPayrollNotificationSerializer(notifications, many=True)
        
        # Return the serialized data as a JSON response
        return Response({
            'payrolls': payrolls_serializer.data,
            'notifications': notifications_serializer.data
        })    

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Salary, BonusType
from .serializers import SalarySerializer, BonusTypeSerializer


@api_view(['POST'])
def create_salary(request):
    """
    Create a new salary record.
    """
    serializer = SalarySerializer(data=request.data)
    if serializer.is_valid():
        # Check if salary already exists for the given user_id and effective_date
        user_id = serializer.validated_data['user_id']
        effective_date = serializer.validated_data['effective_date']
        if Salary.objects.filter(user_id=user_id, effective_date=effective_date).exists():
            return Response({'detail': 'Salary already exists for this user and effective date.'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_bonus(request):
    """
    Create a new bonus record.
    """
    serializer = BonusTypeSerializer(data=request.data)
    if serializer.is_valid():
        user_id = serializer.validated_data['user_id']
        amount = float(serializer.validated_data['amount'])
        paid_status = serializer.validated_data.get('paid_status', 'pending')

        if paid_status == 'paid':
            # Calculate total paid for the user
            existing_paid_bonuses = BonusType.objects.filter(user_id=user_id, paid_status='paid')
            total_paid = sum(float(bonus.amount) for bonus in existing_paid_bonuses) + amount
            serializer.validated_data['total_paid'] = total_paid
        else:
            serializer.validated_data['total_paid'] = "0"

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def mark_bonus_paid(request, bonus_id):
    """
    Mark a bonus as paid.
    """
    bonus = get_object_or_404(BonusType, id=bonus_id)
    if bonus.paid_status == 'paid':
        return Response({'detail': 'This bonus has already been marked as paid.'}, status=status.HTTP_400_BAD_REQUEST)

    bonus.paid_status = 'paid'
    bonus.total_paid = bonus.amount  # Update total paid with the bonus amount
    bonus.save()

    serializer = BonusTypeSerializer(bonus)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def bonus_list(request):
    """
    List all bonuses.
    """
    bonuses = BonusType.objects.all()
    serializer = BonusTypeSerializer(bonuses, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def salary_history(request):
    """
    Retrieve salary and bonus history for the logged-in user.
    """
    user_id = request.query_params.get('user_id')  # Pass user_id as a query parameter
    if not user_id:
        return Response({'detail': 'User ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

    salary = Salary.objects.filter(user_id=user_id)
    bonuses = BonusType.objects.filter(user_id=user_id)

    salary_serializer = SalarySerializer(salary, many=True)
    bonus_serializer = BonusTypeSerializer(bonuses, many=True)

    return Response({
        'salary': salary_serializer.data,
        'bonuses': bonus_serializer.data
    }, status=status.HTTP_200_OK)
