from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from django.db import transaction, DatabaseError
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseRedirect

from ... import models
from ... import permissions
from ... import config


@login_required
@user_passes_test(permissions.is_student)
def student_portal(request):
    request_objects = models.Request.objects.filter(student=request.user).order_by('slot__date').reverse()
    return render(request, 'booking_portal/portal_forms/student_portal.html',
                  {'requests': request_objects, 'usertype': 'student'})


@login_required
@user_passes_test(permissions.is_student)
def book_machine(request, id):
    template, form, _ = config.form_template_dict.get(id)
    if request.method == 'GET':
        student_obj = models.Student.objects.filter(id=request.user.id).first()
        sup_obj = models.Faculty.objects.filter(id=student_obj.supervisor.id).first()

        return render(request, template, {
            'form': form(initial={
                    'user_name': student_obj.id,
                    'sup_name': sup_obj.id,
                    'sup_dept': sup_obj.department,
                }),
            'edit' : True
        })

    elif request.method == "POST" and form(request.POST).is_valid():
        slot_id = request.GET['slots']
        student_id = request.POST['user_name']
        faculty_id = request.POST['sup_name']

        try:
            with transaction.atomic():
                instr_instance = models.Instrument.objects.filter(id=id).first()
                slot_instance = models.Slot.objects.filter(id=slot_id,
                                                           status=models.Slot.STATUS_1,
                                                           instrument=instr_instance).first()
                student_instance = models.Student.objects.filter(id=student_id).first()
                faculty_instance = models.Faculty.objects.filter(id=faculty_id).first()

                if models.Request.objects.filter(instrument=instr_instance,
                                                 status= ~(Q(status=models.Request.STATUS_4) |
                                                           Q(status=models.Request.STATUS_5)),
                                                 student=student_instance).exists():

                    messages.error(request, "You already have an ongoing application for this machine")
                    return HttpResponseRedirect("/booking/")

                if slot_instance and student_instance and faculty_instance and instr_instance:
                    model_object = form(request.POST).save()
                    req_instance = models.Request(student=student_instance,
                                            faculty=faculty_instance,
                                            instrument=instr_instance,
                                            slot=slot_instance,
                                            status=models.Request.STATUS_1,
                                            content_object=model_object)
                    req_instance.save()
                    messages.success(request, 'Form Submission Successful')
                    return HttpResponseRedirect('/booking/')

                elif not slot_instance:
                    messages.error(request, "Sorry, This slot is not available anymore.")
                    return HttpResponseRedirect('/booking/')

        except DatabaseError:
            messages.error(request, "Could not proccess your request, please try again.")
            return HttpResponseRedirect('/booking/')

    else:
        return render(request, template, {'form': form(request.POST), 'edit' : True})