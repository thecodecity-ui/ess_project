from django.db import models
from datetime import timedelta

from authentication.models import Employee, Manager


class LeaveRequest(models.Model):
    LEAVE_TYPE_CHOICES = [
        ('medical', 'Medical'),
        ('vacation', 'Vacation'),
        ('personal', 'Personal'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    
    start_date = models.DateField()
    end_date = models.DateField()
    leave_type = models.CharField(max_length=10, choices=LEAVE_TYPE_CHOICES)
    reason = models.TextField()
    leave_proof = models.FileField(upload_to='media/leave_proof/',blank=True, null=True)
    user = models.CharField(max_length=100)
    user_id = models.CharField(max_length=100)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')# Adjust as per your user model
    email = models.EmailField()
    notification_sent = models.BooleanField(default=False)
    calendar_link = models.URLField(blank=True, null=True)
   # Add this line for storing total days

    def __str__(self):
        return f"{self.user} - {self.leave_type} from {self.start_date} to {self.end_date}"

    @property
    def total_days(self):
        total_days = (self.end_date - self.start_date).days + 1
    # Count the number of Sundays in the leave period
        sundays = sum(1 for i in range(total_days) if (self.start_date + timedelta(days=i)).weekday() == 6)
        return total_days - sundays
# Model for leave requests

    
class Notification(models.Model):
    user = models.CharField(max_length=20)
    date = models.DateField()
    time = models.TimeField()
    message = models.TextField(max_length=300)
    
    
    def __str__(self):
        return f"Notification for {self.user} on {self.date} at {self.time}"
    
class ApplyNotification(models.Model):
    user = models.CharField(max_length=20)
    date = models.DateField()
    time = models.TimeField()
    message = models.TextField(max_length=300)
    
    
    def __str__(self):
        return f"Notification for {self.user} on {self.date} at {self.time}"
        


class LeaveBalance(models.Model):
    user = models.CharField(max_length=20, unique=True)
    medical_leave = models.PositiveIntegerField(default=0)  # Remaining leave balance
    vacation_leave = models.PositiveIntegerField(default=0)  # Remaining leave balance
    personal_leave = models.PositiveIntegerField(default=0)  # Remaining leave balance
    total_leave_days = models.PositiveIntegerField(default=0)  # Remaining leave balance
    total_absent_days = models.PositiveIntegerField(default=0)  # Total absent days

    def __str__(self):
        return f"{self.user} - Balance: {self.total_leave_days} days, Absent: {self.total_absent_days} days"

    # Add method to update total absent days
    def update_total_absent_days(self, days):
        self.total_absent_days += days
        self.save()

    # Method to recalculate total leave days
    def recalculate_total_leave_days(self):
        self.total_leave_days = self.medical_leave + self.vacation_leave + self.personal_leave
        self.save()


class ManagerLeaveRequest(models.Model):
    LEAVE_TYPE_CHOICES = [
        ('medical', 'Medical'),
        ('vacation', 'Vacation'),
        ('personal', 'Personal'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    start_date = models.DateField()
    end_date = models.DateField()
    leave_type = models.CharField(max_length=10, choices=LEAVE_TYPE_CHOICES)
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    user =models.CharField(max_length=20,default=None)
    user_id =models.CharField(max_length=20)
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField(max_length=30, null=False)    
    manager_notification_sent = models.BooleanField(default=False)  # New field for notification status

    
    
    
    
    def __str__(self):
        return f"{self.user} - {self.leave_type} from {self.start_date} to {self.end_date}"

    @property
    def total_days(self):
        total_days = (self.end_date - self.start_date).days + 1
    # Count the number of Sundays in the leave period
        sundays = sum(1 for i in range(total_days) if (self.start_date + timedelta(days=i)).weekday() == 6)
        return total_days - sundays
# Model for leave requests
    
class ManagerNotification(models.Model):
    user = models.CharField(max_length=20)
    date = models.DateField()
    time = models.TimeField()
    message = models.TextField(max_length=300)
    
    def __str__(self):
        return f"Notification for {self.user} on {self.date} at {self.time}"
    
class ManagerApplyNotification(models.Model):
    user = models.CharField(max_length=20)
    date = models.DateField()
    time = models.TimeField()
    message = models.TextField(max_length=300)
    
    
    def __str__(self):
        return f"Notification for {self.user} on {self.date} at {self.time}"    

from authentication.models import Supervisor 

# Optional: Model to track leave balance (if required)
class ManagerLeaveBalance(models.Model):
    user = models.CharField(max_length=20, unique=True)
    total_leave_days = models.PositiveIntegerField(default=0)  # Default value or adjust as needed

    def __str__(self):
        return f"{self.user} - {self.total_leave_days} days"


class SupervisorLeaveRequest(models.Model):
    LEAVE_TYPE_CHOICES = [
        ('medical', 'Medical'),
        ('vacation', 'Vacation'),
        ('personal', 'Personal'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    start_date = models.DateField()
    end_date = models.DateField()
    leave_type = models.CharField(max_length=10, choices=LEAVE_TYPE_CHOICES)
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    user =models.CharField(max_length=20,default=None)
    user_id =models.CharField(max_length=20)
    supervisor = models.ForeignKey(Supervisor, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField(max_length=30, null=False)    
    supervisor_notification_sent = models.BooleanField(default=False)  # New field for notification status

    def __str__(self):
        return f"{self.user} - {self.leave_type} from {self.start_date} to {self.end_date}"

    @property
    def total_days(self):
        total_days = (self.end_date - self.start_date).days + 1
    # Count the number of Sundays in the leave period
        sundays = sum(1 for i in range(total_days) if (self.start_date + timedelta(days=i)).weekday() == 6)
        return total_days - sundays
# Model for leave requests
    
    
class SupervisorNotification(models.Model):
    user = models.CharField(max_length=20)
    date = models.DateField()
    time = models.TimeField()
    message = models.TextField(max_length=300)
    
    def __str__(self):
        return f"Notification for {self.user} on {self.date} at {self.time}"
    
class SupervisorApplyNotification(models.Model):
    user = models.CharField(max_length=20)
    date = models.DateField()
    time = models.TimeField()
    message = models.TextField(max_length=300)
    
    def __str__(self):
        return f"Notification for {self.user} on {self.date} at {self.time}"     

# Optional: Model to track leave balance (if required)
class SupervisorLeaveBalance(models.Model):
    user = models.CharField(max_length=20, unique=True)
    total_leave_days = models.PositiveIntegerField(default=0)  # Default value or adjust as needed

    def __str__(self):
        return f"{self.user} - {self.total_leave_days} days"
