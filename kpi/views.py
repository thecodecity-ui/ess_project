from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from authentication.models import Manager
from projectmanagement.models import Team
from .models import PerformanceReview, Employee
from .serializers import PerformanceReviewSerializer, ManagerPerformanceReviewSerializer
from django.utils import timezone
from .models import PerformanceReview
from .models import Goal, Employee
from .serializers import GoalSerializer
from .models import Goal
from .serializers import GoalSerializer
from django.utils import timezone
from .models import Feedback
from .serializers import FeedbackSerializer
from authentication.models import Manager, Employee
from .models import Feedback
from .serializers import FeedbackSerializer
from authentication.models import Employee
from projectmanagement.models import Task 
from projectmanagement.models import Task  # Assuming you have task-related data
from authentication.models import Manager 
from .models import PerformanceReview, Goal, Feedback
from .serializers import PerformanceReviewSerializer, GoalSerializer, FeedbackSerializer,ManagerPerformanceReviewSerializer
from .models import Manager, ManagerPerformanceReview
from .models import ManagerGoal
from .serializers import ManagerGoalSerializer,ManagerFeedbackSerializer
from authentication.models import Manager
from .models import ManagerPerformanceReview,ManagerFeedback
from .models import OverallFeedback
from .serializers import OverallFeedbackSerializer
from .models import Manager
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Manager, ManagerPerformanceReview
from .serializers import ManagerPerformanceReviewSerializer
from django.shortcuts import get_object_or_404

@api_view(['POST'])
def create_performance_review(request):
    try:
        employee_name = request.data.get('employee_name')
        manager_username = request.session.get('user')  # Assumes session-based authentication
        comments = request.data.get('comments')
        score = request.data.get('score')

        employee = Employee.objects.get(employee_name=employee_name)
        manager = Manager.objects.get(username=manager_username)

        performance_review = PerformanceReview.objects.create(
            employee=employee,
            review_date=timezone.now(),
            manager=manager,
            comments=comments,
            score=score,
        )

        serializer = PerformanceReviewSerializer(performance_review)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    except Employee.DoesNotExist:
        return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)
    except Manager.DoesNotExist:
        return Response({'error': 'Manager not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET'])
def performance_review_list(request):
    """
    Retrieve a list of all performance reviews.
    """
    reviews = PerformanceReview.objects.all()
    serializer = PerformanceReviewSerializer(reviews, many=True)
    return Response(serializer.data)




@api_view(['POST'])
def create_goal(request):
    """
    Create a new goal for an employee.
    """
    employee_id = request.data.get('employee_id')
    goal_text = request.data.get('goal_text')
    start_date = request.data.get('start_date')
    end_date = request.data.get('end_date')

    # Validate employee existence
    try:
        employee = Employee.objects.get(employee_id=employee_id)
    except Employee.DoesNotExist:
        return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)

    # Create the goal
    goal = Goal.objects.create(
        employee=employee,
        goal_text=goal_text,
        start_date=start_date,
        end_date=end_date
    )

    serializer = GoalSerializer(goal)
    return Response(serializer.data, status=status.HTTP_201_CREATED)




@api_view(['GET'])
def goal_list(request):
    """
    Retrieve a list of all goals.
    """
    goals = Goal.objects.all()
    serializer = GoalSerializer(goals, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)




@api_view(['POST'])
def create_feedback(request):
    """
    Create a new feedback entry.
    """
    from_manager_id = request.data.get('from_manager_id')
    to_employee_id = request.data.get('to_employee_id')
    comments = request.data.get('comments')

    try:
        from_manager = Manager.objects.get(manager_id=from_manager_id)
        to_employee = Employee.objects.get(employee_id=to_employee_id)

        feedback = Feedback.objects.create(
            from_manager=from_manager,
            to_employee=to_employee,
            feedback_date=timezone.now(),
            comments=comments
        )

        serializer = FeedbackSerializer(feedback)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Manager.DoesNotExist:
        return Response({"error": "Manager not found"}, status=status.HTTP_404_NOT_FOUND)
    except Employee.DoesNotExist:
        return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def feedback_list(request):
    """
    Retrieve the list of all feedbacks.
    """
    feedbacks = Feedback.objects.all()
    serializer = FeedbackSerializer(feedbacks, many=True)
    return Response(serializer.data)





@api_view(['GET'])
def kpi_dashboard(request):
    """
    Retrieve the KPI dashboard data.
    """
    # Example data that might be shown in the KPI dashboard
    kpi_data = {
        'total_tasks': 120,
        'completed_tasks': 85,
        'pending_tasks': 35,
        'employee_performance': [
            {'employee_id': 1, 'employee_name': 'John Doe', 'tasks_completed': 45},
            {'employee_id': 2, 'employee_name': 'Jane Smith', 'tasks_completed': 40},
            {'employee_id': 3, 'employee_name': 'Jim Beam', 'tasks_completed': 35}
        ],
        'average_score': 8.5
    }
    
    return Response(kpi_data)

 # Assuming you have task-related data

