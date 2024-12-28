import datetime
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from ess import settings
from projectmanagement.models import Project, Task, Role, TaskDocument,Team,employee_task,TaskEmpDocument,TaskLog
from authentication.models import Admin, Manager, Department, Shift, Employee, Location
from django.db.models import Sum,Count
from django.core.files.storage import FileSystemStorage
from .models import TrainingProgram, TrainingParticipation, Certification
from .forms import CertificationForm, TrainingProgramForm, ParticipationForm
from django.core.mail import send_mail
from django.utils import timezone  # Import timezone from django.utils
from django.utils.timezone import now
from datetime import timedelta
from django.shortcuts import render
from .models import employee_task
import json
from django.contrib import messages
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import TaskLog
from .serializers import TaskLogSerializer
from django.utils.timezone import now
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import employee_task
from .serializers import EmployeeTaskSerializer 
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer 
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Project
from .serializers import ProjectSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Project
from .serializers import ProjectSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Project, Task, employee_task
from .serializers import ProjectSerializer, TaskSerializer, EmployeeTaskSerializer 
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Project
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Task, Manager
from .serializers import TaskSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Task
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Task
from .serializers import TaskSerializer
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Task, Manager
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Task, Manager
from .serializers import TaskSerializer
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Role
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Role
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Team, Project, Manager, Employee
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Team
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Team, Project, Manager, Employee
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Manager, Team
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import employee_task, Team, Manager
from django.contrib import messages
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import employee_task
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Task
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import employee_task, Employee
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import employee_task
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Manager, Project
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import Project
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Project
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Project
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Project
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Task, TaskDocument
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import employee_task, TaskEmpDocument
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import TaskDocument, TaskEmpDocument, employee_task, Task
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import TrainingProgram
from .serializers import TrainingProgramSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import TrainingParticipation
from .serializers import ParticipationSerializer  # Ensure you have this serializer
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import TrainingProgram, TrainingParticipation
from .serializers import TrainingProgramSerializer, TrainingParticipationSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import TrainingProgram
from .serializers import TrainingProgramSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import TrainingParticipation
from .serializers import TrainingParticipationSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import CertificationSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Certification
from .serializers import CertificationSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import TrainingProgram, TrainingParticipation, Manager, Employee
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum, Count
from django.utils.timezone import now
from datetime import timedelta
from .models import TaskLog
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from .models import TaskLog, Employee, Manager, Task, employee_task
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Project, Task, employee_task, Manager
from django.contrib import messages
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Task, Project, Manager
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Role
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Team, Project, Manager, Employee
from django.core.exceptions import ValidationError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Project
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Project
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Project
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import TaskDocument, TaskEmpDocument
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import employee_task
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Task
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import TrainingProgram
from .serializers import TrainingProgramSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import TrainingParticipation
from .serializers import TrainingParticipationSerializer
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Certification
from .serializers import CertificationSerializer
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum, Count
from django.utils.timezone import now
from .models import TaskLog, Employee, Manager
from datetime import timedelta
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Employee, Manager
from django.utils import timezone
from authentication.models import Employee, Manager ,Supervisor
from kpi.models import PerformanceReview,Goal, Feedback,ManagerPerformanceReview,ManagerGoal,ManagerFeedback,OverallFeedback

@api_view(['POST'])
def emp_check_in(request):
    """
    Check-in an employee to a task.
    """
    # Check if there's already an active task without check-out time
    active_task = TaskLog.objects.filter(check_out_time__isnull=True).exists()
    if active_task:
        return Response({"detail": "You have already checked in to a task. Please check out before starting a new task."},
                        status=status.HTTP_400_BAD_REQUEST)

    # Create a new TaskLog entry with the current check-in time
    task_log = TaskLog.objects.create(check_in_time=now())
    
    # Serialize the TaskLog object and return the response
    serializer = TaskLogSerializer(task_log)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def emp_check_out(request):
    """
    Check-out an employee from a task.
    """
    try:
        # Get the TaskLog with no check-out time
        task_log = TaskLog.objects.get(check_out_time__isnull=True)
    except ObjectDoesNotExist:
        return Response({"detail": "This task has already been checked out or was never checked in."},
                        status=status.HTTP_400_BAD_REQUEST)

    # Set check-out time and calculate worked hours
    task_log.check_out_time = now()
    task_log.calculate_hours_worked()  # Calculate hours worked and update the entry
    task_log.save()

    # Serialize the TaskLog object and return the response
    serializer = TaskLogSerializer(task_log)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def assigned_task(request):
    if request.method == 'POST':
        # Handle POST request to update task status
        data = request.data
        task_id = data.get('task_id')
        new_status = data.get('status')

        try:
            task = employee_task.objects.get(id=task_id)
            task.emp_taskstatus = new_status
            task.save()
            return Response({'success': True})
        except employee_task.DoesNotExist:
            return Response({'success': False, 'error': 'Task not found'}, status=404)
    
    elif request.method == 'GET':
        # Handle GET request to fetch tasks by status
        not_started_projects = employee_task.objects.filter(emp_taskstatus='not started')
        in_progress_projects = employee_task.objects.filter(emp_taskstatus='in progress')
        in_review_projects = employee_task.objects.filter(emp_taskstatus='in review')
        completed_projects = employee_task.objects.filter(emp_taskstatus='completed')

        # Serialize the task data
        not_started_serializer = EmployeeTaskSerializer(not_started_projects, many=True)
        in_progress_serializer = EmployeeTaskSerializer(in_progress_projects, many=True)
        in_review_serializer = EmployeeTaskSerializer(in_review_projects, many=True)
        completed_serializer = EmployeeTaskSerializer(completed_projects, many=True)

        # Return the tasks as JSON
        return Response({
            'not_started_projects': not_started_serializer.data,
            'in_progress_projects': in_progress_serializer.data,
            'in_review_projects': in_review_serializer.data,
            'completed_projects': completed_serializer.data,
        })




@api_view(['POST', 'GET'])
def assigned_manager_task(request):
    if request.method == 'POST':
        # Handle POST request to update task status
        data = request.data
        ptask_id = data.get('task_id')
        new_status = data.get('status')

        try:
            task = Task.objects.get(id=ptask_id)
            task.status = new_status
            task.save()
            return Response({'success': True})
        except Task.DoesNotExist:
            return Response({'success': False, 'error': 'Task not found'}, status=404)
    
    elif request.method == 'GET':
        # Handle GET request to fetch tasks by status
        not_started_projects = Task.objects.filter(status='not started')
        in_progress_projects = Task.objects.filter(status='in progress')
        in_review_projects = Task.objects.filter(status='in review')
        completed_projects = Task.objects.filter(status='completed')

        # Serialize the task data
        not_started_serializer = TaskSerializer(not_started_projects, many=True)
        in_progress_serializer = TaskSerializer(in_progress_projects, many=True)
        in_review_serializer = TaskSerializer(in_review_projects, many=True)
        completed_serializer = TaskSerializer(completed_projects, many=True)

        # Return the tasks as JSON
        return Response({
            'not_started_projects': not_started_serializer.data,
            'in_progress_projects': in_progress_serializer.data,
            'in_review_projects': in_review_serializer.data,
            'completed_projects': completed_serializer.data,
        })


  # Assuming you have a serializer for Project

