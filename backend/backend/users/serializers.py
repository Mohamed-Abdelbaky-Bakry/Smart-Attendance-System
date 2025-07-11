from rest_framework import serializers
from .models import Account, Student, Instructor

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'name', 'email', 'mobile_number', 'role', 'password', 'last_login', 'is_active', 'is_verified']
        extra_kwargs = {
            'password': {"write_only": True},
            'last_login': {"read_only": True},
            'is_verified': {"read_only": True}
        }
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        account = Account(**validated_data)
        if password:
            account.set_password(password)
        account.save()
        return account

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

class StudentRetriveSerializer(serializers.ModelSerializer):
    account = AccountSerializer(read_only=True)
    class Meta:
        model = Student
        fields = ['account', 'student_code', 'date_of_birth', 'gender', 'address', 'enrollment_date', 'department', 'grade']


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['account', 'student_code', 'date_of_birth', 'gender', 'address', 'enrollment_date', 'department', 'grade']


class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructor
        fields = ['account', 'department', 'hire_date']

class InstructorRetrieveSerializer(serializers.ModelSerializer):
    account = AccountSerializer(read_only=True)
    class Meta:
        model = Instructor
        fields = ['account', 'department', 'hire_date']