@api_view(['GET'])
def kpi_dashboard_employee(request, employee_id):
    """
    Retrieve the employee-specific KPI dashboard data.
    """
    try:
        employee = Employee.objects.get(id=employee_id)

        # Example employee KPI data (replace with actual logic as needed)
        tasks_completed = Task.objects.filter(employee=employee, status='Completed').count()
        tasks_in_progress = Task.objects.filter(employee=employee, status='In Progress').count()

        kpi_data = {
            'employee_name': employee.employee_name,
            'tasks_completed': tasks_completed,
            'tasks_in_progress': tasks_in_progress,
            'average_performance_score': 8.5  # Placeholder score
        }
        
        return Response(kpi_data)

    except Employee.DoesNotExist:
        return Response({'error': 'Employee not found'}, status=404)
    
 # Assuming you need manager data for the admin dashboard

@api_view(['POST'])
def kpi_dashboard_admin(request):
    """
    Retrieve the admin-specific KPI dashboard data.
    This can include aggregated data like task completion stats, active managers, etc.
    """
    try:
        # Example aggregated data (adjust logic based on actual requirements)
        total_tasks = Task.objects.count()
        total_completed_tasks = Task.objects.filter(status='Completed').count()
        total_active_managers = Manager.objects.filter(is_active=True).count()

        kpi_data = {
            'total_tasks': total_tasks,
            'total_completed_tasks': total_completed_tasks,
            'total_active_managers': total_active_managers,
            'average_task_completion_time': '2 days',  # Placeholder value
            'pending_tasks': total_tasks - total_completed_tasks
        }

        return Response(kpi_data)

    except Exception as e:
        return Response({'error': str(e)}, status=500)




@api_view(['GET'])
def performance_review_list_employee(request, employee_name):
    # Filter reviews for the employee
    reviews = PerformanceReview.objects.filter(employee__username=employee_name)
    
    # Serialize the data
    serializer = PerformanceReviewSerializer(reviews, many=True)
    
    # Return serialized data as a JSON response
    return Response(serializer.data)


@api_view(['GET'])
def view_goal_employee(request, employee_name):
    # Filter goals for the employee
    goals = Goal.objects.filter(employee__username=employee_name)
    
    # Serialize the data
    serializer = GoalSerializer(goals, many=True)
    
    # Return serialized data as a JSON response
    return Response(serializer.data)


@api_view(['GET'])
def view_feedback_employee(request, employee_name):
    # Filter feedbacks for the employee
    feedbacks = Feedback.objects.filter(to_employee__username=employee_name)
    
    # Serialize the data
    serializer = FeedbackSerializer(feedbacks, many=True)
    
    # Return serialized data as a JSON response
    return Response(serializer.data)




#admin




# Create performance review for a manager



