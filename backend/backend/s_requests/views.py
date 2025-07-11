from rest_framework import viewsets
from .models import Request
from .serializers import RequestRetrieveSerializer, RequestSerializer, RequestStatusUpdateSerializer, RequestCreateSerializer
from users.permissions import IsStudent, IsInstructor, IsStudentOrInstructor
from rest_framework.permissions import IsAuthenticated
from academics.models import Subject
from django.utils import timezone

class RequestViewSet(viewsets.ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    permission_classes = [IsAuthenticated, IsStudentOrInstructor]
    http_method_names = ['get', 'post', 'patch', 'head', 'options']

    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            return self.queryset.filter(student=user.student_profile, grade=user.student_profile.grade)
        if user.role == 'instructor':
            return self.queryset.filter(
                subject__teaches__instructor=user.instructor_profile
            ).distinct()
        return self.queryset

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated(), IsStudent()]
        elif self.action in ['list', 'retrieve']:
            return [IsAuthenticated(), IsStudentOrInstructor()]
        elif self.action == 'partial_update':
            return [IsAuthenticated(), IsInstructor()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return RequestStatusUpdateSerializer
        if self.action == 'create':
            return RequestCreateSerializer
        if self.action in ['retrieve', 'list']:
            return RequestRetrieveSerializer
        return super().get_serializer_class()
    
    def perform_create(self, serializer):
        user = self.request.user.student_profile
        if self.request.user.role == 'student':
            serializer.save(student=user, grade=user.grade)
        
    def perform_update(self, serializer):
        if self.request.user.role == 'instructor':
            if 'status' in serializer.validated_data:
                serializer.save(replied_at=timezone.now())
            else:
                serializer.save()