from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .forms import geocodeForm, exportForm, attributeFilterForm
from NREL_DataMining.src.NREL_Methods import geocodeAddress
from django.contrib import messages

regions = []
coord_points = []
def index(request):
    return HttpResponse("Hello, world. You're at the analysis index.")

def geocode_view(request):
    if request.method == "POST":
        form = geocodeForm(request.POST)
        if form.is_valid():
            country = form.cleaned_data['country_data']
            region = form.cleaned_data['region_data']
            point = geocodeAddress(region,country)

            if point is None:
                messages.error(request, "Country and Region invalid, please try again")
                return HttpResponseRedirect(request.path_info)

            regions.append(country + ", " + region)
            coord_points.append(point)
            if form.cleaned_data['add_more']:
                return HttpResponseRedirect(request.path_info)

            return HttpResponseRedirect('/analysis/export')

    context = {'form': geocodeForm(), 'regions':regions}
    return render(request, "geocode.html", context)





def export_view(request):
    if request.method == "POST":
        form = exportForm(request.POST)
        if form.is_valid():
            attributes = str(form.cleaned_data['attributes_data'])
            year = str(form.cleaned_data['year_data'])
            leap_year = str(form.cleaned_data['leapYear_data'])
            interval = str(form.cleaned_data['interval_data'])
            utc = str(form.cleaned_data['utc_data'])
            name = str(form.cleaned_data['name_data'])
            reason = str(form.cleaned_data['reason_data'])
            affiliation = str(form.cleaned_data['affiliation_data'])
            email = str(form.cleaned_data['email_data'])
            # Use this alongside the coordinates and submit all of this to NREL Method
            #http redirection happens here
            return HttpResponse("Selection: Attributes: " + attributes + "\n\n"+
                                "Year: " + year + "\n\n" + "Leap Year Included: " + leap_year + "\n\n" +
                                "Interval: " + interval + "\n\n" + "UTC: " + utc + "\n\n" +
                                "Name: " + name + "\n\n" + "Reason: " + reason + "\n\n" +
                                "Affiliation: " + affiliation + "\n\n" + "Email: " + email)

    context = {'form': exportForm()}
    return render(request, "export.html", context)

def attribute_filter_view(request):
    if request.method == "POST":
        form = attributeFilterForm(request.POST)
        if form.is_valid():
            attributes = str(form.cleaned_data['attributes_data'])
            return HttpResponse("Attributes selected: " + attributes)

    context = {'form': attributeFilterForm()}
    return render(request, "attribute_filter.html", context)