@api_view(['POST'])
def create_performance_review_manager(request):
    if request.method == 'POST':
        manager_id = request.data.get('manager')
        review_date = request.data.get('review_date')
        comments = request.data.get('comments')
        score = request.data.get('score')

        # Check if all required fields are provided
        if not manager_id or not review_date or not comments or not score:
            return Response({'error': 'All fields are required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Get the manager object
            manager = Manager.objects.get(id=manager_id)
        except Manager.DoesNotExist:
            return Response({'error': 'Manager not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Create the performance review for the manager
        review = ManagerPerformanceReview(manager=manager, review_date=review_date, comments=comments, score=score)
        review.save()

        # Serialize the review data and return it as a response
        serializer = ManagerPerformanceReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



# Create goal setting for a manager
# views.py



@api_view(['POST'])
def create_goal_manager(request):
    if request.method == 'POST':
        serializer = ManagerGoalSerializer(data=request.data)
        if serializer.is_valid():
            # Check if the manager exists
            try:
                manager = Manager.objects.get(id=request.data['manager'])
            except Manager.DoesNotExist:
                return Response({"error": "Manager not found."}, status=status.HTTP_404_NOT_FOUND)

            # Save the goal
            serializer.save(manager=manager)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# views.py

@api_view(['POST'])
def create_feedback_manager(request):
    if request.method == 'POST':
        serializer = ManagerFeedbackSerializer(data=request.data)
        if serializer.is_valid():
            # Check if the manager exists
            try:
                to_manager = Manager.objects.get(id=request.data['to_manager'])
            except Manager.DoesNotExist:
                return Response({"error": "Manager not found."}, status=status.HTTP_404_NOT_FOUND)

            # Save the feedback
            serializer.save(to_manager=to_manager)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





# View for displaying Manager Performance Reviews
# views.py



@api_view(['GET'])
def view_manager_reviews(request):
    reviews = ManagerPerformanceReview.objects.all()
    if not reviews:
        return Response({"message": "No performance reviews found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = ManagerPerformanceReviewSerializer(reviews, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
# views.py

@api_view(['GET'])
def view_manager_goals(request):
    goals = ManagerGoal.objects.all()
    if not goals:
        return Response({"message": "No goals found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = ManagerGoalSerializer(goals, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
# views.py

@api_view(['GET'])
def view_manager_feedbacks(request):
    feedbacks = ManagerFeedback.objects.all()
    if not feedbacks:
        return Response({"message": "No feedback found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = ManagerFeedbackSerializer(feedbacks, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
# views.py

@api_view(['GET'])
def view_create_performance_review_manager(request, manager_name):
    reviews = ManagerPerformanceReview.objects.filter(manager__username=manager_name)
    if not reviews:
        return Response({"message": f"No performance reviews found for manager {manager_name}."}, status=status.HTTP_404_NOT_FOUND)

    serializer = ManagerPerformanceReviewSerializer(reviews, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
# views.py

@api_view(['GET'])
def view_create_goal_manager(request, manager_name):
    goals = ManagerGoal.objects.filter(manager__username=manager_name)
    if not goals:
        return Response({"message": f"No goals found for manager {manager_name}."}, status=status.HTTP_404_NOT_FOUND)

    serializer = ManagerGoalSerializer(goals, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
# views.py

@api_view(['GET'])
def view_create_feedback_manager(request, manager_name):
    feedbacks = ManagerFeedback.objects.filter(to_manager__username=manager_name)
    if not feedbacks:
        return Response({"message": f"No feedback found for manager {manager_name}."}, status=status.HTTP_404_NOT_FOUND)

    serializer = ManagerFeedbackSerializer(feedbacks, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



#feedback
# views.py


 # Assuming the `check_if_manager` function is placed in `utils.py`

@api_view(['GET'])
def feedback_form(request):
    # Check if the user is a manager or employee
    is_manager = check_if_manager(request.session.get('user'))  # You can replace with actual logic
    return Response({'is_manager': is_manager}, status=status.HTTP_200_OK)

@api_view(['POST'])
def submit_feedback(request):
    comments = request.data.get('comments')
    if not comments:
        return Response({'error': 'Please provide feedback before submitting!'}, status=status.HTTP_400_BAD_REQUEST)

    is_manager = check_if_manager(request.session.get('user'))  # Replace with actual logic
    if is_manager:
        manager = Manager.objects.get(username=request.session.get('user'))
        feedback = OverallFeedback(manager=manager, comments=comments)
    else:
        employee = Employee.objects.get(username=request.session.get('user'))
        feedback = OverallFeedback(employee=employee, comments=comments)

    feedback.save()
    return Response({'message': 'Feedback submitted successfully!'}, status=status.HTTP_201_CREATED)
@api_view(['GET'])
def admin_feedback_dashboard(request):
    feedbacks = OverallFeedback.objects.all()
    if not feedbacks:
        return Response({'message': 'No feedback found.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = OverallFeedbackSerializer(feedbacks, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
@api_view(['POST'])
def update_feedback_status(request, feedback_id):
    feedback = get_object_or_404(OverallFeedback, id=feedback_id)
    feedback.is_reviewed = True
    feedback.save()
    return Response({'message': 'Feedback status updated to reviewed.'}, status=status.HTTP_200_OK)
@api_view(['POST'])
def update_employee_goal(request, goal_id):
    goal = get_object_or_404(Goal, id=goal_id)
    goal.is_completed = True  # Mark goal as completed
    goal.save()
    return Response({'message': 'Goal marked as completed.'}, status=status.HTTP_200_OK)
@api_view(['POST'])
def update_manager_goal(request, goal_id):
    manager_goal = get_object_or_404(ManagerGoal, id=goal_id)
    manager_goal.is_completed = True  # Mark goal as completed
    manager_goal.save()
    return Response({'message': 'Manager goal marked as completed.'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def check_if_manager(request):
    """
    API endpoint to check if a user is a manager.
    """
    username = request.data.get('username')  # Extract username from POST data

    if not username:
        return Response({'error': 'Username is required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Check if the username exists in the Manager model
        Manager.objects.get(username=username)
        return Response({'is_manager': True}, status=status.HTTP_200_OK)
    except Manager.DoesNotExist:
        return Response({'is_manager': False}, status=status.HTTP_404_NOT_FOUND)
