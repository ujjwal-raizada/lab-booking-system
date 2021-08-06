from django.contrib.auth.decorators import user_passes_test

from .models import CustomUser, Student, Faculty, LabAssistant


def is_faculty(user: CustomUser):
    if (len(Faculty.objects.filter(email=user.username))) > 0:
        return True
    return False


def is_student(user: CustomUser):
    if (len(Student.objects.filter(email=user.username))) > 0:
        return True
    return False


def is_lab_assistant(user: CustomUser):
    if (len(LabAssistant.objects.filter(email=user.username))) > 0:
        return True
    return False


def get_user_type(user: CustomUser):
    return (
        "faculty" if is_faculty(user) else
        "assistant" if is_lab_assistant(user) else
        "student" if is_student(user) else
        None
    )
