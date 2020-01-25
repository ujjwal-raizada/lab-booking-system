from django.http import HttpResponse
from django.shortcuts import render

from .forms import FESEMForm

def index(request):
    context = {
    }
    return render(request, 'home.html', context=context)

def book_machine(request):
    if request.method == 'POST':
        form = FESEMForm(request.POST)
        if form.is_valid():
            return HttpResponse('Thanks')

    else:
        form = FESEMForm()

    return render(request, 'booking_portal/fesem.html', {'form': form})
