from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction, DatabaseError

from ..forms.portal_forms import IntrumentList
from ..config import form_template_dict
from ..models import Request, Faculty, Student, Instrument, Slot
from ..permissions import is_student


@login_required
@user_passes_test(is_student)
def instrument_list(request):
    form = IntrumentList()
    return render(request, 'booking_portal/portal_forms/instrument_list.html', {'form': form})


@login_required
@user_passes_test(is_student)
def book_machine(request, id):
    template, form, _ = form_template_dict.get(id)
    if request.method == 'GET':
        student_obj = Student.objects.filter(id=request.user.id).first()
        sup_obj = Faculty.objects.filter(id=student_obj.supervisor.id).first()

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
                instr_instance = Instrument.objects.filter(id=id).first()
                slot_instance = Slot.objects.select_for_update(nowait=True).filter(
                                                        id=slot_id,
                                                        status=Slot.STATUS_1,
                                                        instrument=instr_instance).first()
                student_instance = Student.objects.filter(id=student_id).first()
                faculty_instance = Faculty.objects.filter(id=faculty_id).first()

                if Request.objects.filter(instrument=instr_instance,
                                          student=student_instance).exists():

                    messages.error(request, "You already have an ongoing application for this machine")
                    return HttpResponseRedirect("/booking/")

                if slot_instance and student_instance and faculty_instance and instr_instance:
                    model_object = form(request.POST).save()
                    req_instance = Request(student=student_instance,
                                            faculty=faculty_instance,
                                            instrument=instr_instance,
                                            slot=slot_instance,
                                            status=Request.STATUS_1,
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
