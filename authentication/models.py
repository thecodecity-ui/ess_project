import random
from django.db import models

class Admin(models.Model):
    username = models.CharField(max_length=100)
    user_id = models.CharField(max_length=100,unique=True)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    reset_token = models.CharField(max_length=255, null=True, blank=True)
    token_expiration = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.email
    
class ManagingDirector(models.Model):
    username = models.CharField(max_length=100)
    user_id = models.CharField(max_length=100, unique=True)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    reset_token = models.CharField(max_length=255, null=True, blank=True)
    token_expiration = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.email

class Department(models.Model):
    department_id = models.CharField(max_length=50, unique=True)
    department_name = models.CharField(max_length=100)

    def __str__(self):
        return self.department_name

class Shift(models.Model):
    shift_number = models.CharField(max_length=50, unique=True)
    shift_start_time = models.TimeField()
    shift_end_time = models.TimeField()

    def __str__(self):
        return self.shift_number

class Manager(models.Model):
    manager_id = models.CharField(max_length=100, unique=True)
    manager_name = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)  # ForeignKey to Department
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=10)
    manager_image = models.ImageField(upload_to='manager_images/')
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)  # ForeignKey to Shift
    dob = models.DateField()
    hired_date = models.DateField()
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255) 
    role = models.CharField(max_length=50, default='manager')
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    state = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    pincode = models.CharField(max_length=10, null=True, blank=True)
    linkedin_profile_link = models.URLField(null=True, blank=True)  
    reset_token = models.CharField(max_length=64, blank=True, null=True)
    token_expiration = models.DateTimeField(blank=True, null=True)

    @property
    def department_name(self):
        return self.department.department_name

    def __str__(self):
        return self.manager_name 
    
class Employee(models.Model):
    employee_id = models.CharField(max_length=50, unique=True)
    employee_name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    email = models.EmailField()
    gender = models.CharField(max_length=10)
    employee_image = models.ImageField(upload_to='employee_images/', null=True, blank=True)
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)
    dob = models.DateField()
    hired_date = models.DateField()
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=50, default='employee')  
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    state = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    pincode = models.CharField(max_length=10, null=True, blank=True)
    linkedin_profile_link = models.URLField(null=True, blank=True)   
    reset_token = models.CharField(max_length=64, blank=True, null=True)
    token_expiration = models.DateTimeField(blank=True, null=True)

    @property
    def department_name(self):
        return self.department.department_name

    def __str__(self):
        return self.employee_name
    
class Supervisor(models.Model):
    supervisor_id = models.CharField(max_length=100, unique=True)
    supervisor_name = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)  # ForeignKey to Department
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=10)
    supervisor_image = models.ImageField(upload_to='supervisor_images/')
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)  # ForeignKey to Shift
    dob = models.DateField()
    hired_date = models.DateField()
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255) 
    role = models.CharField(max_length=50, default='supervisor')
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    state = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    pincode = models.CharField(max_length=10, null=True, blank=True)
    linkedin_profile_link = models.URLField(null=True, blank=True)  
    reset_token = models.CharField(max_length=64, blank=True, null=True)
    token_expiration = models.DateTimeField(blank=True, null=True)

    @property
    def department_name(self):
        return self.department.department_name

    def __str__(self):
        return self.supervisor_name    
    

class Location(models.Model):
    location_id = models.CharField(max_length=50, unique=True)
    location_name = models.CharField(max_length=100)

    def __str__(self):
        return self.location_name
    
class Todo(models.Model):
    title=models.CharField(max_length=255)
    completed=models.BooleanField(default=False)
    created_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()  # Use TextField instead of CharField for larger content
    date = models.DateField()  # Date when the news was created
    created_date = models.DateTimeField(auto_now_add=True)  # Automatically set on news creation

    def _str_(self):
        return self.title

#helpdesk 

class Ticket(models.Model):
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('Closed', 'Closed'),
        ('In Progress', 'In Progress'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="created_tickets" , null=True)
    Reciver= models.TextField()
    assigned_to = models.ForeignKey(Manager, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_tickets")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Open')
    proof = models.FileField(upload_to='ticket_proofs/', null=True, blank=True)

    def __str__(self):
        return self.title
    
class Req(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title
    

class Requests(models.Model):
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE)
    supervisor = models.ForeignKey('Supervisor', on_delete=models.SET_NULL, null=True, blank=True)
    admin = models.ForeignKey('Admin', on_delete=models.SET_NULL, null=True, blank=True)  # Add admin field
    title = models.CharField(max_length=255)
    request_ticket_id = models.CharField(max_length=4, unique=True, null=False)

    def save(self, *args, **kwargs):
        if not self.request_ticket_id:
            # Generate a random 4-digit unique ticket ID
            while True:
                ticket_id = f"{random.randint(1000, 9999)}"
                if not Requests.objects.filter(request_ticket_id=ticket_id).exists():
                    self.request_ticket_id = ticket_id
                    break
        super().save(*args, **kwargs)

    description = models.TextField()
    status = models.CharField(
        max_length=50,
        choices=[
            ('Pending', 'Pending'),
            ('Approved', 'Approved'),
            ('Rejected', 'Rejected'),
            ('Forwarded', 'Forwarded'),
        ],
        default='Pending'
    )

    admin_status = models.CharField (
        max_length=50,
        choices=[
            ('Pending', 'Pending'),
            ('Approved', 'Approved'),
            ('Rejected', 'Rejected'),
        ],
        default='Pending'
    )

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.status}"

    