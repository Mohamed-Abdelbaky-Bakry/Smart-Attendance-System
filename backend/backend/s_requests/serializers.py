from rest_framework import serializers
from users.serializers import StudentRetriveSerializer
from academics.serializers import SubjectRetrieveSerializer
from .models import Request
from academics.models import Subject


class RequestSerializer(serializers.ModelSerializer):
    student = serializers.HiddenField(default=serializers.CurrentUserDefault())
    subject = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.none(),
        required=False,
        allow_null=True
    )
    class Meta:
        model = Request
        fields = ['id', 'student', 'subject', 'request_type', 'description', 'status', 'created_at', 'instructor_comment', 'grade', 'replied_at']
        extra_kwargs = {'subject': {'required': True}}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and hasattr(request.user, 'student_profile'):
            student = request.user.student_profile
            enrolled = Subject.objects.filter(enrollment__student=student)
            self.fields['subject'].queryset = enrolled.distinct()

class RequestStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['status', 'instructor_comment']
        read_only_fields = ['student', 'subject', 'request_type', 'description', 'grade']
    

class RequestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['subject', 'request_type', 'description']
        read_only_fields = ['status']


class RequestRetrieveSerializer(serializers.ModelSerializer):
    student = StudentRetriveSerializer(read_only=True)
    subject = SubjectRetrieveSerializer(read_only=True)
    class Meta:
        model = Request
        fields = ['id', 'student', 'subject', 'request_type', 'description', 'status', 'created_at', 'instructor_comment', 'grade', 'replied_at']
        extra_kwargs = {'subject': {'required': True}}