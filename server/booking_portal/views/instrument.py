from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

from ..forms.portal_forms import IntrumentList
from ..config import form_template_dict
from ..models import Request, Faculty, Student, Instrument, Slot
from ..permissions import is_student


@login_required
@user_passes_test(is_student)
def instrument_list(request):
    form = IntrumentList()
    return render(request, 'booking_portal/portal_forms/instrument_list.html', {'form': form})
