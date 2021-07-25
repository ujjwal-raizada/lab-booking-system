from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from ..forms.portal import InstrumentList, SlotList
from ..models import Request
from ..permissions import is_student


@login_required
@user_passes_test(is_student)
def slot_list(request):
    if not request.method == 'POST':
        messages.error(request, "Bad Request")
        return HttpResponseRedirect(reverse('instrument-list'))

    form = InstrumentList(request.POST)
    if not form.is_valid():
        messages.error(request, "Bad Request")
        return HttpResponseRedirect(reverse('instrument-list'))

    instr = form.cleaned_data['instruments']
    if not instr.status:
        # Instrument not available
        return render(
            request,
            'booking_portal/portal_forms/instrument_list.html',
            {
                'form': InstrumentList(),
                'message': "Instrument unavailable due to technical/maintainence reasons."
            }
        )
    if Request.objects.has_student_booked_upcoming_instrument_slot(instr, request.user):
        return render(
            request,
            'booking_portal/portal_forms/instrument_list.html',
            {
                'form': InstrumentList(),
                "message": "Error. You already have a pending request for this instrument."
            }
        )

    return render(
        request,
        'booking_portal/portal_forms/slot_list.html',
        {
            'instrument_name': instr.name,
            'instrument_id': instr.pk,
            'form': SlotList(instr)
        }
    )
