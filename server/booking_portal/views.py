from django.http import HttpResponse
from django.shortcuts import render

from .forms.fesemform import FESEMForm
from .forms.tcspcform import TCSPCForm
from .forms.ftirform import FTIRForm
from .forms.lcmsform import LCMSForm

def index(request):
    context = {
    }
    return render(request, 'home.html', context=context)

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