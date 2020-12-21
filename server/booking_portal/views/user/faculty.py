import random

from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.db import transaction

from ... import models, permissions
from .portal import BasePortalFilter


@login_required
@user_passes_test(permissions.is_faculty)
def faculty_portal(request):
    f = BasePortalFilter(
        request.GET,
        queryset=models.Request.objects.filter(
            faculty=request.user,
        ))

    return render(
        request,
        'booking_portal/portal_forms/faculty_portal.html',
        {
            'context_data': f,
            'usertype': 'faculty'
        }
    )


@login_required
@user_passes_test(permissions.is_faculty)
def faculty_request_accept(request, id):
    try:
        with transaction.atomic():
            request_object = models.Request.objects.get(
                id=id,
                status=models.Request.STATUS_1)
            faculty = request_object.faculty
            if (faculty == models.Faculty.objects.get(id=request.user.id)):
                request_object.status = models.Request.STATUS_2
                request_object.lab_assistant = random.choice(
                    models.LabAssistant.objects.all())
                request_object.save()
                return redirect('faculty_portal')
            else:
                return HttpResponse("Bad Request")
    except Exception as e:
        raise Http404("Page Not Found")


@login_required
@user_passes_test(permissions.is_faculty)
def faculty_request_reject(request, id):
    try:
        with transaction.atomic():
            request_object = models.Request.objects.get(
                id=id,
                status=models.Request.STATUS_1)
            faculty = request_object.faculty
            if (faculty == models.Faculty.objects.get(id=request.user.id)):
                request_object.status = models.Request.STATUS_4
                request_object.save()
                return redirect('faculty_portal')
            else:
                return HttpResponse("Bad Request")
    except Exception as e:
        raise Http404("Page Not Found")
