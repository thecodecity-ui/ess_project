from datetime import datetime,date
import mimetypes
from django.db import models
from django.contrib.auth.models import User
from authentication.models import Manager,Employee
from ess import settings
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils import timezone

class Project(models.Model):
    project_id=models.IntegerField()
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    deadline = models.DateField()
    project_manager=models.CharField(max_length=100)
    project_status=models.CharField(max_length=50,default='not_started')
    completion_date = models.DateTimeField(null=True, blank=True)# Date when the task is marked as completed
    completion_reason = models.TextField(null=True, blank=True)
    

    def __str__(self):
        return self.name

    def is_late(self):
        if self.completion_date:
            # Convert the deadline to a timezone-aware datetime
            deadline_datetime = timezone.make_aware(datetime.combine(self.deadline, datetime.min.time()))
            return self.completion_date > deadline_datetime
        return False 
    
    


class Task(models.Model):
    STATUS_CHOICES = [
        ('not started', 'Not Started'),
        ('in progress', 'In Progress'),
        ('in review', 'In Review'),
        ('completed', 'Completed'),
    ]

    
    task_id=models.IntegerField(unique=True) 
    task_name = models.CharField(max_length=100)
    description = models.TextField()
    priority = models.CharField(max_length=10, choices=[('high', 'High'), ('medium', 'Medium'), ('low', 'Low')])
    start_date = models.DateField()
    deadline = models.DateField()
    project_manager = models.CharField(max_length=100)
    project_name= models.CharField(max_length=100)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='not started')
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE, related_name='tasks')
    completion_date = models.DateTimeField(null=True, blank=True)# Date when the task is marked as completed
    completion_reason = models.TextField(null=True, blank=True)  # Reason for late completion

    def __str__(self):
        return self.task_name
    
    def is_late(self):
        if self.completion_date:
            # Convert the deadline to a timezone-aware datetime
            deadline_datetime = timezone.make_aware(datetime.combine(self.deadline, datetime.min.time()))
            return self.completion_date > deadline_datetime
        return False
    
    @staticmethod
    def calculate_manager_performance(manager_name):
        total_tasks = Task.objects.filter(manager__username=manager_name).count()
        completed_tasks = Task.objects.filter(manager__username=manager_name, status='completed').count()
        if total_tasks > 0:
            return (completed_tasks / total_tasks) * 100
        return 0


   
    


class Role(models.Model):
    role_id = models.CharField(max_length=50)
    role_name=models.CharField(max_length=100)


class Team(models.Model):
    team_id=models.CharField(max_length=50 )
    team_name = models.CharField(max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='teams')
    team_task = models.CharField(max_length=100)
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE, related_name='teams')
    team_leader = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='led_teams')
    members = models.ManyToManyField(Employee, related_name="team_members")
    
class employee_task(models.Model):
    STATUS_CHOICES = [
        ('not started', 'Not Started'),
        ('in progress', 'In Progress'),
        ('in review', 'In Review'),
        ('completed', 'Completed'),  # Optional: Add a 'completed' status if needed
    ]
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE, null=True, blank=True)
    team_name = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)
    project_name = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    emptask_id = models.CharField(max_length=50, blank=True, null=True)  # Task ID
    task_name = models.CharField(max_length=50)
    task_description = models.CharField(max_length=100)
    assigned_to = models.CharField(max_length=50)
    deadline = models.DateField()
    emp_taskstatus = models.CharField(max_length=100, choices=STATUS_CHOICES, default='not started')
    completion_date = models.DateTimeField(null=True, blank=True)  # Date when the task is completed
    completion_reason = models.TextField(null=True, blank=True)  # Reason for task delays
    


    def __str__(self):
        return self.task_name

    def is_late(self):
        if self.completion_date:
            # Convert the deadline to a timezone-aware datetime
            deadline_datetime = timezone.make_aware(datetime.combine(self.deadline, datetime.min.time()))
            return self.completion_date > deadline_datetime
        return False
    
    
    @staticmethod
    def calculate_employee_performance(employee_name):
        total_tasks = employee_task.objects.filter(assigned_to=employee_name).count()
        completed_tasks = employee_task.objects.filter(assigned_to=employee_name, emp_taskstatus='completed').count()
        if total_tasks > 0:
            return (completed_tasks / total_tasks) * 100
        return 0

class TaskLog(models.Model):
    task=models.ForeignKey(Task, on_delete=models.CASCADE, related_name='task_logs', null=True, blank=True)
    employeetask=models.ForeignKey(employee_task, on_delete=models.CASCADE, related_name='task_logs', null=True, blank=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='task_logs', null=True, blank=True)
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE, related_name='task_logs', null=True, blank=True)
    check_in_time = models.DateTimeField()
    check_out_time = models.DateTimeField(null=True)
    hours_worked = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def calculate_hours_worked(self):
        if self.check_in_time and self.check_out_time:
            delta = self.check_out_time - self.check_in_time
            # Calculate hours as a decimal (e.g., 1 hour 30 minutes = 1.5 hours)
            self.hours_worked = delta.total_seconds() / 3600
            self.save()


class TaskDocument(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="documents")
    uploaded_by = models.CharField(max_length=50)
    document = models.FileField(upload_to='task_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class TaskEmpDocument(models.Model):
    employee_task = models.ForeignKey(employee_task, on_delete=models.CASCADE, related_name="documents")
    uploaded_by = models.CharField(max_length=50)
    document = models.FileField(upload_to='task_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
   
# training models
class TrainingProgram(models.Model):
    program_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    for_managers = models.BooleanField(default=False)  # True if this program is for managers
    for_employees = models.BooleanField(default=True)  # True if this program is for employees
    training_incharge = models.ForeignKey(Manager, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class TrainingParticipation(models.Model):
    program = models.ForeignKey(TrainingProgram, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True)
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE, null=True, blank=True)
    completion_status = models.CharField(max_length=20, choices=[('not_started', 'Not Started'), ('in_progress', 'In Progress'), ('completed', 'Completed')], default='not_started')
    completion_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.program.name} - {self.employee or self.manager}"


class Certification(models.Model):
    participation = models.OneToOneField(TrainingParticipation, on_delete=models.CASCADE)
    certification_name = models.CharField(max_length=255)
    certification_date = models.DateField()
    certification_file = models.FileField(upload_to='certificates/')
    
    def __str__(self):
        return f"Certification for {self.participation.employee or self.participation.manager}"
   
    
    def send_certificate_email(self):
        email = EmailMessage(
            subject='Certification Received: {}'.format(self.certification_name),
            body='Dear {},\n\nYou have received the {} certification for completing the training program on {}.'.format(self.participation.employee.employee_name if self.participation.employee else self.participation.manager.manager_name, self.certification_name, self.certification_date),
            from_email=settings.EMAIL_HOST_USER,
            to=[self.participation.employee.email if self.participation.employee else self.participation.manager.email],
        )
        
        # Get the content type
        content_type = mimetypes.guess_type(self.certification_file.name)[0] or 'application/octet-stream'
        
        email.attach(self.certification_file.name, self.certification_file.read(), content_type)
        email.send()