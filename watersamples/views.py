from django.conf import settings
from django.shortcuts import render, render_to_response
from chartit import DataPool, Chart
from watersamples.forms import ChartForm
from watersamples.models import WaterIntakePoint, WaterIntakeInfo
from watersamples.utils import STATUS_CHECKED


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


def chart(request):
    form = ChartForm(request.GET or {})

    if request.GET and form.is_valid():

        info_fields = form.cleaned_data.get('info_fields')
        query = WaterIntakeInfo.objects.filter(
            intake_point_id=form.cleaned_data.get('intake_point'),
            date_taken__gte=form.cleaned_data.get('date_from'),
            status=STATUS_CHECKED
        )
    else:
        query = WaterIntakeInfo.objects
        info_fields = ['classification']

    weatherdata = \
        DataPool(
            series=[{
                'options': {
                    'source': query
                },
                'terms': [
                    'date_taken',
                    'classification',
                    'smell_20_celsium',
                    'smell_60_celsium',
                    'aftertaste',
                    'color',
                    'dry_residue',
                    'pH',
                    'rigidity',
                    'nitrates',
                    'chlorides',
                    'sulphates',
                    'iron_overall',
                    'manganese',
                    'fluorine',
                ]}
            ])

    cht = Chart(
        datasource=weatherdata,
        series_options=[{
            'options': {
                'type': 'line',
                'stacking': False
            },
            'terms': {
                'date_taken': info_fields,
            }
        }],
        chart_options={
            'title': {
                'text': 'Charts for intake points'
            },
            'xAxis': {
                'title': {
                    'text': 'Date'
                }
            },
            'yAxis': {
                'title': {
                    'text': 'Fields'
                }
            }
        })
    return render_to_response('line_chart.html', {'weatherchart': cht, 'form': form})
