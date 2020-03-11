import random
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .config import form_template_dict
from .forms.portal_forms import IntrumentList, SlotList
from .models import EmailModel, Instrument, Slot, Request, Student, Faculty, LabAssistant

def index(request):
    context = {
    }
    return render(request, 'home.html', context=context)

@login_required
def instrument_list(request):
    form = IntrumentList()
    return render(request, 'booking_portal/portal_forms/instrument_list.html', {'form': form})

@login_required
def email(request):
    emails = EmailModel.objects.all()
    context = {
        'emails': emails,
    }
    return render(request, 'email.html', context=context)

@login_required
def book_machine(request, id):
    template, form = form_template_dict.get(id)
    if request.method == 'GET':
        return render(request, template, {'form': form()})

    elif request.method == 'POST': 
        f = form(request.POST)
        if f.is_valid():
            slot_id = request.GET['slots']
            student_name = request.POST['user_name']
            faculty_name = request.POST['sup_name']

            instr_instance = Instrument.objects.filter(id=id).first()
            slot_instance = Slot.objects.filter(id=slot_id,
                                                status=Slot.STATUS_1,
                                                instrument=instr_instance).first()
            student_instance = Student.objects.filter(username=student_name).first()
            faculty_instance = Faculty.objects.filter(username=faculty_name).first()

            # TODO: Object Lock on Request Object
            if slot_instance and student_instance and faculty_instance and instr_instance:
                req_instance = Request(student=student_instance,
                                        faculty=faculty_instance,
                                        instrument=instr_instance,
                                        slot=slot_instance,
                                        status=Request.STATUS_1)
                req_instance.save()
                f.save()
                return HttpResponse("Submission Successful")
            else:
                return HttpResponse('Submission Failed')
        else:
            return render(request, template, {'form': form()})

@login_required
def slot_list(request):
    instr_id = request.POST['instruments']
    instr_name = Instrument.objects.get(id=instr_id).name
    form = SlotList(instr_id)
    return render(request, 'booking_portal/portal_forms/slot_list.html',
                  {'instrument_name': instr_name, 'instrument_id': instr_id, 'form': form})

@login_required
def faculty_portal(request):
    print(request.user)
    requests_objects = Request.objects.filter(faculty=request.user, status=Request.STATUS_1)
    print(requests_objects)
    return render(request, 'booking_portal/portal_forms/faculty_portal.html',
                  {'requests': requests_objects})


@login_required
def faculty_request_accept(request, id):

    #TODO: match faculty access
    request_object = Request.objects.get(id=id)
    request_object.status = Request.STATUS_2
    request_object.message = "accept"
    request_object.lab_assistant = random.choice(LabAssistant.objects.all())
    request_object.save()
    return faculty_portal(request)


@login_required
def faculty_request_reject(request, id):

    #TODO: match faculty access
    request_object = Request.objects.get(id=id)
    request_object.status = Request.STATUS_2
    request_object.message = "reject"
    request_object.save()
    return faculty_portal(request)

@login_required
def lab_assistant_portal(request):
    request_objects = Request.objects.filter(lab_assistant=request.user, status=Request.STATUS_2)
    return render(request, 'booking_portal/portal_forms/lab_assistant_portal.html',
                  {'requests': request_objects})

@login_required
def lab_assistant_accept(request, id):
    request_object = Request.objects.get(id=id)
    request_object.status = Request.STATUS_3
    request_object.message = "accept"
    request_object.save()
    return lab_assistant_portal(request)

@login_required
def lab_assistant_reject(request, id):
    request_object = Request.objects.get(id=id)
    request_object.status = Request.STATUS_3
    request_object.message = "reject"
    request_object.save()
    return lab_assistant_portal(request)

@login_required
def student_portal(request):
    request_objects = Request.objects.filter(student=request.user)
    return render(request, 'booking_portal/portal_forms/student_portal.html',
                  {'requests': request_objects})
