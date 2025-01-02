# from calendar import monthrange
# import datetime
# from mailbox import Message
from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib import messages
# from attendance.views import calculate_total_present_days
from attendance.models import PermissionHour
from attendance.views import calculate_total_present_days
from authentication.utils import generate_reset_token, generate_reset_token_for_employee, generate_reset_token_for_manager, generate_reset_token_for_md, generate_reset_token_for_supervisor, get_email_from_token, get_email_from_token_for_employee, get_email_from_token_for_manager, get_email_from_token_for_md, get_email_from_token_for_supervisor, validate_reset_token, validate_reset_token_for_employee, validate_reset_token_for_manager, validate_reset_token_for_md, validate_reset_token_for_supervisor
from chat.models import Message
from leaves.models import LeaveBalance
from leaves.serializers import LeaveBalanceSerializer

# from projectmanagement.models import Project, Role, Task, Team
from .models import Admin,Manager, Employee, ManagingDirector, Supervisor
# from attendance.models import Attendance, ResetRequest
# from django.contrib.auth import authenticate, login
# from django.contrib.auth.hashers import check_password
from django.conf import settings
from django.core.mail import send_mail
# from .utils import generate_reset_token, generate_reset_token_for_md, get_email_from_token_for_md, validate_reset_token, get_email_from_token, generate_reset_token_for_manager, validate_reset_token_for_manager, get_email_from_token_for_manager, generate_reset_token_for_employee, validate_reset_token_for_employee, get_email_from_token_for_employee, validate_reset_token_for_md 
# # from .forms import LoginForm
# from datetime import datetime, timedelta
# from django.utils.dateparse import parse_date
# from django.utils import timezone
# from django.contrib.auth.password_validation import validate_password
# from django.core.exceptions import ValidationError
import bcrypt

# def index(request):
#     return render(request, 'authentication/index.html')

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Manager, Employee, Admin, ManagingDirector
from .serializers import LoginSerializer, SupervisorSerializer  # Import your serializer
import bcrypt

@api_view(['POST'])
def common_user_login(request):
    serializer = LoginSerializer(data=request.data)
    
    if serializer.is_valid():
        username = serializer.validated_data['username']
        user_id = serializer.validated_data['user_id']
        password = serializer.validated_data['password'].encode('utf-8')

        # Try to authenticate as a Manager
        try:
            manager = Manager.objects.get(username=username, manager_id=user_id)
            if bcrypt.checkpw(password, manager.password.encode('utf-8')):
                request.session['user'] = username
                request.session['user_id'] = user_id
                request.session['email'] = manager.email
                request.session['role'] = 'manager'
                Message.objects.filter(receiver_id=user_id, is_delivered=False).update(is_delivered=True)
                return Response({"message": "Login successful", "role": "manager"}, status=status.HTTP_200_OK)
        except Manager.DoesNotExist:
            pass
        
        # Try to authenticate as a Supervisor
        try:
            supervisor = Supervisor.objects.get(username=username, supervisor_id=user_id)
            if bcrypt.checkpw(password, supervisor.password.encode('utf-8')):
                request.session['user'] = username
                request.session['user_id'] = user_id
                request.session['email'] = supervisor.email
                request.session['role'] = 'supervisor'
                Message.objects.filter(receiver_id=user_id, is_delivered=False).update(is_delivered=True)
                return Response({"message": "Login successful", "role": "supervisor"}, status=status.HTTP_200_OK)
        except Supervisor.DoesNotExist:
            pass

        # Try to authenticate as an Employee
        try:
            employee = Employee.objects.get(username=username, employee_id=user_id)
            if bcrypt.checkpw(password, employee.password.encode('utf-8')):
                request.session['user'] = username
                request.session['user_id'] = user_id
                request.session['email'] = employee.email
                request.session['role'] = 'employee'
                Message.objects.filter(receiver_id=user_id, is_delivered=False).update(is_delivered=True)
                return Response({"message": "Login successful", "role": "employee"}, status=status.HTTP_200_OK)
        except Employee.DoesNotExist:
            pass

        # Try to authenticate as an Admin
        try:
            user = Admin.objects.get(username=username, user_id=user_id)
            if bcrypt.checkpw(password, user.password.encode('utf-8')):
                request.session['user'] = username
                request.session['user_id'] = user_id
                request.session['role'] = 'admin'
                Message.objects.filter(receiver_id=username, is_delivered=False).update(is_delivered=True)
                return Response({"message": "Login successful", "role": "admin"}, status=status.HTTP_200_OK)
        except Admin.DoesNotExist:
            pass
        
        

        # Try to authenticate as a Managing Director
        try:
            user = ManagingDirector.objects.get(username=username, user_id=user_id)
            if bcrypt.checkpw(password, user.password.encode('utf-8')):
                request.session['user'] = username
                request.session['user_id'] = user_id
                request.session['role'] = 'md'
                return Response({"message": "Login successful", "role": "md"}, status=status.HTTP_200_OK)
        except ManagingDirector.DoesNotExist:
            pass

        # If all authentication attempts fail
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .serializers import LoginSerializer, ResetPasswordSerializer
from django.contrib.auth.models import User  # Adjust based on your user model
import bcrypt
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

