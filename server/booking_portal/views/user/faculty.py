import random

from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render

from ... import models, permissions


@login_required
@user_passes_test(permissions.is_faculty)
def faculty_portal(request):
    requests_objects = models.Request.objects.filter(
                                    faculty=request.user,
                                    status=models.Request.STATUS_1).order_by('slot__date').reverse()
    return render(request, 'booking_portal/portal_forms/faculty_portal.html',
                  {'requests': requests_objects, 'usertype': 'faculty'})


@login_required
@user_passes_test(permissions.is_faculty)
def faculty_request_accept(request, id):
    try:
        request_object = models.Request.objects.get(id=id)
    except:
        raise Http404()
    faculty = request_object.faculty
    if (faculty == models.Faculty.objects.get(id=request.user.id)):
        request_object.status = models.Request.STATUS_2
        request_object.message = "accept"
        request_object.lab_assistant = random.choice(models.LabAssistant.objects.all())
        request_object.save()
        return faculty_portal(request)
    else:
        return HttpResponse("Bad Request")


@login_required
@user_passes_test(permissions.is_faculty)
def faculty_request_reject(request, id):
    try:
        request_object = models.Request.objects.get(id=id)
    except:
        raise Http404()
    faculty = request_object.faculty
    if (faculty == models.Faculty.objects.get(id=request.user.id)):
        request_object.status = models.Request.STATUS_2
        request_object.message = "reject"
        request_object.save()
        return faculty_portal(request)
    else:
        return HttpResponse("Bad Request")