import random
import datetime
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q

from .config import form_template_dict, view_application_dict
from .forms.portal_forms import IntrumentList, SlotList
from .models import EmailModel, Instrument, Slot, Request, Student, Faculty, LabAssistant
from .permissions import is_faculty, is_lab_assistant, is_student


def index(request):
    context = {}
    faculty_instance = Faculty.objects.filter(username=request.user.username).first()
    student_instance = Student.objects.filter(username=request.user.username).first()
    lab_instance = LabAssistant.objects.filter(username=request.user.username).first()
    if faculty_instance:
        context = 'faculty'
    elif student_instance:
        context = 'student'
    elif lab_instance:
        context = 'lab'
    else:
        context = 'none'

    return render(request, 'home.html', {'usertype': context})

@login_required
@user_passes_test(is_student)
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
@user_passes_test(is_student)
def book_machine(request, id):
    template, form, _ = form_template_dict.get(id)
    if request.method == 'GET':
        return render(request, template, {'form': form(initial={'user_name': Student.objects.filter(username=request.user.username).first().id}),
                                                                'edit' : True})

    elif request.method == "POST" and form(request.POST).is_valid():
        slot_id = request.GET['slots']
        student_id = request.POST['user_name']
        faculty_id = request.POST['sup_name']

        instr_instance = Instrument.objects.filter(id=id).first()
        slot_instance = Slot.objects.filter(id=slot_id,
                                            status=Slot.STATUS_1,
                                            instrument=instr_instance).first()
        student_instance = Student.objects.filter(id=student_id).first()
        faculty_instance = Faculty.objects.filter(id=faculty_id).first()

        # TODO: Object Lock on Request Object
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
        else:
            return render(request, template, {'form': form(request.POST), 'edit' : True})

    else:
        return render(request, template, {'form': form(request.POST), 'edit' : True})

@login_required
@user_passes_test(is_student)
def slot_list(request):
    instr_id = request.POST['instruments']
    instr_obj = Instrument.objects.get(id=instr_id)
    instr_name = instr_obj.name

    check_prev_slots = Slot.objects.filter((Q(status=Slot.STATUS_2) | Q(status=Slot.STATUS_3))
                                            & Q(date__gte=datetime.datetime.today()))

    if len(check_prev_slots) >= 1 :
        return render(request, 'booking_portal/portal_forms/instrument_list.html',
                      {'form' : IntrumentList(),
                      "message":'You cannot book a slot for this instrument since you already have a booking !'})
    else :
        form = SlotList(instr_id)
        return render(request, 'booking_portal/portal_forms/slot_list.html',
                  {'instrument_name': instr_obj.name, 'instrument_id': instr_id, 'form': form})

@login_required
@user_passes_test(is_faculty)
def faculty_portal(request):
    requests_objects = Request.objects.filter(faculty=request.user, status=Request.STATUS_1).order_by('slot__date').reverse()
    return render(request, 'booking_portal/portal_forms/faculty_portal.html',
                  {'requests': requests_objects, 'usertype': 'faculty'})


@login_required
@user_passes_test(is_faculty)
def faculty_request_accept(request, id):
    try:
        request_object = Request.objects.get(id=id)
    except:
        raise Http404()
    faculty = request_object.faculty
    if (faculty == Faculty.objects.get(id=request.user.id)):
        request_object.status = Request.STATUS_2
        request_object.message = "accept"
        request_object.lab_assistant = random.choice(LabAssistant.objects.all())
        request_object.save()
        return faculty_portal(request)
    else:
        return HttpResponse("Bad Request")


@login_required
@user_passes_test(is_faculty)
def faculty_request_reject(request, id):
    try:
        request_object = Request.objects.get(id=id)
    except:
        raise Http404()
    faculty = request_object.faculty
    if (faculty == Faculty.objects.get(id=request.user.id)):
        request_object.status = Request.STATUS_2
        request_object.message = "reject"
        request_object.save()
        return faculty_portal(request)
    else:
        return HttpResponse("Bad Request")

@login_required
@user_passes_test(is_lab_assistant)
def lab_assistant_portal(request):
    request_objects = Request.objects.filter(lab_assistant=request.user, status=Request.STATUS_2).order_by('slot__date').reverse()
    return render(request, 'booking_portal/portal_forms/lab_assistant_portal.html',
                  {'requests': request_objects, 'usertype': 'lab'})

@login_required
@user_passes_test(is_lab_assistant)
def lab_assistant_accept(request, id):
    try:
        request_object = Request.objects.get(id=id)
    except:
        raise Http404()
    lab_assistant = request_object.lab_assistant
    if (lab_assistant == LabAssistant.objects.get(id=request.user.id)):
        request_object.status = Request.STATUS_3
        request_object.message = "accept"
        request_object.save()
        return lab_assistant_portal(request)
    else:
        return HttpResponse("Bad Request")

@login_required
@user_passes_test(is_lab_assistant)
def lab_assistant_reject(request, id):
    try:
        request_object = Request.objects.get(id=id)
    except:
        raise Http404()
    lab_assistant = request_object.lab_assistant
    if (lab_assistant == LabAssistant.objects.get(id=request.user.id)):
        request_object.status = Request.STATUS_3
        request_object.message = "reject"
        request_object.save()
        return lab_assistant_portal(request)
    else:
        return HttpResponse("Bad Request")

@login_required
@user_passes_test(is_student)
def student_portal(request):
    request_objects = Request.objects.filter(student=request.user).order_by('slot__date').reverse()
    return render(request, 'booking_portal/portal_forms/student_portal.html',
                  {'requests': request_objects, 'usertype': 'student'})

@login_required
def show_application(request, id):
    try:
        request_obj = Request.objects.get(id=id)
    except:
        raise Http404()
    content_object = request_obj.content_object
    template, form = view_application_dict[content_object._meta.model]

    data = content_object.__dict__
    data['user_name'] = Student.objects.get(id=data['user_name_id'])
    data['sup_name'] = Faculty.objects.get(id=data['sup_name_id'])
    form_object = form(data)

    for field_val, val in data.items():
        try:
            form_object.fields[field_val].widget.attrs['readonly'] = True
        except KeyError:
            pass

    return render(request, template, {'form': form_object, 'edit' : False})