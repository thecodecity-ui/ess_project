# Generated by Django 5.0.6 on 2024-12-24 09:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplyNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=20)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('message', models.TextField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='LeaveBalance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=20, unique=True)),
                ('medical_leave', models.PositiveIntegerField(default=0)),
                ('vacation_leave', models.PositiveIntegerField(default=0)),
                ('personal_leave', models.PositiveIntegerField(default=0)),
                ('total_leave_days', models.PositiveIntegerField(default=0)),
                ('total_absent_days', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='ManagerApplyNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=20)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('message', models.TextField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='ManagerLeaveBalance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=20, unique=True)),
                ('total_leave_days', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='ManagerNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=20)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('message', models.TextField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=20)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('message', models.TextField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='SupervisorApplyNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=20)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('message', models.TextField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='SupervisorLeaveBalance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=20, unique=True)),
                ('total_leave_days', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='SupervisorNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=20)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('message', models.TextField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='LeaveRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('leave_type', models.CharField(choices=[('medical', 'Medical'), ('vacation', 'Vacation'), ('personal', 'Personal')], max_length=10)),
                ('reason', models.TextField()),
                ('leave_proof', models.FileField(blank=True, null=True, upload_to='media/leave_proof/')),
                ('user', models.CharField(max_length=100)),
                ('user_id', models.CharField(max_length=100)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=10)),
                ('email', models.EmailField(max_length=254)),
                ('notification_sent', models.BooleanField(default=False)),
                ('calendar_link', models.URLField(blank=True, null=True)),
                ('employee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='authentication.employee')),
            ],
        ),
        migrations.CreateModel(
            name='ManagerLeaveRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('leave_type', models.CharField(choices=[('medical', 'Medical'), ('vacation', 'Vacation'), ('personal', 'Personal')], max_length=10)),
                ('reason', models.TextField()),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=10)),
                ('user', models.CharField(default=None, max_length=20)),
                ('user_id', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=30)),
                ('manager_notification_sent', models.BooleanField(default=False)),
                ('manager', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='authentication.manager')),
            ],
        ),
        migrations.CreateModel(
            name='SupervisorLeaveRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('leave_type', models.CharField(choices=[('medical', 'Medical'), ('vacation', 'Vacation'), ('personal', 'Personal')], max_length=10)),
                ('reason', models.TextField()),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=10)),
                ('user', models.CharField(default=None, max_length=20)),
                ('user_id', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=30)),
                ('supervisor_notification_sent', models.BooleanField(default=False)),
                ('supervisor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='authentication.supervisor')),
            ],
        ),
    ]
