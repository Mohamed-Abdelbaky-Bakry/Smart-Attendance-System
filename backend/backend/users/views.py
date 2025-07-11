from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import Account, Student, Instructor
from .serializers import AccountSerializer, StudentSerializer, InstructorSerializer, StudentRetriveSerializer, InstructorRetrieveSerializer
from .permissions import IsAdmin, IsInstructor
from core.base import BaseResponseMixin
from rest_framework import permissions

class AccountViewSet(BaseResponseMixin, viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsAdmin()]
        return [permissions.IsAuthenticated()]
    
    def perform_create(self, serializer):
        password = serializer.validated_data.pop('password')
        account = serializer.save()
        account.set_password(password)
        account.save()
        return account

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        account = self.perform_create(serializer)
        data = AccountSerializer(account).data
        return Response({'is_successful': True, 'errors': None, 'data': data}, status=status.HTTP_201_CREATED)
    

class StudentViewSet(BaseResponseMixin, viewsets.ModelViewSet):
    queryset = Student.objects.select_related('account').all()
    serializer_class = StudentSerializer

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return StudentRetriveSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsAdmin()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            return Student.objects.filter(account=user)
        elif user.role == 'instructor':
            return Student.objects.all()
        elif user.role == 'admin':
            return Student.objects.all()
        return Student.objects.none()


class InstructorViewSet(BaseResponseMixin, viewsets.ModelViewSet):
    queryset = Instructor.objects.select_related('account').all()
    serializer_class = InstructorSerializer

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return InstructorRetrieveSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsAdmin()]
        return [permissions.IsAuthenticated()]

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, username=email, password=password)
        if user and user.is_active:
            login(request, user)
            data = AccountSerializer(user).data
            return Response({'is_successful': True, 'errors': None, 'data': data})
        return Response({'is_successful': False, 'errors': ['Invalid credentials'], 'data': None}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        logout(request)
        return Response({'is_successful': True, 'errors': None, 'data': {'message': 'Logged out'}})