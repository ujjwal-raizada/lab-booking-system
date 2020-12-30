import datetime

from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from django.db import transaction, DatabaseError
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.utils.timezone import now

from ... import models
from ... import permissions
from ... import config
from .portal import BasePortalFilter


@login_required
@user_passes_test(permissions.is_student)
def student_portal(request):
    f = BasePortalFilter(
        request.GET,
        queryset=models.Request.objects.filter(
            student=request.user
        ))

    return render(
        request,
        'booking_portal/portal_forms/student_portal.html',
        {
            'context_data': f,
            'usertype': 'student'
        }
    )


@login_required
@user_passes_test(permissions.is_student)
def book_machine(request, id):
    form, form_model = config.form_template_dict.get(id)
    slot_id = request.GET['slots']
    default_context = {
        'edit': True,
        'instrument_title': form.title,
        'instrument_subtitle': form.subtitle,
        'instrument_verbose_name': form_model._meta.verbose_name,
        'form_notes': form.help_text,
        'usertype': 'student',
        'status': models.Request.STATUS_1,
    }

    try:
        instr_obj = models.Instrument.objects.get(id=id)
        slot_obj = models.Slot.objects.get(
            id=slot_id,
            instrument=instr_obj,
            status=models.Slot.STATUS_1,
            date__gte=now().date(),
        )
        student_obj = models.Student.objects.get(
            id=request.user.id
        )
        sup_obj = models.Faculty.objects.get(
            id=student_obj.supervisor.id
        )

    except:
        messages.error(request, "Bad Request")
        return HttpResponseRedirect("/")

    if request.method == 'GET':

        return render(
            request,
            'booking_portal/instrument_form.html',
            {
                'form': form(initial={
                    'user_name': student_obj.id,
                    'sup_name': sup_obj.id,
                    'sup_dept': sup_obj.department,
                    'date': slot_obj.date,
                    'time': slot_obj.time,
                    'duration': slot_obj.duration_verbose,
                }),
                ** default_context,
            }
        )

    elif request.method == "POST" and form(request.POST).is_valid():
        try:
            with transaction.atomic():
                slot_obj = models.Slot.objects.filter(
                    id=slot_id,
                    status=models.Slot.STATUS_1,
                    instrument=instr_obj,
                    date__gte=now().date(),
                ).first()

                if models.Request.objects.filter(
                    ~(
                        Q(status=models.Request.STATUS_4) |
                        Q(status=models.Request.STATUS_5)
                    ),
                    instrument=instr_obj,
                    student=student_obj,
                    slot__date__gte=now().date(),
                ).exists():
                    messages.error(
                        request,
                        "You already have an ongoing application for this machine"
                    )
                    return HttpResponseRedirect("/")

                if slot_obj and student_obj and sup_obj and instr_obj:
                    model_object = form(request.POST).save()
                    req_instance = models.Request(
                        student=student_obj,
                        faculty=sup_obj,
                        instrument=instr_obj,
                        slot=slot_obj,
                        status=models.Request.STATUS_1,
                        content_object=model_object
                    )
                    req_instance.save()
                    messages.success(request, 'Form Submission Successful')
                    return HttpResponseRedirect('/')

                elif not slot_obj:
                    messages.error(
                        request, "Sorry, This slot is not available anymore.")
                    return HttpResponseRedirect('/')

        except DatabaseError:
            messages.error(
                request, "Could not proccess your request, please try again.")
            return HttpResponseRedirect('/')

    else:
        return render(
            request,
            'booking_portal/instrument_form.html',
            {
                'form': form(request.POST),
                ** default_context
            }
        )
