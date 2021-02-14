import datetime

from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.timezone import now

from ..forms.portal_forms import IntrumentList, SlotList
from ..models import Instrument, Slot, Request, Student
from ..permissions import is_student
from django.http import HttpResponseRedirect
from django.contrib import messages


@login_required
@user_passes_test(is_student)
def slot_list(request):
    try:
        instr_id = request.POST['instruments']
        instr_obj = Instrument.objects.get(id=instr_id)
        instr_name = instr_obj.name
        student_obj = Student.objects.get(id=request.user.id)
    except:
        messages.error(request, "Bad Request")
        return HttpResponseRedirect("/")


    if not instr_obj.status:
        ## If the instrument has been cancelled by the user
        return render(
            request,
            'booking_portal/portal_forms/instrument_list.html',
            {
                'form': IntrumentList(),
                "message": 'Instrument unavailable due to technical/maintainence reasons'
            }
        )

    # Check if a student has already one booking for the specified instrument, if yes then
    # he / she is not allowed another booking until the slot is consumed
    elif Request.objects.filter(
        ~(
            Q(status=Request.REJECTED) |
            Q(status=Request.CANCELLED)
        ),
        instrument=instr_obj,
        student=student_obj,
        slot__date__gt=now().date(),
    ).exists():
        return render(
            request,
            'booking_portal/portal_forms/instrument_list.html',
            {
                'form': IntrumentList(),
                "message": "Error. You already have a pending/approved request."
            }
        )
    else:
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
