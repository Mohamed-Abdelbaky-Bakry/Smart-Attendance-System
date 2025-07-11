from core.base import BaseResponseMixin
from rest_framework import viewsets, permissions
from .models import AcademicYear, Subject, Enrollment, ClassSession, Department, AttendanceRecord, Teaches, SessionDate
from .serializers import AcademicYearSerializer, AttendanceRecordRetrieveSerializer, ClassSessionSerializer, AttendanceRecordSerializer, SessionDateRetrieveSerializer, SubjectSerializer, SessionDateSerializer, SubjectRetrieveSerializer, EnrollmentSerializer, DepartmentSerializer, EnrollmentRetrieveSerializer, ClassSessionRetrieveSerializer, TeachesRetrieveSerializer, TeachesSerializer
from users.permissions import IsAdmin, IsInstructorOrAdmin
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from users.models import Instructor


class AcademicYearViewSet(BaseResponseMixin, viewsets.ModelViewSet):
    queryset = AcademicYear.objects.all()
    serializer_class = AcademicYearSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsAdmin()]
        return [permissions.IsAuthenticated()]


class DepartmentViewSet(BaseResponseMixin, viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsAdmin()]
        return [permissions.IsAuthenticated()]
    

class SubjectViewSet(BaseResponseMixin, viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return SubjectRetrieveSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsAdmin()]
        return [permissions.IsAuthenticated()]


class EnrollmentViewSet(BaseResponseMixin, viewsets.ModelViewSet):
    queryset = Enrollment.objects.select_related(
        'student', 'subject', 'academic_year'
    ).all()
    serializer_class = EnrollmentSerializer

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return EnrollmentRetrieveSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsAdmin()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            return Enrollment.objects.filter(student=user.student_profile)
        return Enrollment.objects.all()
    

class ClassSessionViewSet(BaseResponseMixin, viewsets.ModelViewSet):
    queryset = ClassSession.objects.select_related('subject', 'instructor', 'academic_year').all()
    serializer_class = ClassSessionSerializer

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return ClassSessionRetrieveSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'list', 'retrieve']:
            return [permissions.IsAuthenticated(), IsInstructorOrAdmin()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'instructor':
            return ClassSession.objects.filter(instructor__account=user)
        return ClassSession.objects.all()
    

class TeachesViewSet(viewsets.ModelViewSet):
    queryset = Teaches.objects.all()
    serializer_class = TeachesSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Teaches.objects.all()
        if user.role == 'instructor':
            return Teaches.objects.filter(instructor=user.instructor_profile)
        return Teaches.objects.none()

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return TeachesRetrieveSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsAdmin()]
        return [permissions.IsAuthenticated()]

class SessionDateViewSet(viewsets.ModelViewSet):
    queryset = SessionDate.objects.all()
    serializer_class = SessionDateSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return SessionDateRetrieveSerializer
        return super().get_serializer_class()


class AttendanceRecordViewSet(viewsets.ModelViewSet):
    queryset = AttendanceRecord.objects.select_related('student__account', 'session_date', 'session_date__class_session')
    serializer_class = AttendanceRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'student':
            return self.queryset.filter(student__account=user)
        elif user.role == 'instructor':
            instructor = Instructor.objects.get(account=user)
            subjects = Teaches.objects.filter(instructor=instructor).values_list('subject_id', flat=True)
            return self.queryset.filter(session_date__class_session__subject_id__in=subjects)
        return self.queryset

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return AttendanceRecordRetrieveSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsAdmin()]
        return [permissions.IsAuthenticated()]

    @action(detail=False, methods=['get'])
    def by_student(self, request):
        student_id = request.query_params.get('student_id')
        if not student_id:
            return Response({'error': 'Missing student_id'}, status=400)

        records = self.get_queryset().filter(student__id=student_id)
        serializer = self.get_serializer(records, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_session(self, request):
        session_id = request.query_params.get('session_id')
        if not session_id:
            return Response({'error': 'Missing session_id'}, status=400)

        records = self.get_queryset().filter(session_date__id=session_id)
        serializer = self.get_serializer(records, many=True)
        return Response(serializer.data)