from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction

from ... import models, permissions
from .portal import BasePortalFilter


@login_required
@user_passes_test(permissions.is_lab_assistant)
def lab_assistant_portal(request):
    f = BasePortalFilter(
            request.GET,
            queryset= models.Request.objects.all()
        )

    return render(
        request,
        'booking_portal/portal_forms/lab_assistant_portal.html',
        {
            'context_data' : f,
            'usertype': 'lab'
        }
    )


@login_required
@user_passes_test(permissions.is_lab_assistant)
def lab_assistant_accept(request, id):
    try:
        with transaction.atomic():
            request_object = models.Request.objects.get(
                                                    id=id,
                                                    status=models.Request.STATUS_2
            )
            lab_assistant = request_object.lab_assistant
            if (lab_assistant == models.LabAssistant.objects.get(id=request.user.id)):
                request_object.status = models.Request.STATUS_3
                request_object.save()
                return lab_assistant_portal(request)
            else:
                return HttpResponse("Bad Request")
    except:
        raise Http404("Page Not Found")


@transaction.atomic
@login_required
@user_passes_test(permissions.is_lab_assistant)
def lab_assistant_reject(request, id):
    try:
        with transaction.atomic():
            request_object = models.Request.objects.get(
                                                    id=id,
                                                    status=models.Request.STATUS_2
            )
            lab_assistant = request_object.lab_assistant
            if (lab_assistant == models.LabAssistant.objects.get(id=request.user.id)):
                request_object.status = models.Request.STATUS_4
                request_object.save()
                return lab_assistant_portal(request)
            else:
                return HttpResponse("Bad Request")
    except:
        raise Http404("Page Not Found")
