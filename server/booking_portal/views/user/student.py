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
        ).order_by('-slot__date'))

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
    """View for booking machine"""

    # Retrieve form/form_model from template_dict
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
        ## Check if the instrument id and slot id match
        instr_obj = models.Instrument.objects.get(id=id)
        slot_obj = models.Slot.objects.get(
            id=slot_id,
            instrument=instr_obj,
            status=models.Slot.STATUS_1,
        )
        ## Check for student and supervisor
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
        ## Render form with initial data
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

    # Checks for form submission with valid data and then proceeds
    elif request.method == "POST" and form(request.POST).is_valid():
        try:
            ## Avoid multiple edits for same instrument slot
            with transaction.atomic():
                slot_obj = models.Slot.objects.filter(
                    id=slot_id,
                    status=models.Slot.STATUS_1,
                    instrument=instr_obj,
                ).first()

                if models.Request.objects.filter(
                    ~(
                        Q(status=models.Request.STATUS_4) |
                        Q(status=models.Request.STATUS_5)
                    ),
                    instrument=instr_obj,
                    student=student_obj,
                    slot__date__gt=now().date(),
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
                    ## Save request object and send email to users
                    ## Check Request post_save signal for more details
                    req_instance.save()
                    messages.success(request, 'Form Submission Successful')
                    return HttpResponseRedirect('/')

                # Slot got consumed by another person while filling the details
                elif not slot_obj:
                    messages.error(
                        request, "Sorry, This slot is not available anymore.")
                    return HttpResponseRedirect('/')

        except DatabaseError:
            ## When more than one user is trying for the same
            ## slot, this error is raised for the user who
            ## submitted the form later.
            messages.error(
                request, "Could not proccess your request, please try again.")
            return HttpResponseRedirect('/')

    else:
        ## There's an error in your form, render the form again
        ## Currently no other HTTP methods are supported, so this
        ## block will be called when there is some error in the form
        return render(
            request,
            'booking_portal/instrument_form.html',
            {
                'form': form(request.POST),
                ** default_context
            }
        )
