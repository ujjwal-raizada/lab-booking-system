import datetime

from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.decorators import login_required, user_passes_test

from ..forms.portal_forms import IntrumentList, SlotList
from ..models import Instrument, Slot, Request, Student
from ..permissions import is_student


@login_required
@user_passes_test(is_student)
def slot_list(request):
    instr_id = request.POST['instruments']
    instr_obj = Instrument.objects.get(id=instr_id)
    instr_name = instr_obj.name
    student_obj = Student.objects.get(id=request.user.id)

    if Request.objects.filter(
        ~(
            Q(status=Request.STATUS_4) |
            Q(status=Request.STATUS_5)
        ),
        instrument=instr_obj,
        student=student_obj
    ).exists():
        return render(
            request,
            'booking_portal/portal_forms/instrument_list.html',
            {
                'form' : IntrumentList(),
                "message":'You cannot book a slot for this instrument since you already have a booking !'
            }
        )
    else :
        form = SlotList(instr_id)
        return render(
            request,
            'booking_portal/portal_forms/slot_list.html',
            {
                'instrument_name': instr_obj.name,
                'instrument_id': instr_id,
                'form': form
            }
        )
