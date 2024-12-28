from rest_framework import serializers
from .models import Manager, Employee, Department, Shift, Location, Supervisor
import bcrypt
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class ManagerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Ensure password is not returned in responses

    class Meta:
        model = Manager
        fields = ['manager_id', 'manager_name', 'department', 'email', 'gender', 'manager_image', 'shift', 'dob', 'hired_date', 'username', 'password']
    
    def validate_password(self, value):
        """
        Custom password validator to use Django's built-in validation.
        """
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError({
                'password': e.messages
            })
        return value

    def create(self, validated_data):
        """
        Overridden create method to hash the password before saving the manager.
        """
        raw_password = validated_data.pop('password')  # Remove password from validated data
        try:
            # Ensure password meets complexity requirements
            self.validate_password(raw_password)
        except serializers.ValidationError as e:
            raise e  # Propagate the error if validation fails
        
        # Hash password using bcrypt
        hashed_password = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        validated_data['password'] = hashed_password  # Store the hashed password
        
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        If the password is being updated, hash the new password before saving.
        """
        if 'password' in validated_data:
            raw_password = validated_data.pop('password')
            hashed_password = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            validated_data['password'] = hashed_password
        
        return super().update(instance, validated_data)
    
class SupervisorSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Ensure password is not returned in responses

    class Meta:
        model = Supervisor
        fields = ['supervisor_id', 'supervisor_name', 'department', 'email', 'gender', 'supervisor_image', 'shift', 'dob', 'hired_date', 'username', 'password']
    
    def validate_password(self, value):
        """
        Custom password validator to use Django's built-in validation.
        """
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError({
                'password': e.messages
            })
        return value

    def create(self, validated_data):
        """
        Overridden create method to hash the password before saving the manager.
        """
        raw_password = validated_data.pop('password')  # Remove password from validated data
        try:
            # Ensure password meets complexity requirements
            self.validate_password(raw_password)
        except serializers.ValidationError as e:
            raise e  # Propagate the error if validation fails
        
        # Hash password using bcrypt
        hashed_password = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        validated_data['password'] = hashed_password  # Store the hashed password
        
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        If the password is being updated, hash the new password before saving.
        """
        if 'password' in validated_data:
            raw_password = validated_data.pop('password')
            hashed_password = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            validated_data['password'] = hashed_password
        
        return super().update(instance, validated_data)    

class EmployeeSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Ensure password is not returned in responses

    class Meta:
        model = Employee
        fields = ['employee_id', 'employee_name', 'department', 'email', 'gender', 'employee_image', 'shift', 'dob', 'hired_date', 'username', 'password']
    
    def validate_password(self, value):
        """
        Custom password validator to use Django's built-in validation.
        """
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError({
                'password': e.messages
            })
        return value

    def create(self, validated_data):
        """
        Overridden create method to hash the password before saving the manager.
        """
        raw_password = validated_data.pop('password')  # Remove password from validated data
        try:
            # Ensure password meets complexity requirements
            self.validate_password(raw_password)
        except serializers.ValidationError as e:
            raise e  # Propagate the error if validation fails
        
        # Hash password using bcrypt
        hashed_password = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        validated_data['password'] = hashed_password  # Store the hashed password
        
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        If the password is being updated, hash the new password before saving.
        """
        if 'password' in validated_data:
            raw_password = validated_data.pop('password')
            hashed_password = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            validated_data['password'] = hashed_password
        
        return super().update(instance, validated_data)

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['department_id', 'department_name']

class ShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shift
        fields = ['shift_number', 'shift_start_time', 'shift_end_time']

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['location_id', 'location_name']

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    user_id = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=255, write_only=True)

class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, write_only=True)
    
from rest_framework import serializers
from .models import Todo, News, Ticket, Req, Requests

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['id', 'title', 'completed', 'created_on']

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ['id', 'title', 'content', 'date', 'created_date']

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = [
            'id', 'title', 'description', 'created_on', 'last_updated',
            'created_by', 'Reciver', 'assigned_to', 'status', 'proof'
        ]

class ReqSerializer(serializers.ModelSerializer):
    class Meta:
        model = Req
        fields = ['id', 'title', 'description']

class RequestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requests
        fields = [
            'id', 'employee', 'supervisor', 'admin', 'title', 'request_ticket_id',
            'description', 'status', 'admin_status', 'created_on', 'updated_on'
        ]
    
