from django.http import HttpResponse
from django.shortcuts import render
from .forms import geocodeForm, exportForm, attributeFilterForm


def index(request):
    return HttpResponse("Hello, world. You're at the analysis index.")

def geocode_view(request):
    if request.method == "POST":
        form = geocodeForm(request.POST)
        if form.is_valid():
            country = form.cleaned_data['country_data']
            region = form.cleaned_data['region_data']

            #http redirection happens here
            return HttpResponse("Looking at " + country + " : " + region)

    context = {'form': geocodeForm()}
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

            #http redirection happens here
            return HttpResponse("Selection: Attributes: " + attributes + "\n\n"+
                                "Year: " + year + "\n\n" + "Leap Year Included: " + leap_year + "\n\n" +
                                "Interval: " + interval + "\n\n" + "UTC: " + utc + "\n\n" +
                                "Name: " + name + "\n\n" + "Reason: " + reason + "\n\n" +
                                "Affiliation: " + affiliation + "\n\n" + "Email: " + email)

    context = {'form': exportForm()}
    return render(request, "export.html", context)

def attribute_filter_view(request):
    context = {'form': attributeFilterForm()}
    return render(request, "attribute_filter.html", context)