@api_view(['POST'])
def user_logout(request):
    request.session.flush()
    return Response({"message": "You have been logged out successfully."}, status=status.HTTP_200_OK)

@api_view(['POST'])
def forgot_password(request):
    email = request.data.get('email')

    try:
        user = Admin.objects.get(email=email)
        token = generate_reset_token(email)  # Generate a reset token
        if token:
            reset_link = f"http://127.0.0.1:8000/admin/reset_password/{token}/"

            send_mail(
                'Password Reset Request',
                f'Hello,\n\nWe received a request to reset your password. '
                f'Click the link below to reset your password:\n\n{reset_link}\n\n'
                'If you did not request this change, please ignore this email.\n\nBest regards,\nVulturelines Tech Management Private Ltd.,',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

            return Response({"message": "Password reset link sent to your email."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Something went wrong. Please try again later."}, status=status.HTTP_400_BAD_REQUEST)
    except Admin.DoesNotExist:
        return Response({"error": "Email not found."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def reset_password(request, token):
    serializer = ResetPasswordSerializer(data=request.data)
    if serializer.is_valid():
        password = serializer.validated_data['password']

        if validate_reset_token(token):  # Check if the token is valid
            email = get_email_from_token(token)  # Get email from token
            if email:
                try:
                    user = Admin.objects.get(email=email)
                    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

                    user.password = hashed_password
                    user.reset_token = None
                    user.token_expiration = None
                    user.save()

                    return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)
                except Admin.DoesNotExist:
                    return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def custom_admin_home(request):
    if 'user' not in request.session:
        return Response({"error": "Unauthorized."}, status=status.HTTP_401_UNAUTHORIZED)

    managers = Manager.objects.all()
    employees = Employee.objects.all()
    shift = Shift.objects.all()
    department = Department.objects.all()
    # Collect other models as needed...

    context = {
        'managers': managers,
        'employees': employees,
        'shift' : shift,
        'department': department,
        # Add other context variables as needed...
    }

    return Response(context, status=status.HTTP_200_OK)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Manager, Supervisor, Employee
from .serializers import ManagerSerializer, SupervisorSerializer, EmployeeSerializer
from django.db.models import Sum
from datetime import timedelta

@api_view(['GET'])
def manager_dashboard(request):
    if request.user.is_authenticated and request.session.get('role') == 'manager':
        manager_id = request.session.get('user_id')
        try:
            manager = Manager.objects.get(manager_id=manager_id)
            serializer = ManagerSerializer(manager)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Manager.DoesNotExist:
            return Response({'error': 'Manager not found'}, status=status.HTTP_404_NOT_FOUND)
    return Response({'error': 'Unauthorized access'}, status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
def supervisor_dashboard(request):
    if request.user.is_authenticated and request.session.get('role') == 'supervisor':
        supervisor_id = request.session.get('user_id')
        try:
            supervisor = Supervisor.objects.get(supervisor_id=supervisor_id)
            serializer = SupervisorSerializer(supervisor)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Supervisor.DoesNotExist:
            return Response({'error': 'Supervisor not found'}, status=status.HTTP_404_NOT_FOUND)
    return Response({'error': 'Unauthorized access'}, status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
def employee_dashboard(request):
    if request.user.is_authenticated and request.session.get('role') == 'employee':
        employee_id = request.session.get('user_id')
        user = request.session.get('user')
        try:
            employee = Employee.objects.get(employee_id=employee_id)
            leave_balance = LeaveBalance.objects.filter(user=user).first()
            
            # # Calculate total approved permission hours
            total_permission_hours = PermissionHour.objects.filter(
                employee=employee, status='Approved'
            ).aggregate(total=Sum('duration'))['total'] or timedelta()

            # Assume calculate_total_present_days is a utility function
            total_present_days = calculate_total_present_days(employee.id)

            response_data = {
                'employee': EmployeeSerializer(employee).data,
                'leave_balance': LeaveBalanceSerializer(leave_balance).data if leave_balance else None,
                # 'total_permission_hours': total_permission_hours.total_seconds() / 3600,  # Convert to hours
                'total_present_days': total_present_days,
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Employee.DoesNotExist:
            return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)
    return Response({'error': 'Unauthorized access'}, status=status.HTTP_403_FORBIDDEN)


from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Manager, Employee
from django.core.mail import send_mail
from django.conf import settings
import bcrypt

@api_view(['POST'])
def forgot_password_manager(request):
    email = request.data.get('email')

    try:
        user = Manager.objects.get(email=email)
        token = generate_reset_token_for_manager(email)  # Generate a reset token
        if token:
            reset_link = f"http://127.0.0.1:8000/manager/reset_password/{token}/"

            send_mail(
                'Password Reset Request',
                f'Hello,\n\nWe received a request to reset your password. '
                f'Click the link below to reset your password:\n\n{reset_link}\n\n'
                'If you did not request this change, please ignore this email.\n\nBest regards,\nVulturelines Tech Management Private Ltd.',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

            return Response({"message": "Password reset link sent to your email."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Something went wrong. Please try again later."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Manager.DoesNotExist:
        return Response({"error": "Email not found."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def reset_password_manager(request, token):
    password = request.data.get('password')

    if validate_reset_token_for_manager(token):  # Check if the token is valid
        email = get_email_from_token_for_manager(token)  # Get email from token
        if email:
            try:
                user = Manager.objects.get(email=email)
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                
                # Update the password and clear the reset token and expiration
                user.password = hashed_password
                user.reset_token = None
                user.token_expiration = None
                user.save()

                return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)
            except Manager.DoesNotExist:
                return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def forgot_password_employee(request):
    email = request.data.get('email')

    try:
        user = Employee.objects.get(email=email)
        token = generate_reset_token_for_employee(email)  # Generate a reset token
        if token:
            reset_link = f"http://127.0.0.1:8000/employee/reset_password/{token}/"

            send_mail(
                'Password Reset Request',
                f'Hello,\n\nWe received a request to reset your password. '
                f'Click the link below to reset your password:\n\n{reset_link}\n\n'
                'If you did not request this change, please ignore this email.\n\nBest regards,\nVulturelines Tech Management Private Ltd.',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

            return Response({"message": "Password reset link sent to your email."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Something went wrong. Please try again later."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Employee.DoesNotExist:
        return Response({"error": "Email not found."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def reset_password_employee(request, token):
    password = request.data.get('password')

    if validate_reset_token_for_employee(token):  # Check if the token is valid
        email = get_email_from_token_for_employee(token)  # Get email from token
        if email:
            try:
                user = Employee.objects.get(email=email)
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                
                # Update the password and clear the reset token and expiration
                user.password = hashed_password
                user.reset_token = None
                user.token_expiration = None
                user.save()

                return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)
            except Employee.DoesNotExist:
                return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)


from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Manager, Employee, Department, Shift, Location
from .serializers import ManagerSerializer, EmployeeSerializer, DepartmentSerializer, ShiftSerializer, LocationSerializer
import bcrypt
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

# Add Manager
@api_view(['POST'])
def add_manager(request):
    # Instantiate the serializer with the incoming request data
    serializer = ManagerSerializer(data=request.data)
    
    # Check if the serializer is valid
    if serializer.is_valid():
        # If password is valid, it will be hashed in the serializer itself
        try:
            # The password validation is already handled inside the serializer's create method
            raw_password = request.data.get('password')
            validate_password(raw_password)  # Optionally re-validate password here if needed
            
        except ValidationError as e:
            return Response({"errors": e.messages}, status=status.HTTP_400_BAD_REQUEST)
        
        # Save the manager instance (the password is already hashed in the serializer)
        serializer.save()
        return Response({"message": "Manager added successfully!"}, status=status.HTTP_201_CREATED)

    # If the serializer is not valid, return validation errors
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Update Manager
@api_view(['PUT'])
def update_manager(request, id):
    manager = Manager.objects.get(manager_id=id)
    serializer = ManagerSerializer(manager, data=request.data, partial=True)  # Use partial=True for optional fields
    if serializer.is_valid():
        if 'password' in request.data:
            raw_password = request.data.get('password')

            # Validate the password
            try:
                validate_password(raw_password)
            except ValidationError as e:
                return Response({"errors": e.messages}, status=status.HTTP_400_BAD_REQUEST)

            hashed_password = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            serializer.validated_data['password'] = hashed_password
        
        serializer.save()
        return Response({"message": "Manager updated successfully!"}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View Manager Profile
@api_view(['GET'])
def view_manager_profile(request, id):
    manager = get_object_or_404(Manager, manager_id=id)
    serializer = ManagerSerializer(manager)
    return Response(serializer.data, status=status.HTTP_200_OK)

# View Manager Profile
@api_view(['GET'])
def manager_list(request):
    manager = Manager.objects.all()
    serializer = ManagerSerializer(manager,many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Update Manager Profile
@api_view(['PUT'])
def update_manager_profile(request, id):
    manager = get_object_or_404(Manager, manager_id=id)
    serializer = ManagerSerializer(manager, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Manager profile updated successfully."}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Delete Manager
@api_view(['DELETE'])
def delete_manager(request, id):
    try:
        manager = Manager.objects.get(manager_id=id)
        manager.delete()
        return Response({"message": "Manager deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)
    except Manager.DoesNotExist:
        return Response({"error": "Manager not found."}, status=status.HTTP_404_NOT_FOUND)
    
# Add Manager
@api_view(['POST'])
def add_supervisor(request):
    # Instantiate the serializer with the incoming request data
    serializer = SupervisorSerializer(data=request.data)
    
    # Check if the serializer is valid
    if serializer.is_valid():
        # If password is valid, it will be hashed in the serializer itself
        try:
            # The password validation is already handled inside the serializer's create method
            raw_password = request.data.get('password')
            validate_password(raw_password)  # Optionally re-validate password here if needed
            
        except ValidationError as e:
            return Response({"errors": e.messages}, status=status.HTTP_400_BAD_REQUEST)
        
        # Save the manager instance (the password is already hashed in the serializer)
        serializer.save()
        return Response({"message": "Supervisor added successfully!"}, status=status.HTTP_201_CREATED)

    # If the serializer is not valid, return validation errors
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Update Manager
@api_view(['PUT'])
def update_supervisor(request, id):
    supervisor = Supervisor.objects.get(supervisor_id=id)
    serializer = SupervisorSerializer(supervisor, data=request.data, partial=True)  # Use partial=True for optional fields
    if serializer.is_valid():
        if 'password' in request.data:
            raw_password = request.data.get('password')

            # Validate the password
            try:
                validate_password(raw_password)
            except ValidationError as e:
                return Response({"errors": e.messages}, status=status.HTTP_400_BAD_REQUEST)

            hashed_password = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            serializer.validated_data['password'] = hashed_password
        
        serializer.save()
        return Response({"message": "Supervisor updated successfully!"}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Delete Manager
@api_view(['DELETE'])
def delete_supervisor(request, id):
    try:
        supervisor = Supervisor.objects.get(supervisor_id=id)
        supervisor.delete()
        return Response({"message": "Supervisor deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)
    except Manager.DoesNotExist:
        return Response({"error": "Superviosr not found."}, status=status.HTTP_404_NOT_FOUND) 

# View Manager Profile
@api_view(['GET'])
def view_supervisor_profile(request, id):
    supervisor = get_object_or_404(Supervisor, supervisor_id=id)
    serializer = SupervisorSerializer(supervisor)
    return Response(serializer.data, status=status.HTTP_200_OK)



# Update Manager Profile
@api_view(['PUT'])
def update_supervisor_profile(request, id):
    supervisor = get_object_or_404(Manager, supervisor_id=id)
    serializer = SupervisorSerializer(supervisor, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Manager profile updated successfully."}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)      


# View Over all Supervisor Profile
@api_view(['GET'])
def supervisor_list(request):
    supervisor = Supervisor.objects.all()
    serializer = SupervisorSerializer(supervisor,many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# Delete Supervisor
@api_view(['DELETE'])
def delete_supervisor_overall(request):
    try:
        supervisor = Supervisor.objects.all()
        supervisor.delete()
        return Response({"message": "Supervisor  table deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)
    except Manager.DoesNotExist:
        return Response({"error": "Superviosr not found."}, status=status.HTTP_404_NOT_FOUND)     
    


@api_view(['POST'])
def forgot_password_supervisor(request):
    email = request.data.get('email')

    try:
        user = Supervisor.objects.get(email=email)
        token = generate_reset_token_for_supervisor(email)  # Generate a reset token
        if token:
            reset_link = f"http://127.0.0.1:8000/supervisor/reset_password/{token}/"

            send_mail(
                'Password Reset Request',
                f'Hello,\n\nWe received a request to reset your password. '
                f'Click the link below to reset your password:\n\n{reset_link}\n\n'
                'If you did not request this change, please ignore this email.\n\nBest regards,\nVulturelines Tech Management Private Ltd.',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

            return Response({"message": "Password reset link sent to your email."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Something went wrong. Please try again later."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Manager.DoesNotExist:
        return Response({"error": "Email not found."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def reset_password_supervisor(request, token):
    password = request.data.get('password')

    if validate_reset_token_for_supervisor(token):  # Check if the token is valid
        email = get_email_from_token_for_supervisor(token)  # Get email from token
        if email:
            try:
                user = Supervisor.objects.get(email=email)
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                
                # Update the password and clear the reset token and expiration
                user.password = hashed_password
                user.reset_token = None
                user.token_expiration = None
                user.save()

                return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)
            except Manager.DoesNotExist:
                return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)     
    







# Repeat for Employee
@api_view(['POST'])
def add_employee(request):
    # Instantiate the serializer with the incoming request data
    serializer = EmployeeSerializer(data=request.data)
    
    # Check if the serializer is valid
    if serializer.is_valid():
        # If password is valid, it will be hashed in the serializer itself
        try:
            # The password validation is already handled inside the serializer's create method
            raw_password = request.data.get('password')
            validate_password(raw_password)  # Optionally re-validate password here if needed
            
        except ValidationError as e:
            return Response({"errors": e.messages}, status=status.HTTP_400_BAD_REQUEST)
        
        # Save the manager instance (the password is already hashed in the serializer)
        serializer.save()
        return Response({"message": "Employee added successfully!"}, status=status.HTTP_201_CREATED)

    # If the serializer is not valid, return validation errors
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_employee(request, id):
    employee = Employee.objects.get(id=id)
    serializer = EmployeeSerializer(employee, data=request.data, partial=True)
    if serializer.is_valid():
        if 'password' in request.data:
            raw_password = request.data.get('password')

            # Validate the password
            try:
                validate_password(raw_password)
            except ValidationError as e:
                return Response({"errors": e.messages}, status=status.HTTP_400_BAD_REQUEST)

            hashed_password = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            serializer.validated_data['password'] = hashed_password
        
        serializer.save()
        return Response({"message": "Employee updated successfully!"}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View all Employee Profiles
@api_view(['GET'])
def employee_list(request):
    try:
        # Retrieve all employees from the database
        employees = Employee.objects.all()

        # Serialize the data (many=True because we're passing a queryset)
        serializer = EmployeeSerializer(employees, many=True)

        # Return the serialized employee data in the response
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        # In case of any unexpected errors
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
# Update Employee Profile
@api_view(['PUT'])
def update_employee_profile(request, id):
    try:
        # Retrieve the employee object from the database
        employee = get_object_or_404(Employee, employee_id=id)

        # Log the incoming request data for debugging purposes
        print("Incoming request data:", request.data)

        # Serialize the data with the existing employee data
        serializer = EmployeeSerializer(employee, data=request.data, partial=True)

        # Check if the serializer is valid and log errors if any
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated successfully."}, status=status.HTTP_200_OK)
        else:
            # Log the validation errors for debugging
            print("Serializer errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(f"Error updating profile: {str(e)}")
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
def delete_employee(request, id):
    try:
        employee = Employee.objects.get(id=id)
        employee.delete()
        return Response({"message": "Employee deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)
    except Employee.DoesNotExist:
        return Response({"error": "Employee not found."}, status=status.HTTP_404_NOT_FOUND)

# Repeat for Department
@api_view(['POST'])
def add_department(request):
    serializer = DepartmentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Department added successfully!"}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def show_department(request, id):
    try:
        department = Department.objects.get(id=id)
        serializer = DepartmentSerializer(department)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Department.DoesNotExist:
        return Response({"error": "Department not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def overall_department(request):
    try:
        # Fetch all department records from the database
        departments = Department.objects.all()

        # Serialize the department data (many=True indicates multiple objects)
        serializer = DepartmentSerializer(departments, many=True)

        # Return the serialized data as a response
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        # In case of any unexpected errors
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
def update_department(request, id):
    department = Department.objects.get(id=id)
    serializer = DepartmentSerializer(department, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Department updated successfully!"}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_department(request, id):
    try:
        department = Department.objects.get(id=id)
        department.delete()
        return Response({"message": "Department deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)
    except Department.DoesNotExist:
        return Response({"error": "Department not found."}, status=status.HTTP_404_NOT_FOUND)

# Repeat for Shift
@api_view(['POST'])
def add_shift(request):
    serializer = ShiftSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Shift added successfully!"}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_shift(request, id):
    shift = Shift.objects.get(id=id)
    serializer = ShiftSerializer(shift, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Shift updated successfully!"}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def show_shift(request, id):
    shift = Shift.objects.get(id=id)
    serializer = ShiftSerializer(shift)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def overall_shift(request):
    shift = Shift.objects.all()
    serializer = ShiftSerializer(shift,many=True)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_shift(request, id):
    try:
        shift = Shift.objects.get(id=id)
        shift.delete()
        return Response({"message": "Shift deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)
    except Shift.DoesNotExist:
        return Response({"error": "Shift not found."}, status=status.HTTP_404_NOT_FOUND)

# Repeat for Location
@api_view(['POST'])
def add_location(request):
    serializer = LocationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Location added successfully!"}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_location(request, id):
    location = Location.objects.get(id=id)
    serializer = LocationSerializer(location, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Location updated successfully!"}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def show_location(request, id):
    location = Location.objects.get(id=id)
    serializer = LocationSerializer(location)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def overall_location(request):
    location = Location.objects.all()
    serializer = LocationSerializer(location,many=True)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_location(request, id):
    try:
        location = Location.objects.get(id=id)
        location.delete()
        return Response({"message": "Location deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)
    except Location.DoesNotExist:
        return Response({"error": "Location not found."}, status=status.HTTP_404_NOT_FOUND)






from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Manager, Employee, Department, Shift, Location
from .serializers import ManagerSerializer, EmployeeSerializer, DepartmentSerializer, ShiftSerializer, LocationSerializer
import bcrypt
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

@api_view(['GET'])
def md_home(request):
    if 'user' not in request.session:
        return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)

    managers = Manager.objects.all()
    employees = Employee.objects.all()
    departments = Department.objects.all()
    shifts = Shift.objects.all()
    locations = Location.objects.all()

    context = {
        'managers': ManagerSerializer(managers, many=True).data,
        'employees': EmployeeSerializer(employees, many=True).data,
        'departments': DepartmentSerializer(departments, many=True).data,
        'shifts': ShiftSerializer(shifts, many=True).data,
        'locations': LocationSerializer(locations, many=True).data,
    }

    return Response(context, status=status.HTTP_200_OK)

@api_view(['POST'])
def md_add_manager(request):
    serializer = ManagerSerializer(data=request.data)
    if serializer.is_valid():
        raw_password = request.data.get('password')

        try:
            validate_password(raw_password)
        except ValidationError as e:
            return Response({"errors": e.messages}, status=status.HTTP_400_BAD_REQUEST)

        hashed_password = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        serializer.validated_data['password'] = hashed_password

        serializer.save()
        return Response({"message": "Manager added successfully!"}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def md_add_supervisor(request):
    serializer = SupervisorSerializer(data=request.data)
    if serializer.is_valid():
        raw_password = request.data.get('password')

        try:
            validate_password(raw_password)
        except ValidationError as e:
            return Response({"errors": e.messages}, status=status.HTTP_400_BAD_REQUEST)

        hashed_password = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        serializer.validated_data['password'] = hashed_password

        serializer.save()
        return Response({"message": "supervisor added successfully!"}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def md_add_employee(request):
    serializer = EmployeeSerializer(data=request.data)
    if serializer.is_valid():
        raw_password = request.data.get('password')

        try:
            validate_password(raw_password)
        except ValidationError as e:
            return Response({"errors": e.messages}, status=status.HTTP_400_BAD_REQUEST)

        hashed_password = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        serializer.validated_data['password'] = hashed_password

        serializer.save()
        return Response({"message": "Employee added successfully!"}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def md_add_department(request):
    serializer = DepartmentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Department added successfully!"}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def md_add_shift(request):
    serializer = ShiftSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Shift added successfully!"}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def md_add_location(request):
    serializer = LocationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Location added successfully!"}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def md_show_location(request, id):
    location = Location.objects.get(id=id)
    serializer = LocationSerializer(location)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def md_show_overall_location(request):
    location = Location.objects.all()
    serializer = LocationSerializer(location,many=True)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def md_show_shift(request, id):
    shift = Shift.objects.get(id=id)
    serializer = ShiftSerializer(shift)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def md_show_overall_shift(request):
    shift = Shift.objects.all()
    serializer = ShiftSerializer(shift,many=True)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def md_show_department(request, id):
    department = Department.objects.get(id=id)
    serializer = ShiftSerializer(department)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def md_show_overall_department(request):
    department = Department.objects.all()
    serializer = DepartmentSerializer(department,many=True)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def md_employee_list(request):
    employee = Employee.objects.all()
    serializer = EmployeeSerializer(employee,many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# View Employee Profile
@api_view(['GET'])
def md_view_employee_profile(request, id):
    employee = get_object_or_404(Employee, employee_id=id)
    serializer = EmployeeSerializer(employee)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def md_manager_list(request):
    manager = Employee.objects.all()
    serializer = EmployeeSerializer(manager,many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# View Employee Profile
@api_view(['GET'])
def md_view_manager_profile(request, id):
    manager = get_object_or_404(Manager, manager_id=id)
    serializer = ManagerSerializer(manager)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def md_supervisor_list(request):
    supervisor = Supervisor.objects.all()
    serializer = SupervisorSerializer(supervisor,many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# View Employee Profile
@api_view(['GET'])
def md_view_supervisor_profile(request, id):
    supervisor = get_object_or_404(Supervisor, supervisor_id=id)
    serializer = SupervisorSerializer(supervisor)
    return Response(serializer.data, status=status.HTTP_200_OK)





# #Delete functionality perform by mdfrom rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from .models import Manager, Employee, Department, Shift, Location
from .serializers import ManagerSerializer, EmployeeSerializer, DepartmentSerializer, ShiftSerializer, LocationSerializer

# Delete Functions
@api_view(['DELETE'])
def md_delete_manager(request, manager_id):
    manager = get_object_or_404(Manager, manager_id=manager_id)
    manager.delete()
    return Response({'message': 'Manager deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

# Delete Functions
@api_view(['DELETE'])
def md_delete_supervisor(request, supervisor_id):
    supervisor = get_object_or_404(Supervisor, supervisor_id=supervisor_id)
    supervisor.delete()
    return Response({'message': 'supervisor deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['DELETE'])
def md_delete_employee(request, employee_id):
    employee = get_object_or_404(Employee, employee_id=employee_id)
    employee.delete()
    return Response({'message': 'Employee deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['DELETE'])
def md_delete_department(request, department_id):
    department = get_object_or_404(Department, department_id=department_id)
    department.delete()
    return Response({'message': 'Department deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['DELETE'])
def md_delete_shift(request, shift_number):
    shift = get_object_or_404(Shift, shift_number=shift_number)
    shift.delete()
    return Response({'message': 'Shift deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['DELETE'])
def md_delete_location(request, location_id):
    location = get_object_or_404(Location, location_id=location_id)
    location.delete()
    return Response({'message': 'Location deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

# Update Functions
@api_view(['PUT'])
def md_update_manager(request, id):
    manager = get_object_or_404(Manager, id=id)
    serializer = ManagerSerializer(manager, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Update Functions
@api_view(['PUT'])
def md_update_supervisor(request, id):
    supervisor = get_object_or_404(Supervisor, id=id)
    serializer = SupervisorSerializer(supervisor, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def md_update_employee(request, id):
    employee = get_object_or_404(Employee, id=id)
    serializer = EmployeeSerializer(employee, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def md_update_department(request, id):
    department = get_object_or_404(Department, id=id)
    serializer = DepartmentSerializer(department, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def md_update_shift(request, id):
    shift = get_object_or_404(Shift, id=id)
    serializer = ShiftSerializer(shift, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def md_update_location(request, id):
    location = get_object_or_404(Location, id=id)
    serializer = LocationSerializer(location, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Password Reset Functions
@api_view(['POST'])
def forgot_password_md(request):
    email = request.data.get('email')
    try:
        user = ManagingDirector.objects.get(email=email)
        token = generate_reset_token_for_md(email)  # Replace with your token generation logic
        reset_link = f"http://127.0.0.1:8000/md/reset_password_md/{token}/"
        
        # Send email logic here...

        return Response({'message': 'Password reset link sent to your email.'}, status=status.HTTP_200_OK)
    except ManagingDirector.DoesNotExist:
        return Response({'error': 'Email not found.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def reset_password_md(request, token):
    password = request.data.get('password')
    if validate_reset_token_for_md(token):  # Check if the token is valid
        email = get_email_from_token_for_md(token)  # Get email from token
        if email:
            try:
                user = ManagingDirector.objects.get(email=email)
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                user.password = hashed_password
                user.save()
                return Response({'message': 'Password has been reset successfully.'}, status=status.HTTP_200_OK)
            except ManagingDirector.DoesNotExist:
                return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)


from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Employee, Manager
from .serializers import EmployeeSerializer, ManagerSerializer





# Update Manager Profile
@api_view(['PUT'])
def update_supervisor_profile(request, id):
    supervisor = get_object_or_404(Supervisor, supervisor_id=id)
    serializer = SupervisorSerializer(supervisor, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response({"message": "supervisor profile updated successfully."}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def manager_view_employee_profile(request):
    employee_id = request.data.get('employee_id')

    if not employee_id:
        return Response({"error": "Employee ID is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        employee = get_object_or_404(Employee, employee_id=employee_id)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Employee.DoesNotExist:
        return Response({"error": f"No employee found with ID {employee_id}."}, status=status.HTTP_404_NOT_FOUND)
    
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Requests, Employee, Supervisor, Admin
from .serializers import RequestsSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_request(request):
    if request.method == 'POST':
        data = request.data
        employee_username = request.user.username  # Assume request.user is authenticated
        try:
            employee = Employee.objects.get(username=employee_username)
            supervisor = Supervisor.objects.get(id=data.get('supervisor_id'))

            new_request = Requests.objects.create(
                employee=employee,
                supervisor=supervisor,
                title=data.get('title'),
                request_ticket_id=data.get('request_ticket_id'),
                description=data.get('description'),
                status='onprocess',
            )
            serializer = RequestsSerializer(new_request)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Employee.DoesNotExist:
            return Response({'error': 'Employee not found. Please log in again.'}, status=status.HTTP_400_BAD_REQUEST)
        except Supervisor.DoesNotExist:
            return Response({'error': 'Supervisor not found.'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def supervisor_view_allrequest(request):
    if request.method == 'GET':
        supervisor_id = request.user.id  # Assume the user is authenticated and represents a supervisor
        try:
            supervisor = Supervisor.objects.get(supervisor_id=supervisor_id)
            requests = Requests.objects.filter(supervisor=supervisor)
            serializer = RequestsSerializer(requests, many=True)
            return Response(serializer.data)
        except Supervisor.DoesNotExist:
            return Response({'error': 'Supervisor not found.'}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'POST':
        action = request.data.get('action')
        request_id = request.data.get('request_id')
        try:
            request_obj = Requests.objects.get(id=request_id)
            if action == 'Approve':
                request_obj.status = 'Approved'
            elif action == 'Reject':
                request_obj.status = 'Rejected'
            elif action == 'Forward':
                admin = Admin.objects.first()
                if admin:
                    request_obj.supervisor = None
                    request_obj.admin = admin
                    request_obj.status = 'Forwarded'
                else:
                    return Response({'error': 'No admin available to forward the request.'}, status=status.HTTP_400_BAD_REQUEST)
            request_obj.save()
            return Response({'message': f'Request {action} successfully.'}, status=status.HTTP_200_OK)
        except Requests.DoesNotExist:
            return Response({'error': 'Request not found.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def admin_view_request(request):
    if request.method == 'GET':
        forwarded_requests = Requests.objects.filter(status='Forwarded')
        serializer = RequestsSerializer(forwarded_requests, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        action = request.data.get('action')
        request_id = request.data.get('request_id')
        try:
            request_obj = Requests.objects.get(id=request_id)
            if action == 'Approve':
                supervisor = Supervisor.objects.first()
                if supervisor:
                    request_obj.admin = None
                    request_obj.supervisor = supervisor
                    request_obj.admin_status = 'Approved'
            elif action == 'Reject':
                supervisor = Supervisor.objects.first()
                if supervisor:
                    request_obj.admin = None
                    request_obj.supervisor = supervisor
                    request_obj.admin_status = 'Rejected'
            request_obj.save()
            return Response({'message': f'Request {action} successfully.'}, status=status.HTTP_200_OK)
        except Requests.DoesNotExist:
            return Response({'error': 'Request not found.'}, status=status.HTTP_404_NOT_FOUND)


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import News, Ticket, Requests, Manager
from .serializers import NewsSerializer, TicketSerializer, RequestsSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_news(request):
    if request.method == "POST":
        serializer = NewsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(date=timezone.now().date())  # Automatically set the date to today's date
            return Response({"message": "News sent successfully!", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_all_news(request):
    if request.method == "GET":
        all_news = News.objects.all().order_by('-date')
        serializer = NewsSerializer(all_news, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_news(request,id):
    if request.method == "GET":
        all_news = News.objects.get(id=id)
        serializer = NewsSerializer(all_news)
        return Response(serializer.data, status=status.HTTP_200_OK)    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def self_all_service(request):
    if request.method == "GET":
        tickets = Ticket.objects.all()
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def self_service(request,id):
    if request.method == "GET":
        tickets = Ticket.objects.get(id=id)
        serializer = TicketSerializer(tickets)
        return Response(serializer.data, status=status.HTTP_200_OK)    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_ticket(request):
    if request.method == "POST":
        data = request.data
        receiver = data.get('receiver')
        hr_name = data.get('hr_name')
        tl_name = data.get('tl_name')
        proof = request.FILES.get('proof')  # Uploaded proof file

        # Determine the manager assigned based on the receiver (HR or TL)
        assigned_manager = None
        if receiver == 'HR':
            assigned_manager = Manager.objects.filter(manager_name=hr_name).first()
        elif receiver == 'TL':
            assigned_manager = Manager.objects.filter(manager_name=tl_name).first()

        if not assigned_manager:
            return Response({"error": "Manager not found for the given receiver."}, status=status.HTTP_400_BAD_REQUEST)

        # Add the assigned manager to the data
        ticket_data = {
            "title": data.get('title'),
            "description": data.get('description'),
            "Reciver": receiver,
            "assigned_to": assigned_manager.id,  # Pass manager ID for the ForeignKey field
            "proof": proof,
        }

        serializer = TicketSerializer(data=ticket_data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Ticket created successfully!", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def self_all_request(request):
    if request.method == "GET":
        all_requests = Requests.objects.all()
        serializer = RequestsSerializer(all_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def self_request(request,id):
    if request.method == "GET":
        all_requests = Requests.objects.get(id=id)
        serializer = RequestsSerializer(all_requests)
        return Response(serializer.data, status=status.HTTP_200_OK)    

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Todo
from .serializers import TodoSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def todo_all_list(request):
    """
    List all Todos.
    """
    todos = Todo.objects.all()
    serializer = TodoSerializer(todos, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def todo_list(request,id):
    """
    List all Todos.
    """
    todos = Todo.objects.get(id=id)
    serializer = TodoSerializer(todos)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def todo_create(request):
    """
    Create a new Todo item.
    """
    serializer = TodoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Todo item created successfully!", "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def todo_toggle(request, id):
    """
    Toggle the 'completed' status of a Todo item.
    """
    todo = get_object_or_404(Todo, id=id)
    todo.completed = not todo.completed
    todo.save()
    serializer = TodoSerializer(todo)
    return Response({"message": "Todo status toggled successfully!", "data": serializer.data}, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def todo_delete(request, id):
    """
    Delete a Todo item.
    """
    todo = get_object_or_404(Todo, id=id)
    todo.delete()
    return Response({"message": "Todo item deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)
