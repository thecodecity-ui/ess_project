# Generated by Django 5.0.6 on 2024-12-22 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0005_managerdocument'),
    ]

    operations = [
        migrations.CreateModel(
            name='SupervisorDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=30)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('aadhar_card', models.FileField(blank=True, null=True, upload_to='documents/aadhar/')),
                ('pan_card', models.FileField(blank=True, null=True, upload_to='documents/pan/')),
                ('bank_details', models.FileField(blank=True, null=True, upload_to='documents/bank/')),
                ('previous_payslip', models.FileField(blank=True, null=True, upload_to='documents/payslip/')),
                ('experience_certificate', models.FileField(blank=True, null=True, upload_to='documents/experience/')),
                ('degree_certificate', models.FileField(blank=True, null=True, upload_to='documents/degree/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
