from datetime import datetime
from django.db.models import Sum
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import *
from .forms import *

# def polling_unit_result(request, polling_unit_id):
#     result = AnnouncedPuResults.objects.filter(
#         polling_unit_uniqueid=polling_unit_id)
#     return render(request, 'polling_unit_result.html', {'result': result})


def home(request):
    return render(request, 'home.html')


def view_poll_result(request):
    if request.method == 'POST':
        form = ViewPollResult(request.POST)
        if form.is_valid():
            result = form.cleaned_data['polling_unit_uniqueid']
            return redirect('polling_unit_result', polling_unit_uniqueid=result)
    else:
        form = ViewPollResult()
    return render(request, 'view_poll_result.html', {'form': form})


def polling_unit_result(request, polling_unit_uniqueid):
    result = AnnouncedPuResults.objects.filter(
        polling_unit_uniqueid=polling_unit_uniqueid
        )
    
    try:
        polling_unit = PollingUnit.objects.get(uniqueid=polling_unit_uniqueid)
        pu_name = polling_unit.polling_unit_name  # get the name of the LGA
        context = {
            'result': result,
            'pu_name': pu_name

        }
    except PollingUnit.DoesNotExist:
        context = {
            'result': result,
        }

    return render(request, 'polling_unit_result.html', context)



# myproject/views.py


def lga_result(request):
    lgas = Lga.objects.all()
    selected_lga = request.GET.get('lga', None)
    total_result = None

    if selected_lga:
        lga = Lga.objects.get(lga_id= int(selected_lga))
        lga_name = Lga.objects.get(lga_id=selected_lga).lga_name
        # polling_units = PollingUnit.objects.filter(lga_id=lga.lga_id)
        # total_result = AnnouncedPuResults.objects.filter(polling_unit__in=polling_units).aggregate(
        #     Sum('party_score'))['party_score__sum']
        polling_units = PollingUnit.objects.filter(lga_id=lga.lga_id)
        total_result = AnnouncedPuResults.objects.filter(polling_unit_uniqueid__in=polling_units.values('uniqueid')).aggregate(
            Sum('party_score'))['party_score__sum']
    else:
        lga_name = 'no lga selected yet'

    context = {
        'lgas': lgas,
        'selected_lga': selected_lga,
        'lga_name' :  lga_name,
        'total_result': total_result,
    }

    return render(request, 'lga_results.html', context)


def add_polling_unit_result(request):
    if request.method == 'POST':
        form = AddPollingUnitResultForm(request.POST)
        if form.is_valid():
            result = form.save(commit=False)
            # set the date_entered column to the current date and time
            result.date_entered = datetime.now()
            result.save()
            return redirect('polling_unit_result', polling_unit_uniqueid=result.polling_unit_uniqueid)
    else:
        form = AddPollingUnitResultForm()
    return render(request, 'add_polling_unit_result.html', {'form': form})








# def new_polling_unit(request, pu_id):
#     for pu in PollingUnit.objects.filter()
    

# def total_result(request):
#     if request.method == 'POST':
#         lga_id = request.POST.get('lga')
#         lga = Lga.objects.get(id=lga_id)
#         polling_units = PollingUnit.objects.filter(lga=lga)
#         total_results = []
#         for party in Party.objects.all():
#             total_score = 0
#             for pu in polling_units:
#                 try:
#                     result = AnnouncedPuResults.objects.get(
#                         polling_unit=pu, party=party)
#                     total_score += result.party_score
#                 except AnnouncedPuResults.DoesNotExist:
#                     pass
#             total_results.append({'party': party, 'total_score': total_score})
#         context = {'lga': lga, 'total_results': total_results}
#         return render(request, 'total_result.html', context)
#     else:
#         lgas = Lga.objects.filter(state_id=25)
#         context = {'lgas': lgas}
#         return render(request, 'select_lga.html', context)
