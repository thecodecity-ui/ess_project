from rest_framework import serializers
from .models import TaskLog, Task
from .models import employee_task
from .models import Project
from .models import Task, Manager
from .models import TrainingProgram
from .models import TrainingParticipation
from rest_framework import serializers
from .models import TrainingProgram, TrainingParticipation
from rest_framework import serializers
from .models import TrainingProgram
from rest_framework import serializers
from .models import  Employee, Manager
from kpi.models import PerformanceReview, Goal, Feedback
from django.db import models
from .models import TrainingProgram, TrainingParticipation
from .models import Certification
from django.utils import timezone

class TaskLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskLog
        fields = ['id', 'task', 'employee', 'manager', 'check_in_time', 'check_out_time', 'hours_worked']

    def validate(self, data):
        # Custom validation (if needed) can be added here
        return data

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['task_id', 'task_name', 'description', 'priority', 'start_date', 'deadline', 'status', 'manager']

class EmployeeTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = employee_task
        fields = '__all__'  # You can list specific fields here if needed

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'  # You can specify the fields you want here instead of '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['project_id', 'name', 'description', 'start_date', 'deadline', 'project_manager']


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'task_id', 
            'project_name', 
            'task_name', 
            'description', 
            'priority', 
            'start_date', 
            'deadline', 
            'project_manager'
        ]

    def validate_project_manager(self, value):
        try:
            # Ensure the manager exists in the database
            manager = Manager.objects.get(manager_name=value)
        except Manager.DoesNotExist:
            raise serializers.ValidationError("Manager not found")
        return value

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['task_id', 'task_name', 'project_name', 'status', 'start_date', 'deadline']

class TrainingProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingProgram
        fields = '__all__'  # List all fields or define specific ones


class ParticipationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingParticipation
        fields = '__all__'  # List all fields or specify them as needed




class TrainingProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingProgram
        fields = '__all__'  # or specify fields if needed

class TrainingParticipationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingParticipation
        fields = '__all__'  # or specify fields if needed



class TrainingProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingProgram
        fields = '__all__'


class TrainingProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingProgram
        fields = '__all__'

class TrainingParticipationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingParticipation
        fields = '__all__'




class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = ['certificate_file', 'employee', 'program', 'date_uploaded'] 
         # Adjust the fields according to your model



# Serializer for PerformanceReview
class PerformanceReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerformanceReview
        fields = ['id', 'employee', 'manager', 'review_date', 'comments', 'score']
        read_only_fields = ['review_date']

    # To add employee and manager names as readable fields
    employee_name = serializers.CharField(source='employee.employee_name', read_only=True)
    manager_username = serializers.CharField(source='manager.username', read_only=True)

    def create(self, validated_data):
        # Automatically assigns the review date to current time when creating a performance review
        validated_data['review_date'] = timezone.now()
        return super().create(validated_data)


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ['id', 'employee', 'goal_text', 'start_date', 'end_date']

    employee_name = serializers.CharField(source='employee.employee_name', read_only=True)


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['id', 'from_manager', 'to_employee', 'feedback_date', 'comments']
        read_only_fields = ['feedback_date']

    from_manager_name = serializers.CharField(source='from_manager.username', read_only=True)
    to_employee_name = serializers.CharField(source='to_employee.employee_name', read_only=True)

