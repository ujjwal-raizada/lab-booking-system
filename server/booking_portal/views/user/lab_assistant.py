from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

from ... import models, permissions


@login_required
@user_passes_test(permissions.is_lab_assistant)
def lab_assistant_portal(request):
    request_objects = models.Request.objects.filter(lab_assistant=request.user, status=models.Request.STATUS_2).order_by('slot__date').reverse()
    return render(request, 'booking_portal/portal_forms/lab_assistant_portal.html',
                  {'requests': request_objects, 'usertype': 'lab'})


@login_required
@user_passes_test(permissions.is_lab_assistant)
def lab_assistant_accept(request, id):
    try:
        request_object = models.Request.objects.get(id=id)
    except:
        raise Http404()
    lab_assistant = request_object.lab_assistant
    if (lab_assistant == models.LabAssistant.objects.get(id=request.user.id)):
        request_object.status = models.Request.STATUS_3
        request_object.message = "accept"
        request_object.save()
        return lab_assistant_portal(request)
    else:
        return HttpResponse("Bad Request")


@login_required
@user_passes_test(permissions.is_lab_assistant)
def lab_assistant_reject(request, id):
    try:
        request_object = models.Request.objects.get(id=id)
    except:
        raise Http404()
    lab_assistant = request_object.lab_assistant
    if (lab_assistant == models.LabAssistant.objects.get(id=request.user.id)):
        request_object.status = models.Request.STATUS_3
        request_object.message = "reject"
        request_object.save()
        return lab_assistant_portal(request)
    else:
        return HttpResponse("Bad Request")
