from rest_framework import serializers
from .models import PayrollManagement, PayrollNotification, ManagerPayrollNotification, SupervisorPayrollNotification
from .models import Salary, BonusType

class PayrollManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayrollManagement
        fields = [
            'id', 'user', 'user_id', 'month', 'email', 
            'base_salary', 'net_salary', 'total_working_hours', 
            'overtime_hours', 'overtime_pay', 'pdf_path'
        ]


class PayrollNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayrollNotification
        fields = [
            'id', 'user', 'user_id', 'date', 'time', 'message'
        ]


class ManagerPayrollNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagerPayrollNotification
        fields = [
            'id', 'user', 'user_id', 'date', 'time', 'message'
        ]


class SupervisorPayrollNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupervisorPayrollNotification
        fields = [
            'id', 'user', 'user_id', 'date', 'time', 'message'
        ]




class SalarySerializer(serializers.ModelSerializer):
    # Additional read-only fields if required
    total_salary = serializers.CharField(read_only=True)
    monthly_salary = serializers.CharField(read_only=True)

    class Meta:
        model = Salary
        fields = [
            'id', 'user_id', 'annual_salary', 'bonus', 
            'total_salary', 'monthly_salary', 
            'effective_date', 'updated_date'
        ]


class BonusTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BonusType
        fields = [
            'id', 'user_id', 'bonus_type', 'amount', 
            'due_date', 'paid_status', 'total_paid'
        ]