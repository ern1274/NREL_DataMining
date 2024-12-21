from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .forms import geocodeForm, exportForm, attributeFilterForm, forms_attributes_string
from NREL_DataMining.src.NREL_Methods import geocodeAddress, exportToDF_api
from NREL_DataMining.src.Data_Preprocess import organize_dfs
from django.contrib import messages
import pandas as pd

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

def export_view(request):
    if 'regions' not in request.session or not len(request.session.get('regions')) >= 1:
        messages.error(request, "Add at least 1 country and region")
        return HttpResponseRedirect('/analysis/geocode')

    if request.method == "POST":
        form = exportForm(request.POST)
        if form.is_valid():
            attributes = str(form.cleaned_data['attributes_data'])
            if form.cleaned_data['all_attributes_data']:
                attributes = str(forms_attributes_string)
            request.session['attributes'] = attributes

            year = str(form.cleaned_data['year_data'])
            request.session['year'] = year

            leap_year = str(form.cleaned_data['leapYear_data'])
            request.session['leap_year'] = leap_year

            interval = str(form.cleaned_data['interval_data'])
            request.session['interval'] = interval

            utc = str(form.cleaned_data['utc_data'])
            request.session['utc'] = utc

            name = str(form.cleaned_data['name_data'])
            request.session['name'] = name

            reason = str(form.cleaned_data['reason_data'])
            request.session['reason'] = reason

            affiliation = str(form.cleaned_data['affiliation_data'])
            request.session['affiliation'] = affiliation

            email = str(form.cleaned_data['email_data'])
            request.session['email'] = email

            info = {'attributes':attributes,
                    'regions': request.session['regions'],
                    'points': request.session['region_points'],
                    'year':year,
                    'leap_year':leap_year,
                    'interval': interval,
                    'utc':utc,
                    'name':name,
                    'reason':reason,
                    'affiliation':affiliation,
                    'email':email}
            export_df = exportToDF_api(info)
            # export_df is dict[country][region]=dict-like dataframe, values should be passed back into pandas dataframe for ease of viewing
            request.session['export_df'] = export_df
            export_df_string = ""

            for country in export_df.keys():
                for region in export_df[country].keys():
                    test_df = pd.DataFrame.from_dict(data=request.session['export_df'][country][region], orient='columns')

                    export_df_string += country + ", " + region + "\n"
                    export_df_string += test_df.to_string()
                export_df_string += "\n\n"
            # For display purposes
            request.session['export_df_string'] = export_df_string
            # Maybe redirect to attribute filter form and display form first
            # somehow display the data in a concise way
            return HttpResponse(str(export_df_string),content_type="text/plain")
            #return HttpResponse("Selection: Attributes: " + attributes + "\n\n"+
            #                    "Year: " + year + "\n\n" + "Leap Year Included: " + leap_year + "\n\n" +
            #                    "Interval: " + interval + "\n\n" + "UTC: " + utc + "\n\n" +
            #                    "Name: " + name + "\n\n" + "Reason: " + reason + "\n\n" +
            #                    "Affiliation: " + affiliation + "\n\n" + "Email: " + email)
        else:
            for error in form.errors:
                messages.error(request, form.errors[error])
    context = {'export_form': exportForm(),
               'regions': request.session.get('regions')}
    return render(request, "export.html", context)

def attribute_filter_view(request):
    if not len(request.session.get('regions')) >= 1:
        messages.error(request, "Add a region first")
        return HttpResponseRedirect('/analysis/geocode')

    if 'export_df' not in request.session:
        messages.error(request, "Fill out export form first")
        return HttpResponseRedirect('/analysis/export')

    if 'order_filt_attribs' not in request.session:
        reset_filter_attributes(request)

    if request.method == "POST":
        form = attributeFilterForm(request.POST)
        if form.is_valid():
            attribute = form.cleaned_data['attribute_data']
            if attribute in request.session.get('order_filt_attribs'):
                messages.error(request, "Already selected this attribute")
            elif attribute != '':
                arr = request.session.get('order_filt_attribs')
                arr.append(attribute)
                request.session['order_filt_attribs'] = arr
            return HttpResponseRedirect(request.path_info)

    context = {'form': attributeFilterForm(),
               'attributes': request.session.get('order_filt_attribs')}

    return render(request, "attribute_filter.html", context)

def reset_filter_attributes(request):
    request.session['order_filt_attribs'] = []
    return HttpResponseRedirect('/analysis/attribute_filter')

def delete_filter_attribute(request):
    form = attributeFilterForm(request.POST)
    if form.is_valid():
        attribute_to_delete = form.cleaned_data['attribute_data']
        if attribute_to_delete in request.session['order_filt_attribs']:
            arr = request.session['order_filt_attribs']
            arr.remove(attribute_to_delete)
            request.session['order_filt_attribs'] = arr
        else:
            messages.error(request, "Attribute hasn't been selected")
    return HttpResponseRedirect('/analysis/attribute_filter')


def recurse_organized_string(attributes, data, ind):
    string = ""
    if len(attributes) == ind:
        return str(data)

    string += "\n"
    string += "\t"*ind
    string += attributes[ind] + "\n"

    for assignment in data.keys():
        string += "\n\n"
        string += "\t"*ind
        string += str(assignment) + "\n"

        string += "\n"
        string += "\t" * ind
        string += recurse_organized_string(attributes,data[assignment],ind+1)
    return string

def sorted_results_view(request):
    # Don't need regions at this point
    #if not len(request.session.get('regions')) >= 1:
    #    messages.error(request, "Add a region first")
    if 'export_df' not in request.session:
        messages.error(request, "Fill out export form first")
        return HttpResponseRedirect('/analysis/export')
    if 'order_filt_attribs' not in request.session:
        messages.error(request, "Add attributes to filter the data by (NOT REQUIRED)")
        return HttpResponseRedirect('/analysis/attribute_filter')
    organized_df = organize_dfs(request.session.get('export_df'), request.session.get('order_filt_attribs'))
    organized_df_string = ""

    for country in organized_df.keys():
        organized_df_string += "\n\n" + country + "\n"
        if country == 'ALL':
            organized_df_string += recurse_organized_string(request.session.get('order_filt_attribs'), organized_df[country], 0)
            continue
        for region in organized_df[country].keys():
            organized_df_string += "\n" + region + "\n"
            organized_df_string += recurse_organized_string(request.session.get('order_filt_attribs'), organized_df[country][region], 0)
        organized_df_string += "\n\n"
    # NEXT STEP: SET UP HTML FILE TO PROPERLY DISPLAY ORGANIZED_DF
    # request.session['organized_df_string'] = organized_df_string
    # request.session['organized_df'] = organized_df
    return HttpResponse(organized_df_string,content_type="text/plain")
