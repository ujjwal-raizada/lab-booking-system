from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render

from ... import models
from ... import permissions


@login_required
@user_passes_test(permissions.is_student)
def student_portal(request):
    request_objects = models.Request.objects.filter(student=request.user).order_by('slot__date').reverse()
    return render(request, 'booking_portal/portal_forms/student_portal.html',
                  {'requests': request_objects, 'usertype': 'student'})