@api_view(['POST'])
def create_project(request):
    if request.method == 'POST':
        # Extract project data from the request body
        project_data = request.data
        
        # Create a new Project instance and populate fields
        serializer = ProjectSerializer(data=project_data)
        
        if serializer.is_valid():
            serializer.save()  # Save the project instance
            return Response({'success': True, 'message': 'Project created successfully!'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def edit_project(request, project_id):
    try:
        project = Project.objects.get(project_id=project_id)
    except Project.DoesNotExist:
        return Response({'success': False, 'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Update project with data from the request
    if request.method == 'PUT':
        serializer = ProjectSerializer(project, data=request.data)

        if serializer.is_valid():
            serializer.save()  # Save the updated project instance
            return Response({'success': True, 'message': 'Project updated successfully!'}, status=status.HTTP_200_OK)
        else:
            return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def show_project_status(request, project_id):
    try:
        project = Project.objects.get(project_id=project_id)
    except Project.DoesNotExist:
        return Response({'success': False, 'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)
    
    tasks = Task.objects.filter(project_name=project.name)
    emptasks = employee_task.objects.filter(team_project_name=project.name)
    
    # Serialize the data
    project_serializer = ProjectSerializer(project)
    tasks_serializer = TaskSerializer(tasks, many=True)
    emptasks_serializer = EmployeeTaskSerializer(emptasks, many=True)
    
    return Response({
        'project': project_serializer.data,
        'tasks': tasks_serializer.data,
        'emptasks': emptasks_serializer.data
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
def delete_project(request, project_id):
    try:
        # Try to retrieve the project by its ID
        project = Project.objects.get(project_id=project_id)
        project.delete()  # Delete the project
        return Response({'success': True, 'message': 'Project deleted successfully!'}, status=status.HTTP_200_OK)
    except Project.DoesNotExist:
        return Response({'success': False, 'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def create_task(request):
    # Deserialize the incoming data
    serializer = TaskSerializer(data=request.data)
    
    # Check if the data is valid
    if serializer.is_valid():
        try:
            # Save the task if valid
            serializer.save()
            return Response({'success': True, 'message': 'Task created successfully!'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    else:
        # If validation fails, return errors
        return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def delete_task(request, task_id):
    try:
        task = get_object_or_404(Task, task_id=task_id)
        task.delete()
        return Response({"success": True, "message": "Task deleted successfully!"}, status=status.HTTP_200_OK)
    except Task.DoesNotExist:
        return Response({"success": False, "error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def edit_task(request, task_id):
    # Get the task object
    task = get_object_or_404(Task, task_id=task_id)

    # Create a serializer instance with the existing task data
    serializer = TaskSerializer(task, data=request.data, partial=True)  # partial=True allows partial updates

    if serializer.is_valid():
        # Save the updated task
        serializer.save()
        return Response({"success": True, "message": "Task updated successfully!"}, status=status.HTTP_200_OK)
    else:
        return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def show_my_tasks(request):
    # Get the manager's ID from the request body (assuming the manager's ID is passed in the request)
    user_id = request.data.get('user_id')  # Get the user_id from the POST request body

    if not user_id:
        return Response({"success": False, "error": "user_id is required"}, status=400)

    try:
        # Fetch the manager object based on the provided user_id
        manager = Manager.objects.get(manager_id=user_id)
    except Manager.DoesNotExist:
        return Response({"success": False, "error": "Manager not found"}, status=404)

    # Get tasks where this manager is assigned
    tasks = Task.objects.filter(manager=manager)

    # Serialize the tasks
    serializer = TaskSerializer(tasks, many=True)

    return Response({"success": True, "tasks": serializer.data}, status=200)


@api_view(['POST'])
def create_role(request):
    # Check if role_id and role_name are present in the POST request body
    prole_id = request.data.get('role_id')
    prole_name = request.data.get('role_name')

    if not prole_id or not prole_name:
        return Response({"success": False, "error": "role_id and role_name are required"}, status=status.HTTP_400_BAD_REQUEST)

    # Create and save the new Role object
    role = Role(role_id=prole_id, role_name=prole_name)
    role.save()

    return Response({"success": True, "message": "Role created successfully!"}, status=status.HTTP_201_CREATED)

# Delete Role API View
@api_view(['GET'])
def delete_role(request, id):
    try:
        role = get_object_or_404(Role, id=id)
        role.delete()
        return Response({"success": True, "message": "Role deleted successfully!"}, status=status.HTTP_200_OK)
    except Role.DoesNotExist:
        return Response({"success": False, "error": "Role not found"}, status=status.HTTP_404_NOT_FOUND)

# Edit Role API View
@api_view(['POST'])
def edit_role(request, id):
    try:
        role = get_object_or_404(Role, id=id)
        role.role_id = request.data.get('role_id', role.role_id)  # Use provided role_id or keep existing
        role.role_name = request.data.get('role_name', role.role_name)  # Use provided role_name or keep existing
        
        role.save()
        return Response({"success": True, "message": "Role updated successfully!"}, status=status.HTTP_200_OK)
    except Role.DoesNotExist:
        return Response({"success": False, "error": "Role not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def create_team(request):
    try:
        # Extract the data from the JSON request body
        team_name = request.data['team_name']
        project_name = request.data['project']
        team_task = request.data['team_task']
        manager_name = request.data['manager']
        team_leader_name = request.data['team_leader']
        members = request.data['members']
        team_id = request.data['team_id']

        # Fetch the related project, manager, and team leader
        project = get_object_or_404(Project, name=project_name)
        manager = get_object_or_404(Manager, manager_name=manager_name)
        team_leader = get_object_or_404(Employee, employee_name=team_leader_name)

        # Create the team
        team = Team(
            team_name=team_name, 
            project=project, 
            team_task=team_task,  
            manager=manager, 
            team_leader=team_leader,
            team_id=team_id
        )
        team.save()

        # Add members to the team
        for member_name in members:
            member = get_object_or_404(Employee, employee_name=member_name)
            team.members.add(member)
        
        team.save()

        # Return a success response
        return Response({"success": True, "message": "Team created successfully!"}, status=status.HTTP_201_CREATED)
    
    except KeyError as e:
        return Response({"success": False, "error": f"Missing required field: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"success": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def delete_team(request, team_id):
    try:
        # Fetch the team by ID or return 404 if not found
        team = get_object_or_404(Team, team_id=team_id)
        
        # Delete the team
        team.delete()

        # Return a success response
        return Response({"success": True, "message": "Team deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)
    
    except Exception as e:
        return Response({"success": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def edit_team(request, team_id):
    try:
        # Get the team object or return 404 if it doesn't exist
        team = get_object_or_404(Team, team_id=team_id)

        # Extract the updated data from the request body
        team_name = request.data['team_name']
        project_name = request.data['project']
        team_task = request.data['team_task']
        manager_name = request.data['manager']
        team_leader_name = request.data['team_leader']
        members = request.data['members']
        team_id = request.data['team_id']

        # Fetch related objects based on new values
        project = get_object_or_404(Project, name=project_name)
        manager = get_object_or_404(Manager, manager_name=manager_name)
        team_leader = get_object_or_404(Employee, employee_name=team_leader_name)

        # Update team details
        team.team_name = team_name
        team.project = project
        team.team_task = team_task
        team.manager = manager
        team.team_leader = team_leader
        team.team_id = team_id
        team.save()

        # Clear existing members and add updated ones
        team.members.clear()
        for member_name in members:
            member = get_object_or_404(Employee, employee_name=member_name)
            team.members.add(member)

        # Return success response
        return Response({"success": True, "message": "Team updated successfully!"}, status=status.HTTP_200_OK)

    except KeyError as e:
        return Response({"success": False, "error": f"Missing required field: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"success": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def view_my_teams(request):
    try:
        # Retrieve the manager's username from the session
        manager_username = request.session.get('user')

        if not manager_username:
            return Response({"success": False, "message": "Manager not found in session."}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the manager object based on their username
        manager = Manager.objects.get(username=manager_username)

        # Get all teams managed by this manager
        teams = Team.objects.filter(manager=manager)

        # Serialize the teams (you can create a serializer if needed or return a simple list)
        team_data = [{"team_id": team.team_id, "team_name": team.team_name, "project_name": team.project.name, "manager": team.manager.username} for team in teams]

        # Return the team data as JSON
        return Response({"success": True, "teams": team_data}, status=status.HTTP_200_OK)

    except Manager.DoesNotExist:
        return Response({"success": False, "message": "Manager not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"success": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def assign_task_to_team_member(request, user):
    try:
        # Extract data from the request
        member = request.data.get('member')
        task_name = request.data.get('task_name')
        task_description = request.data.get('task_description')
        deadline = request.data.get('deadline')
        emptask_id = request.data.get('task_id')

        if not member or not task_name or not task_description or not deadline or not emptask_id:
            return Response({"success": False, "message": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new task
        emp_task = employee_task(
            task_name=task_name,
            task_description=task_description,
            assigned_to=member,
            deadline=deadline,
            emptask_id=emptask_id,
        )
        emp_task.save()

        return Response({"success": True, "message": "Task assigned to team member successfully!"}, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({"success": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def show_employee_tasks(request, user):
    if request.method == 'POST' and request.content_type == 'application/json':
        data = request.data
        task_id = data.get('task_id')
        new_status = data.get('status')

        try:
            task = employee_task.objects.get(id=task_id)
            task.emp_taskstatus = new_status
            task.save()
            return Response({'success': True}, status=status.HTTP_200_OK)
        except employee_task.DoesNotExist:
            return Response({'success': False, 'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
    
    elif request.method == 'GET':
        # Fetch tasks by their status for the employee
        not_started_projects = employee_task.objects.filter(emp_taskstatus='not started', assigned_to=user)
        in_progress_projects = employee_task.objects.filter(emp_taskstatus='in progress', assigned_to=user)
        in_review_projects = employee_task.objects.filter(emp_taskstatus='in review', assigned_to=user)
        completed_projects = employee_task.objects.filter(emp_taskstatus='completed', assigned_to=user)

        # Structure the response
        context = {
            'not_started_projects': not_started_projects,
            'in_progress_projects': in_progress_projects,
            'in_review_projects': in_review_projects,
            'completed_projects': completed_projects,
        }

        return Response(context, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def show_assigned_manager_task(request):
    if request.method == 'POST' and request.content_type == 'application/json':
        data = request.data
        ptask_id = data.get('task_id')
        new_status = data.get('status')

        try:
            task = Task.objects.get(id=ptask_id)
            task.status = new_status
            task.save()
            return Response({'success': True}, status=status.HTTP_200_OK)
        except Task.DoesNotExist:
            return Response({'success': False, 'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'GET':
        # Fetch tasks by their status for the manager
        not_started_projects = Task.objects.filter(status='not started')
        in_progress_projects = Task.objects.filter(status='in progress')
        in_review_projects = Task.objects.filter(status='in review')
        completed_projects = Task.objects.filter(status='completed')

        # Structure the response
        context = {
            'not_started_projects': not_started_projects,
            'in_progress_projects': in_progress_projects,
            'in_review_projects': in_review_projects,
            'completed_projects': completed_projects,
        }

        return Response(context, status=status.HTTP_200_OK)




@api_view(['GET'])
def view_my_emptask(request):
    # Assume the employee's user_id is stored in the session
    user_id = request.session.get('user_id')

    try:
        # Retrieve the employee object based on user_id
        employee = Employee.objects.get(employee_id=user_id)

        # Get all the tasks assigned to the employee
        emptasks = employee_task.objects.filter(assigned_to=employee)

        # Prepare the response data
        task_data = [
            {
                'task_id': task.id,
                'task_name': task.task_name,
                'task_description': task.task_description,
                'deadline': task.deadline,
                'status': task.emp_taskstatus
            }
            for task in emptasks
        ]
        
        return Response({'tasks': task_data}, status=status.HTTP_200_OK)
    
    except Employee.DoesNotExist:
        return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def delete_emptask(request, task_name):
    try:
        # Fetch the task based on task_name
        task = employee_task.objects.get(task_name=task_name)
        task.delete()
        return Response({'message': 'Task deleted successfully!'}, status=status.HTTP_200_OK)
    
    except employee_task.DoesNotExist:
        return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def project_manager_dashboard(request, user):
    try:
        # Fetch the manager based on the username
        manager = Manager.objects.get(username=user)
        
        # Fetch the projects associated with the manager
        projects = Project.objects.filter(project_manager=manager)
        
        # Prepare project data to send in the response
        project_data = []
        for project in projects:
            project_data.append({
                'project_id': project.project_id,
                'project_name': project.project_name,
                'project_description': project.project_description,
                # Add other relevant project fields here
            })
        
        # Send response with manager and project details
        return Response({
            'manager': {
                'manager_id': manager.manager_id,
                'manager_name': manager.manager_name,
                # Include other manager fields as necessary
            },
            'projects': project_data,
        }, status=status.HTTP_200_OK)
    
    except Manager.DoesNotExist:
        return Response({'error': 'Manager not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def update_managerproject_status(request, project_id):
    try:
        # Fetch the project using the provided project_id
        project = Project.objects.get(project_id=project_id)
        
        # Get the new status from the request body (JSON)
        new_status = request.data.get('project_status')

        # Update the project status
        project.project_status = new_status

        # If the status is "completed", mark the project as completed
        if new_status == 'completed':
            project.completion_date = timezone.now()  # Save current date as completion date

            # If the project is completed late, request a reason for the delay
            if project.is_late():  # Check if the project was completed after the deadline
                project.completion_reason = request.data.get('completion_reason', '')

        elif new_status == 'overdue':
            project.completion_reason = request.data.get('completion_reason', '')

        project.save()  # Save the updated project status

        # Return a success response with the updated project status
        return Response({'message': 'Project status updated successfully!'}, status=status.HTTP_200_OK)
    
    except Project.DoesNotExist:
        return Response({'error': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)



def project_detail(request, project_id):
    # Get the project by id or return a 404 if not found
    project = get_object_or_404(Project, project_id=project_id)

    # Pass the project to the template for display
    return render(request, 'authentication/project_detail.html', {'project': project})



@api_view(['POST'])
def kanban_dashboard(request):
    # Fetch projects categorized by their status
    not_started_projects = Project.objects.filter(project_status='not_started')
    in_progress_projects = Project.objects.filter(project_status='in_progress')
    completed_projects = Project.objects.filter(project_status='completed')

    # Prepare the data to be returned in the response
    projects_data = {
        'not_started_projects': [project.name for project in not_started_projects],
        'in_progress_projects': [project.name for project in in_progress_projects],
        'completed_projects': [project.name for project in completed_projects],
    }

    return Response(projects_data)



@api_view(['POST'])
def update_project_status(request):
    project_id = request.data.get('project_id')
    new_status = request.data.get('new_status')

    try:
        # Retrieve the project by its ID
        project = Project.objects.get(id=project_id)
        project.project_status = new_status
        project.save()

        return Response({'success': True}, status=status.HTTP_200_OK)
    except Project.DoesNotExist:
        return Response({'success': False, 'message': 'Project not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def get_projects(request):
    # Get all projects with selected fields
    projects = Project.objects.all().values('project_id', 'name', 'start_date', 'deadline', 'project_status')
    project_list = list(projects)  # Convert QuerySet to list
    
    return Response(project_list)  # Return the list of projects as a JSON response


@api_view(['POST'])
def get_project_data(request):
    # Fetch all projects
    projects = Project.objects.all()
    
    # Prepare the project data as a list of dictionaries
    project_data = [
        {
            'id': project.project_id,
            'name': project.name,
            'start_date': project.start_date.strftime('%Y-%m-%d'),
            'deadline': project.deadline.strftime('%Y-%m-%d'),
            'status': project.project_status
        }
        for project in projects
    ]
    
    return Response(project_data)  # Return the project data as a JSON response



@api_view(['POST'])
def upload_document(request, task_id):
    # Ensure that file is in the request
    if 'document' not in request.FILES:
        return Response({'error': 'No document provided'}, status=status.HTTP_400_BAD_REQUEST)

    # Get the task associated with the given task_id
    task = get_object_or_404(Task, task_id=task_id)

    # Extract the uploaded document
    document = request.FILES['document']

    # Create the TaskDocument object and save it
    TaskDocument.objects.create(
        task=task,
        uploaded_by=task.manager.username,  # Assuming 'manager' is a related field
        document=document
    )

    # Return a success response
    return Response({'message': 'Document uploaded successfully'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def upload_document_emp(request, id):
    # Ensure that the document is provided in the request
    if 'document' not in request.FILES:
        return Response({'error': 'No document provided'}, status=status.HTTP_400_BAD_REQUEST)

    # Get the employee_task associated with the given task id
    task = get_object_or_404(employee_task, id=id)

    # Extract the uploaded document
    document = request.FILES['document']
    uploaded_by = task.assigned_to  # Assuming 'assigned_to' is an Employee object

    # Create a TaskEmpDocument object and save it
    TaskEmpDocument.objects.create(
        employee_task=task,
        uploaded_by=uploaded_by,
        document=document
    )

    # Return a success response
    return Response({'message': 'Document uploaded successfully'}, status=status.HTTP_201_CREATED)



@api_view(['POST'])
def admin_view_documents(request):
    # Fetch documents from the database
    documents = TaskDocument.objects.all()
    empdocuments = TaskEmpDocument.objects.all()

    # Prepare the documents data
    documents_data = [
        {
            'id': doc.id,
            'task_id': doc.task.task_id,
            'uploaded_by': doc.uploaded_by,
            'document': doc.document.url  # Assuming the document is stored as a file URL
        } for doc in documents
    ]
    
    empdocuments_data = [
        {
            'id': emp_doc.id,
            'employee_task_id': emp_doc.employee_task.id,
            'uploaded_by': emp_doc.uploaded_by,
            'document': emp_doc.document.url
        } for emp_doc in empdocuments
    ]

    return Response({'documents': documents_data, 'empdocuments': empdocuments_data}, status=status.HTTP_200_OK)

@api_view(['POST'])
def employee_performance_view(request, username):
    try:
        performance_percentage = employee_task.calculate_employee_performance(username)
        return Response({'username': username, 'performance_percentage': performance_percentage}, status=status.HTTP_200_OK)
    except employee_task.DoesNotExist:
        return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def manager_performance_view(request, username):
    try:
        performance_percentage = Task.calculate_manager_performance(username)
        return Response({'username': username, 'performance_percentage': performance_percentage}, status=status.HTTP_200_OK)
    except Task.DoesNotExist:
        return Response({'error': 'Manager not found'}, status=status.HTTP_404_NOT_FOUND)



@api_view(['POST'])
def create_training_program(request):
    if request.method == 'POST':
        # Use the serializer to validate and save the data
        serializer = TrainingProgramSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Training program created successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def enroll_participant(request):
    if request.method == 'POST':
        # Use the serializer to validate and save the data
        serializer = ParticipationSerializer(data=request.data)
        
        if serializer.is_valid():
            # Save the participation instance
            training_participation = serializer.save()

            # Send email notification
            recipient_email = None
            recipient_name = None

            if training_participation.manager:
                recipient_email = training_participation.manager.email
                recipient_name = training_participation.manager.username
            elif training_participation.employee:
                recipient_email = training_participation.employee.email
                recipient_name = training_participation.employee.username

            if recipient_email:
                send_mail(
                    'Training Enrollment Success',
                    f'Dear {recipient_name}, you have been successfully enrolled in {training_participation.program}.',
                    settings.EMAIL_HOST_USER,
                    [recipient_email],
                    fail_silently=False,
                )

            return Response({'message': 'Participant successfully enrolled and notified.'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



# List all training programs
@api_view(['GET'])
def list_training_programs(request):
    programs = TrainingProgram.objects.all()
    serializer = TrainingProgramSerializer(programs, many=True)
    return Response(serializer.data)

# View progress of participants
@api_view(['GET'])
def view_training_progress(request):
    participations = TrainingParticipation.objects.all()
    serializer = TrainingParticipationSerializer(participations, many=True)
    return Response(serializer.data)



# Update view for TrainingProgram
@api_view(['POST'])
def update_program(request, program_id):
    program = get_object_or_404(TrainingProgram, program_id=program_id)
    serializer = TrainingProgramSerializer(program, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Delete view for TrainingProgram
@api_view(['POST'])
def delete_program(request, program_id):
    program = get_object_or_404(TrainingProgram, program_id=program_id)
    program.delete()
    return Response({'message': 'Program deleted successfully!'}, status=status.HTTP_200_OK)



# Update view for TrainingProgress
@api_view(['POST'])
def update_progress(request, program_name):
    progress = get_object_or_404(TrainingParticipation, program__name=program_name)
    serializer = TrainingParticipationSerializer(progress, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Delete view for TrainingProgress
@api_view(['POST'])
def delete_progress(request, program_name):
    progress = get_object_or_404(TrainingParticipation, program__name=program_name)
    progress.delete()
    return Response({'message': 'Progress deleted successfully!'}, status=status.HTTP_200_OK)



@api_view(['POST'])
def upload_certificate(request):
    serializer = CertificationSerializer(data=request.data)
    if serializer.is_valid():
        certification = serializer.save()
        certification.send_certificate_email()  # Custom method for sending the email
        return Response({'message': 'Certificate uploaded and email sent successfully!'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def employee_dashboard_certificates(request):
    employee = request.data.get('employee_username')  # Retrieve the employee username from the request body
    if not employee:
        return Response({'error': 'Employee username is required.'}, status=status.HTTP_400_BAD_REQUEST)

    certificates = Certification.objects.filter(participation_employee_username=employee)
    serializer = CertificationSerializer(certificates, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def manager_dashboard_certificates(request):
    manager = request.data.get('manager_username')  # Retrieve the manager username from the request body
    if not manager:
        return Response({'error': 'Manager username is required.'}, status=status.HTTP_400_BAD_REQUEST)

    certificates = Certification.objects.filter(participation_manager_username=manager)
    serializer = CertificationSerializer(certificates, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['POST'])
def enroll_training_manager(request):
    training_programs = TrainingProgram.objects.filter(for_managers=True)
    data = [{'id': program.program_id, 'name': program.name} for program in training_programs]
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def enroll_training_employee(request):
    training_programs = TrainingProgram.objects.filter(for_employees=True)
    data = [{'id': program.program_id, 'name': program.name} for program in training_programs]
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def enroll_manager(request):
    program_id = request.data.get('program_id')
    manager_username = request.data.get('manager_username')

    if not program_id or not manager_username:
        return Response({'error': 'Program ID and Manager username are required.'}, status=status.HTTP_400_BAD_REQUEST)

    program = TrainingProgram.objects.filter(program_id=program_id).first()
    manager = Manager.objects.filter(username=manager_username).first()

    if not program or not manager:
        return Response({'error': 'Invalid program or manager.'}, status=status.HTTP_404_NOT_FOUND)

    if TrainingParticipation.objects.filter(program=program, manager=manager).exists():
        return Response({'message': f'You have already been enrolled in {program.name} by admin.'}, status=status.HTTP_400_BAD_REQUEST)

    TrainingParticipation.objects.create(program=program, manager=manager, completion_status='not_started')

    send_mail(
        'Training Enrollment Success',
        f'You have been successfully enrolled in {program.name}.',
        settings.EMAIL_HOST_USER,
        [manager.email],
        fail_silently=False,
    )
    return Response({'message': f'Successfully enrolled in {program.name}.'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def enroll_employee(request):
    program_id = request.data.get('program_id')
    employee_username = request.data.get('employee_username')

    if not program_id or not employee_username:
        return Response({'error': 'Program ID and Employee username are required.'}, status=status.HTTP_400_BAD_REQUEST)

    program = TrainingProgram.objects.filter(program_id=program_id).first()
    employee = Employee.objects.filter(username=employee_username).first()

    if not program or not employee:
        return Response({'error': 'Invalid program or employee.'}, status=status.HTTP_404_NOT_FOUND)

    if TrainingParticipation.objects.filter(program=program, employee=employee).exists():
        return Response({'message': f'You have already been enrolled in {program.name} by admin.'}, status=status.HTTP_400_BAD_REQUEST)

    TrainingParticipation.objects.create(program=program, employee=employee, completion_status='not_started')

    send_mail(
        'Training Enrollment Success',
        f'You have been successfully enrolled in {program.name}.',
        settings.EMAIL_HOST_USER,
        [employee.email],
        fail_silently=False,
    )
    return Response({'message': f'Successfully enrolled in {program.name}.'}, status=status.HTTP_201_CREATED)



@api_view(['POST'])
def performance_chart_view(request):
    user_id = request.data.get('user_id')
    user_type = request.data.get('user_type')

    if not user_id or not user_type:
        return Response({'error': 'User ID and User Type are required.'}, status=status.HTTP_400_BAD_REQUEST)

    performance_data = get_performance_data(user_id, user_type)
    return Response({'performance': performance_data}, status=status.HTTP_200_OK)


def get_performance_data(user_id, user_type):
    if user_type == 'employee':
        logs = TaskLog.objects.filter(employee__employee_id=user_id)
    elif user_type == 'manager':
        logs = TaskLog.objects.filter(manager__manager_id=user_id)
    else:
        return {'error': 'Invalid user type.'}

    # Daily Performance
    today = now().date()
    daily_data = logs.filter(check_out_time__date=today).aggregate(
        total_hours=Sum('hours_worked'),
        task_count=Count('id')
    )

    # Weekly Performance
    start_of_week = today - timedelta(days=today.weekday())  # Monday of this week
    weekly_data = logs.filter(check_out_time__date__gte=start_of_week).aggregate(
        total_hours=Sum('hours_worked'),
        task_count=Count('id')
    )

    # Monthly Performance
    start_of_month = today.replace(day=1)  # First day of the current month
    monthly_data = logs.filter(check_out_time__date__gte=start_of_month).aggregate(
        total_hours=Sum('hours_worked'),
        task_count=Count('id')
    )

    # Annual Performance
    start_of_year = today.replace(month=1, day=1)  # First day of the current year
    annual_data = logs.filter(check_out_time__date__gte=start_of_year).aggregate(
        total_hours=Sum('hours_worked'),
        task_count=Count('id')
    )

    return {
        'daily': daily_data,
        'weekly': weekly_data,
        'monthly': monthly_data,
        'annual': annual_data
    }



@api_view(['POST'])
def task_check_in(request):
    task_id = request.data.get('task_id')
    user_type = request.data.get('user_type')
    user_id = request.data.get('user_id')

    if not task_id or not user_type or not user_id:
        return Response({'error': 'Task ID, User Type, and User ID are required.'}, status=status.HTTP_400_BAD_REQUEST)

    if user_type == 'employee':
        employee = get_object_or_404(Employee, employee_id=user_id)
        emptask = get_object_or_404(employee_task, emptask_id=task_id)

        # Check if the employee already has any active task logs (not checked out)
        if TaskLog.objects.filter(employee=employee, check_out_time__isnull=True).exists():
            return Response({'error': "You have already checked in to a task. Please check out before starting a new task."}, status=status.HTTP_400_BAD_REQUEST)

        TaskLog.objects.create(employeetask=emptask, employee=employee, check_in_time=now())
        return Response({'success': 'Checked in successfully!'}, status=status.HTTP_200_OK)

    elif user_type == 'manager':
        manager = get_object_or_404(Manager, manager_id=user_id)
        task = get_object_or_404(Task, task_id=task_id)

        # Check if the manager already has any active task logs (not checked out)
        if TaskLog.objects.filter(manager=manager, check_out_time__isnull=True).exists():
            return Response({'error': "You have already checked in to a task. Please check out before starting a new task."}, status=status.HTTP_400_BAD_REQUEST)

        TaskLog.objects.create(task=task, manager=manager, check_in_time=now())
        return Response({'success': 'Checked in successfully!'}, status=status.HTTP_200_OK)

    return Response({'error': 'Invalid user type.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def task_check_out(request):
    task_id = request.data.get('task_id')
    user_type = request.data.get('user_type')

    if not task_id or not user_type:
        return Response({'error': 'Task ID and User Type are required.'}, status=status.HTTP_400_BAD_REQUEST)

    if user_type == 'employee':
        emptask = get_object_or_404(employee_task, emptask_id=task_id)

        try:
            log = TaskLog.objects.get(employeetask=emptask, check_out_time__isnull=True)
        except TaskLog.DoesNotExist:
            return Response({'error': "This task has already been checked out or was never checked in."}, status=status.HTTP_400_BAD_REQUEST)

        log.check_out_time = now()
        log.calculate_hours_worked()
        log.save()
        return Response({'success': 'Checked out successfully!'}, status=status.HTTP_200_OK)

    elif user_type == 'manager':
        task = get_object_or_404(Task, task_id=task_id)

        try:
            log = TaskLog.objects.get(task=task, check_out_time__isnull=True)
        except TaskLog.DoesNotExist:
            return Response({'error': "This task has already been checked out or was never checked in."}, status=status.HTTP_400_BAD_REQUEST)

        log.check_out_time = now()
        log.calculate_hours_worked()
        log.save()
        return Response({'success': 'Checked out successfully!'}, status=status.HTTP_200_OK)

    return Response({'error': 'Invalid user type.'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def md_create_project(request):
    required_fields = ['project_id', 'project_name', 'project_description', 'project_startdate', 'project_deadline', 'project_manager']
    for field in required_fields:
        if field not in request.data:
            return Response({'error': f'Missing field: {field}'}, status=status.HTTP_400_BAD_REQUEST)

    project = Project(
        project_id=request.data['project_id'],
        name=request.data['project_name'],
        description=request.data['project_description'],
        start_date=request.data['project_startdate'],
        deadline=request.data['project_deadline'],
        project_manager=request.data['project_manager']
    )
    project.save()
    return Response({'success': 'Project created successfully!'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def md_edit_project(request, project_id):
    project = get_object_or_404(Project, project_id=project_id)

    required_fields = ['project_id', 'project_name', 'project_description', 'project_start_date', 'project_deadline', 'project_manager']
    for field in required_fields:
        if field not in request.data:
            return Response({'error': f'Missing field: {field}'}, status=status.HTTP_400_BAD_REQUEST)

    project.project_id = request.data['project_id']
    project.name = request.data['project_name']
    project.description = request.data['project_description']
    project.start_date = request.data['project_start_date']
    project.deadline = request.data['project_deadline']
    project.project_manager = request.data['project_manager']
    project.save()

    return Response({'success': 'Project updated successfully!'}, status=status.HTTP_200_OK)


@api_view(['GET'])
def md_show_project_status(request, project_id):
    project = get_object_or_404(Project, project_id=project_id)
    tasks = Task.objects.filter(project_name=project.name)
    emptasks = employee_task.objects.filter(team_project_name=project.name)

    context = {
        'project': {
            'project_id': project.project_id,
            'name': project.name,
            'description': project.description,
            'start_date': project.start_date,
            'deadline': project.deadline,
            'manager': project.project_manager,
        },
        'tasks': list(tasks.values()),
        'emptasks': list(emptasks.values())
    }
    return Response(context, status=status.HTTP_200_OK)


@api_view(['POST'])
def md_delete_project(request, project_id):
    project = get_object_or_404(Project, project_id=project_id)
    project.delete()
    return Response({'success': 'Project deleted successfully!'}, status=status.HTTP_200_OK)



@api_view(['POST'])
def md_create_task(request):
    required_fields = ['task_id', 'project_manager', 'project_name', 'task_name', 'task_description', 'priority', 'task_startdate', 'task_deadline']
    for field in required_fields:
        if field not in request.data:
            return Response({'error': f'Missing field: {field}'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        manager = Manager.objects.get(manager_name=request.data['project_manager'])
    except Manager.DoesNotExist:
        return Response({'error': 'Manager not found'}, status=status.HTTP_404_NOT_FOUND)
    
    task = Task(
        task_id=request.data['task_id'],
        project_manager=manager.manager_name,
        project_name=request.data['project_name'],
        task_name=request.data['task_name'],
        description=request.data['task_description'],
        priority=request.data['priority'],
        start_date=request.data['task_startdate'],
        deadline=request.data['task_deadline'],
        manager=manager
    )
    task.save()
    return Response({'success': 'Task created successfully!'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def md_edit_task(request, task_id):
    task = get_object_or_404(Task, task_id=task_id)

    required_fields = ['task_id', 'project_manager', 'project_name', 'task_name', 'task_description', 'priority', 'task_startdate', 'task_deadline']
    for field in required_fields:
        if field not in request.data:
            return Response({'error': f'Missing field: {field}'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        manager = Manager.objects.get(manager_name=request.data['project_manager'])
    except Manager.DoesNotExist:
        return Response({'error': 'Manager not found'}, status=status.HTTP_404_NOT_FOUND)

    task.task_id = request.data['task_id']
    task.project_name = request.data['project_name']
    task.task_name = request.data['task_name']
    task.description = request.data['task_description']
    task.priority = request.data['priority']
    task.start_date = request.data['task_startdate']
    task.deadline = request.data['task_deadline']
    task.manager = manager
    task.save()

    return Response({'success': 'Task updated successfully!'}, status=status.HTTP_200_OK)


@api_view(['DELETE'])
def md_delete_task(request, task_id):
    task = get_object_or_404(Task, task_id=task_id)
    task.delete()
    return Response({'success': 'Task deleted successfully!'}, status=status.HTTP_200_OK)



@api_view(['POST'])
def md_create_role(request):
    # Validate required fields
    required_fields = ['role_id', 'role_name']
    for field in required_fields:
        if field not in request.data:
            return Response({'error': f'Missing field: {field}'}, status=status.HTTP_400_BAD_REQUEST)

    # Create the role
    role = Role(
        role_id=request.data['role_id'],
        role_name=request.data['role_name']
    )
    role.save()
    return Response({'success': 'Role created successfully!'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def md_edit_role(request, id):
    role = get_object_or_404(Role, id=id)

    # Validate required fields
    required_fields = ['role_id', 'role_name']
    for field in required_fields:
        if field not in request.data:
            return Response({'error': f'Missing field: {field}'}, status=status.HTTP_400_BAD_REQUEST)

    # Update the role
    role.role_id = request.data['role_id']
    role.role_name = request.data['role_name']
    role.save()

    return Response({'success': 'Role updated successfully!'}, status=status.HTTP_200_OK)


@api_view(['DELETE'])
def md_delete_role(request, id):
    role = get_object_or_404(Role, id=id)
    role.delete()
    return Response({'success': 'Role deleted successfully!'}, status=status.HTTP_200_OK)


# Create Team
@api_view(['POST'])
def md_create_team(request):
    # Validate required fields
    required_fields = ['team_id', 'team_name', 'project', 'team_task', 'manager', 'team_leader', 'members']
    for field in required_fields:
        if field not in request.data:
            return Response({'error': f'Missing field: {field}'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Extract data from request
    team_name = request.data['team_name']
    project_name = request.data['project']
    team_task = request.data['team_task']
    manager_name = request.data['manager']
    team_leader_name = request.data['team_leader']
    members = request.data['members']
    team_id = request.data['team_id']

    # Fetch related objects
    project = get_object_or_404(Project, name=project_name)
    manager = get_object_or_404(Manager, manager_name=manager_name)
    team_leader = get_object_or_404(Employee, employee_name=team_leader_name)

    # Create the team
    team = Team(team_name=team_name, project=project, team_task=team_task,  manager=manager, team_leader=team_leader, team_id=team_id)
    team.save()

    # Add members to the team
    for member_name in members:
        member = get_object_or_404(Employee, employee_name=member_name)
        team.members.add(member)
    
    team.save()

    return Response({'success': 'Team created successfully!'}, status=status.HTTP_201_CREATED)


# Edit Team
@api_view(['POST'])
def md_edit_team(request, team_id):
    team = get_object_or_404(Team, team_id=team_id)

    # Validate required fields
    required_fields = ['team_name', 'project', 'team_task', 'manager', 'team_leader', 'members']
    for field in required_fields:
        if field not in request.data:
            return Response({'error': f'Missing field: {field}'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Extract data from request
    team_name = request.data['team_name']
    project_name = request.data['project']
    team_task = request.data['team_task']
    manager_name = request.data['manager']
    team_leader_name = request.data['team_leader']
    members = request.data['members']
    team_id = request.data['team_id']

    # Fetch related objects
    project = get_object_or_404(Project, name=project_name)
    manager = get_object_or_404(Manager, manager_name=manager_name)
    team_leader = get_object_or_404(Employee, employee_name=team_leader_name)

    # Update team details
    team.team_name = team_name
    team.project = project
    team.team_task = team_task
    team.manager = manager
    team.team_leader = team_leader
    team.team_id = team_id
    team.save()

    # Clear existing members and add updated ones
    team.members.clear()
    for member_name in members:
        member = get_object_or_404(Employee, employee_name=member_name)
        team.members.add(member)

    return Response({'success': 'Team updated successfully!'}, status=status.HTTP_200_OK)


# Delete Team
@api_view(['DELETE'])
def md_delete_team(request, team_id):
    team = get_object_or_404(Team, team_id=team_id)
    team.delete()
    return Response({'success': 'Team deleted successfully!'}, status=status.HTTP_200_OK)


@api_view(['GET'])
def md_kanban_dashboard(request):
    # Fetch projects categorized by their status
    not_started_projects = Project.objects.filter(project_status='not_started')
    in_progress_projects = Project.objects.filter(project_status='in_progress')
    completed_projects = Project.objects.filter(project_status='completed')

    # Serialize project data to return as JSON
    not_started_projects_data = [{"project_id": project.project_id, "project_name": project.name, "status": project.project_status} for project in not_started_projects]
    in_progress_projects_data = [{"project_id": project.project_id, "project_name": project.name, "status": project.project_status} for project in in_progress_projects]
    completed_projects_data = [{"project_id": project.project_id, "project_name": project.name, "status": project.project_status} for project in completed_projects]

    # Return data as a JSON response
    return Response({
        'not_started_projects': not_started_projects_data,
        'in_progress_projects': in_progress_projects_data,
        'completed_projects': completed_projects_data
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
def md_get_projects(request):
    projects = Project.objects.all().values('project_id', 'name', 'start_date', 'deadline', 'project_status')
    project_list = list(projects)  # Convert QuerySet to list
    return Response(project_list, status=200)

@api_view(['GET'])
def md_get_project_data(request):
    projects = Project.objects.all()
    project_data = [
        {
            'id': project.project_id,
            'name': project.name,
            'start_date': project.start_date.strftime('%Y-%m-%d'),
            'deadline': project.deadline.strftime('%Y-%m-%d'),
            'status': project.project_status
        }
        for project in projects
    ]
    return Response(project_data, status=200)


@api_view(['GET'])
def md_admin_view_documents(request):
    documents = TaskDocument.objects.all().values('document_id', 'document_name', 'upload_date')
    empdocuments = TaskEmpDocument.objects.all().values('document_id', 'document_name', 'upload_date')
    
    response_data = {
        'documents': list(documents),
        'empdocuments': list(empdocuments)
    }
    
    return Response(response_data, status=200)


@api_view(['GET'])
def md_employee_performance_view(request, username):
    performance_percentage = employee_task.calculate_employee_performance(username)
    return Response({'performance': performance_percentage}, status=200)


@api_view(['GET'])
def md_manager_performance_view(request, username):
    performance_percentage = Task.calculate_manager_performance(username)
    return Response({'performance': performance_percentage}, status=200)


@api_view(['POST'])
def md_create_training_program(request):
    if request.method == 'POST':
        # Deserialize the incoming JSON data
        serializer = TrainingProgramSerializer(data=request.data)
        
        if serializer.is_valid():
            # Save the new training program if valid
            serializer.save()
            return Response({'message': 'Training program created successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def md_enroll_participant(request):
    if request.method == 'POST':
        # Deserialize incoming data
        serializer = TrainingParticipationSerializer(data=request.data)
        
        if serializer.is_valid():
            participation = serializer.save()

            # Send email notification
            if participation.manager:
                recipient_email = participation.manager.email
                recipient_name = participation.manager.username
            elif participation.employee:
                recipient_email = participation.employee.email
                recipient_name = participation.employee.username
            else:
                recipient_email = None
                recipient_name = None

            if recipient_email:
                send_mail(
                    'Training Enrollment Success',
                    f'Dear {recipient_name}, you have been successfully enrolled in {participation.program}.',
                    settings.EMAIL_HOST_USER,
                    [recipient_email],
                    fail_silently=False,
                )

            return Response({'message': 'Participant enrolled successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def md_list_training_programs(request):
    programs = TrainingProgram.objects.all()
    serializer = TrainingProgramSerializer(programs, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def md_view_training_progress(request):
    participations = TrainingParticipation.objects.all()
    serializer = TrainingParticipationSerializer(participations, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
def md_update_program(request, program_id):
    program = get_object_or_404(TrainingProgram, program_id=program_id)
    if request.method == 'PUT':
        serializer = TrainingProgramSerializer(program, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Training program updated successfully!'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def md_delete_program(request, program_id):
    program = get_object_or_404(TrainingProgram, program_id=program_id)
    program.delete()
    return Response({'message': 'Training program deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['PUT'])
def md_update_progress(request, program_name):
    progress = get_object_or_404(TrainingParticipation, program__name=program_name)
    if request.method == 'PUT':
        serializer = TrainingParticipationSerializer(progress, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Training progress updated successfully!'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def md_delete_progress(request, program_name):
    progress = get_object_or_404(TrainingParticipation, program__name=program_name)
    progress.delete()
    return Response({'message': 'Training progress deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def md_upload_certificate(request):
    if request.method == 'POST':
        # Use serializer to handle file and form data
        serializer = CertificationSerializer(data=request.data)
        
        if serializer.is_valid():
            certification = serializer.save()
            
            # Send the certificate email (you might need to adjust this part as per your email logic)
            certification.send_certificate_email()
            
            # Return a success response
            return Response({'message': 'Certificate uploaded and email sent successfully!'}, status=status.HTTP_201_CREATED)
        
        # Return errors if the serializer is invalid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['POST'])
def md_performance_chart(request, user_type, user_id):
    # Get the user type (manager or employee)
    if user_type == 'employee':
        user = get_object_or_404(Employee, employee_id=user_id)
        task_logs = TaskLog.objects.filter(employee=user)
    elif user_type == 'manager':
        user = get_object_or_404(Manager, manager_id=user_id)
        task_logs = TaskLog.objects.filter(manager=user)
    else:
        return Response({"error": "Invalid user type"}, status=status.HTTP_400_BAD_REQUEST)

    # Get current date
    today = now().date()
    
    # Calculate daily, weekly, monthly, and annual data
    daily_data = task_logs.filter(check_in_time__date=today).aggregate(
        hours_worked=Sum('hours_worked'),
        total_tasks=Count('task')
    )

    weekly_data = task_logs.filter(check_in_time__gte=today - timedelta(days=7)).aggregate(
        hours_worked=Sum('hours_worked'),
        total_tasks=Count('task')
    )

    monthly_data = task_logs.filter(check_in_time__gte=today - timedelta(days=30)).aggregate(
        hours_worked=Sum('hours_worked'),
        total_tasks=Count('task')
    )

    annual_data = task_logs.filter(check_in_time__year=today.year).aggregate(
        hours_worked=Sum('hours_worked'),
        total_tasks=Count('task')
    )

    # Prepare the response data
    performance_data = {
        'user_type': user_type,
        'user_id': user_id,
        'user_name': user.username,  # Assuming the user has a `username` field
        'daily_data': daily_data,
        'weekly_data': weekly_data,
        'monthly_data': monthly_data,
        'annual_data': annual_data,
    }
    
    return Response(performance_data, status=status.HTTP_200_OK)


@api_view(['POST'])
def md_create_performance_review(request):
    employee_name = request.data.get('employee_name')
    manager_username = request.data.get('manager_username')
    comments = request.data.get('comments')
    score = request.data.get('score')

    try:
        employee = Employee.objects.get(employee_name=employee_name)
        manager = Manager.objects.get(username=manager_username)
    except (Employee.DoesNotExist, Manager.DoesNotExist):
        return Response({"error": "Employee or Manager not found"}, status=status.HTTP_400_BAD_REQUEST)

    performance_review = PerformanceReview.objects.create(
        employee=employee,
        review_date=timezone.now(),
        manager=manager,
        comments=comments,
        score=score
    )
    return Response({"message": "Performance review created successfully"}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def md_performance_review_list(request):
    reviews = PerformanceReview.objects.all()
    review_data = [
        {
            'employee_name': review.employee.employee_name,
            'manager_name': review.manager.username,
            'review_date': review.review_date,
            'comments': review.comments,
            'score': review.score
        }
        for review in reviews
    ]
    return Response(review_data, status=status.HTTP_200_OK)

@api_view(['POST'])
def md_create_goal(request):
    employee_id = request.data.get('employee_id')
    goal_text = request.data.get('goal_text')
    start_date = request.data.get('start_date')
    end_date = request.data.get('end_date')

    try:
        employee = Employee.objects.get(employee_id=employee_id)
    except Employee.DoesNotExist:
        return Response({"error": "Employee not found"}, status=status.HTTP_400_BAD_REQUEST)

    Goal.objects.create(
        employee=employee,
        goal_text=goal_text,
        start_date=start_date,
        end_date=end_date
    )
    return Response({"message": "Goal created successfully"}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def md_goal_list(request):
    goals = Goal.objects.all()
    goal_data = [
        {
            'employee_name': goal.employee.employee_name,
            'goal_text': goal.goal_text,
            'start_date': goal.start_date,
            'end_date': goal.end_date
        }
        for goal in goals
    ]
    return Response(goal_data, status=status.HTTP_200_OK)

@api_view(['POST'])
def md_create_feedback(request):
    from_manager_id = request.data.get('from_manager_id')
    to_employee_id = request.data.get('to_employee_id')
    comments = request.data.get('comments')

    try:
        from_manager = Manager.objects.get(manager_id=from_manager_id)
        to_employee = Employee.objects.get(employee_id=to_employee_id)
    except (Manager.DoesNotExist, Employee.DoesNotExist):
        return Response({"error": "Manager or Employee not found"}, status=status.HTTP_400_BAD_REQUEST)

    Feedback.objects.create(
        from_manager=from_manager,
        to_employee=to_employee,
        feedback_date=timezone.now(),
        comments=comments
    )
    return Response({"message": "Feedback created successfully"}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def md_feedback_list(request):
    feedbacks = Feedback.objects.all()
    feedback_data = [
        {
            'from_manager': feedback.from_manager.username,
            'to_employee': feedback.to_employee.employee_name,
            'feedback_date': feedback.feedback_date,
            'comments': feedback.comments
        }
        for feedback in feedbacks
    ]
    return Response(feedback_data, status=status.HTTP_200_OK)








