from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .forms import geocodeForm, exportForm, attributeFilterForm
from NREL_DataMining.src.NREL_Methods import geocodeAddress
from django.contrib import messages

#regions = []
#coord_points = []
# USE SESSION MIDDLEWARE TO STORE POINTS ABOVE
# LEARN HOW TO ACCESS SESSION MIDDLEWARE IN VIEWS AND HTML
def index(request):
    return HttpResponse("Hello, world. You're at the analysis index.")


# AFTER STORING POINTS IN SESSION MIDDLEWARE
# LEARN HOW TO DELETE INDIVIDUAL POINTS AND/OR CLEAR ALL POINTS
def geocode_view(request):
    if 'regions' not in request.session:
        reset_region_and_points(request)

    if request.method == "POST":
        form = geocodeForm(request.POST)
        if form.is_valid():
            country = form.cleaned_data['country_data']
            region = form.cleaned_data['region_data']
            point = geocodeAddress(region,country)

            # If country and region are not real or not available, then point is None
            if point is None:
                messages.error(request, "Country and Region invalid, please try again")
                return HttpResponseRedirect(request.path_info)

            country_region = country + ", " + region
            # If country and region are already selected, form is invalid
            if country_region in request.session.get('regions'):
                messages.error(request, "Already have this Country and Region, please try again")
                return HttpResponseRedirect(request.path_info)

            region_arr = request.session['regions']
            region_arr.append(country_region)
            request.session['regions'] = region_arr

            point_arr = request.session['region_points']
            point_arr.append(point)
            request.session['region_points'] = point_arr


            return HttpResponseRedirect(request.path_info)

    context = {'geo_form': geocodeForm(),
               'regions': request.session.get('regions')}
    return render(request, "geocode.html", context)


def reset_region_and_points(request):
    request.session['regions'] = []
    request.session['region_points'] = []
    return HttpResponseRedirect('/analysis/geocode')

def preverify_export(request):
    # Verify there is at least one region
    if len(request.session.get('regions')) >= 1:
        return HttpResponseRedirect('/analysis/export')
    messages.error(request, "Add at least 1 country and region")
    return HttpResponseRedirect('/analysis/geocode')


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