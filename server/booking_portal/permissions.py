from django.contrib.auth.decorators import user_passes_test

from .models import Student, Faculty, LabAssistant


def is_faculty(user):
    if (len(Faculty.objects.filter(id=user.id))) > 0:
        return True
    return False

def is_student(user):
    if (len(Student.objects.filter(id=user.id))) > 0:
        return True
    return False

def is_lab_assistant(user):
    if (len(LabAssistant.objects.filter(id=user.id))) > 0:
        return True
    return False
