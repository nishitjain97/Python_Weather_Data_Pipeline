from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
from django.http import HttpResponse
from django.core.paginator import Paginator

from .models import Weather, Stats, Crops

def getWeather(request):
    # Return weather JSON
    date_filter = request.GET.get("date", -1)
    station_filter = request.GET.get("station_id", -1)

    # Filter data
    if date_filter == -1 and station_filter == -1:
        model = Weather.objects.all()
    elif date_filter == -1:
        model = Weather.objects.filter(Station_id = station_filter)
    elif station_filter == -1:
        model = Weather.objects.filter(Date = date_filter)
    else:
        model = Weather.objects.filter(Date = date_filter).filter(Station_id = station_filter)
        
    page_number = request.GET.get("page", 1)
    paginator = Paginator(model, 10)
    page_obj = paginator.get_page(page_number)
    output_json = serializers.serialize('json', page_obj.object_list)

    # print(output_json)
    payload = {
	    'page': {
	    'current': page_obj.number,
	    'has_next': page_obj.has_next(),
	    'has_previous': page_obj.has_previous()
        },
        'data': output_json
    }
    return JsonResponse(payload)

def getStats(request):
    # Return stats json
    date_filter = request.GET.get("year", -1)
    station_filter = request.GET.get("station_id", -1)

    # Filter data
    if date_filter == -1 and station_filter == -1:
        model = Stats.objects.all()
    elif date_filter == -1:
        model = Stats.objects.filter(Station_id = station_filter)
    elif station_filter == -1:
        model = Stats.objects.filter(Year = date_filter)
    else:
        model = Stats.objects.filter(Year = date_filter).filter(Station_id = station_filter)
        
	
    page_number = request.GET.get("page", 1)
    paginator = Paginator(model, 10)
    page_obj = paginator.get_page(page_number)
    output_json = serializers.serialize('json', page_obj.object_list)

    # print(output_json)
    payload = {
	    'page': {
	    'current': page_obj.number,
	    'has_next': page_obj.has_next(),
	    'has_previous': page_obj.has_previous()
        },
        'data': output_json
    }
    return JsonResponse(payload)

def getCrops(request):
    # Return crops JSON
    date_filter = request.GET.get("date", -1)

    if date_filter == -1:
        # Get all data
        model = Crops.objects.all()
    else:
        # Get filtered data
        model = Crops.objects.filter(Date = date_filter)
        
	
    page_number = request.GET.get("page", 1)
    paginator = Paginator(model, 10)
    page_obj = paginator.get_page(page_number)
    output_json = serializers.serialize('json', page_obj.object_list)

    # print(output_json)
    payload = {
	    'page': {
	    'current': page_obj.number,
	    'has_next': page_obj.has_next(),
	    'has_previous': page_obj.has_previous()
        },
        'data': output_json
    }
    return JsonResponse(payload)