from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .forms.fesemform import FESEMForm
from .forms.tcspcform import TCSPCForm
from .forms.ftirform import FTIRForm
from .forms.lcmsform import LCMSForm
from .forms.portal_forms import IntrumentList
from .models import EmailModel

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
    if id == 1:
        if request.method == 'POST':
            form = FESEMForm(request.POST)
            if form.is_valid():
                return HttpResponse('Submission successful for FESEMForm')
        else:
            form = FESEMForm()
        return render(request, 'booking_portal/fesem.html', {'form': form})

    elif id == 2:
        if request.method == 'POST':
            form = TCSPCForm(request.POST)
            if form.is_valid():
                return HttpResponse('Submission Successful for TCSPCForm')
        else:
            form = TCSPCForm()
        return render(request, 'booking_portal/tcspc.html', {'form': form})

    elif id == 3:
        if request.method == 'POST':
            form = FTIRForm(request.POST)
            if form.is_valid():
                return HttpResponse("Submission successful for FTIRForm")
        else:
            form = FTIRForm()
        return render(request, 'booking_portal/ftir.html', {'form': form})

    elif id == 4:
        if request.method == 'POST':
            form = LCMSForm(request.POST)
            if form.is_valid():
                return HttpResponse("Submission successful for LCMSForm")
        else:
            form = LCMSForm()
        return render(request, 'booking_portal/lcms.html', {'form': form})

    else:
        return HttpResponse('Form for this ID has not been built yet')

