from django.http import Http404
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from ..models import Faculty, Student, LabAssistant, Request
from ..config import view_application_dict


def index(request):
    context = {}
    faculty_instance = Faculty.objects.filter(id=request.user.id).first()
    student_instance = Student.objects.filter(id=request.user.id).first()
    lab_instance = LabAssistant.objects.filter(id=request.user.id).first()
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
            form_object.fields[field_val].widgets.attrs['disabled'] = True
            form_object.fields[field_val].widget.attrs['readonly'] = True
        except KeyError:
            pass

    return render(request, template, {'form': form_object, 'edit' : False})
