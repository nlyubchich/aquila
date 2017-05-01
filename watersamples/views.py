from django.conf import settings
from django.shortcuts import render

from watersamples.models import WaterIntakePoint


def maps(request):
    points = WaterIntakePoint.objects.all()
    markers = [{
        'lat': point.geolocation.lat,
        'lon': point.geolocation.lon,
        'name': point.name,
    } for point in points]
    center_lat = request.GET.get('lat')
    center_lon = request.GET.get('lon')
    return render(request, 'map.html', {
        'markers': markers,
        'center_lat': center_lat or 50.45,
        'center_lon': center_lon or 30.52,
        'gmaps_key': settings.GOOGLE_MAPS_API_KEY
    })
