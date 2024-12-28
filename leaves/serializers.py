from rest_framework import serializers
from .models import (
    LeaveRequest, Notification, ApplyNotification, LeaveBalance,
    ManagerLeaveRequest, ManagerNotification, ManagerApplyNotification, ManagerLeaveBalance,
    SupervisorLeaveRequest, SupervisorNotification, SupervisorApplyNotification, SupervisorLeaveBalance
)

class LeaveRequestSerializer(serializers.ModelSerializer):
    total_days = serializers.ReadOnlyField()

    class Meta:
        model = LeaveRequest
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

class ApplyNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplyNotification
        fields = '__all__'

class LeaveBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveBalance
        fields = '__all__'

class ManagerLeaveRequestSerializer(serializers.ModelSerializer):
    total_days = serializers.ReadOnlyField()

    class Meta:
        model = ManagerLeaveRequest
        fields = '__all__'

class ManagerNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagerNotification
        fields = '__all__'

class ManagerApplyNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagerApplyNotification
        fields = '__all__'

class ManagerLeaveBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagerLeaveBalance
        fields = '__all__'

class SupervisorLeaveRequestSerializer(serializers.ModelSerializer):
    total_days = serializers.ReadOnlyField()

    class Meta:
        model = SupervisorLeaveRequest
        fields = '__all__'

class SupervisorNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupervisorNotification
        fields = '__all__'

class SupervisorApplyNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupervisorApplyNotification
        fields = '__all__'

class SupervisorLeaveBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupervisorLeaveBalance
        fields = '__all__'
