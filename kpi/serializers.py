from rest_framework import serializers
from .models import PerformanceReview, Goal, Feedback, ManagerPerformanceReview, ManagerGoal, ManagerFeedback, OverallFeedback

class PerformanceReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerformanceReview
        fields = ['id', 'employee', 'review_date', 'manager', 'comments', 'score']

class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ['id', 'employee', 'goal_text', 'start_date', 'end_date', 'is_completed']

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['id', 'from_manager', 'to_employee', 'feedback_date', 'comments']

class ManagerPerformanceReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagerPerformanceReview
        fields = ['id', 'manager', 'review_date', 'comments', 'score']

class ManagerGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagerGoal
        fields = ['id', 'manager', 'goal_text', 'start_date', 'end_date', 'is_completed']

class ManagerFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagerFeedback
        fields = ['id', 'to_manager', 'feedback_date', 'comments']

class OverallFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = OverallFeedback
        fields = ['id', 'employee', 'manager', 'feedback_date', 'comments', 'is_reviewed']

from rest_framework import serializers
from .models import ManagerPerformanceReview

class ManagerPerformanceReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagerPerformanceReview
        fields = ['id', 'manager', 'review_date', 'comments', 'score']
        # Optionally, include related manager details
        depth = 1  # Uncomment this line to include nested manager details (optional)



# serializers.py


