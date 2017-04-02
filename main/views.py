from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Workshops ,Subscribe, Cars, Specializations, Crafts, Governorates, Zones
from .serializer import SubscribeSerializer, WorkshopsListSerializer, WorkshopSerializer, CarsSerializer, SpecializationsSerializer, CraftsSerializer, GovernoratesSerializer, ZonesSerializer
import requests, json
from django.db.models import Q
from django.http import HttpResponse ##


## index page
def index(request):
    return render(request, 'main/index.html')

## testing
def display_meta(request):
    values = request.META.items()
    html = []
    for k, v in values:
        html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
    return HttpResponse('<table>%s</table>' % '\n'.join(html))

def testpostrequest(request):
    #r = requests.post('http://127.0.0.1:8000/api/subscribe/', data={'email':'admin12@mysite.com'})
    querystring = {'name': 'aerv', 'zone_id': '1'}
    r = requests.get('http://127.0.0.1:8000/api/workshops/', params=querystring)
    #r = requests.put('http://127.0.0.1:8000/api/subscribe/', data = {'email':'admin19@mysite.com', 'active': '1'})
    return render(request, 'main/test.html', {'respond': r})

def search(request):
    return render(request, 'main/search_box.html')

## end testing

def submit_search(request):
    selections = requests.get('http://127.0.0.1:8000/api/selections/')
    json_selections = selections.json()

    workshop_name = request.GET.get('workshop_name')
    specializtion_id = request.GET.get('specializtion_id')
    craft_id = request.GET.get('craft_id')
    car_id = request.GET.get('car_id')
    governorate_id = request.GET.get('governorate_id')
    zone_id = request.GET.get('zone_id')
    ordered_by = request.GET.get('ordered_by')

    querystring = {
        'workshop_name': workshop_name,
        'specializtion_id': specializtion_id,
        'craft_id': craft_id,
        'car_id': car_id,
        'governorate_id': governorate_id,
        'zone_id': zone_id,
        'ordered_by': ordered_by,        
        }
    if any(querystring.values()):
        r = requests.get('http://127.0.0.1:8000/api/workshops/', params=querystring)

        if r.status_code == 200:
            json_response = r.json()
            return render(request, 'main/index.html', {'selections': json_selections, 'workshops': json_response})
        else:
            return render(request, 'main/index.html', {'error': {'message': 'request fails', 'code': r.status_code}})
    return render(request, 'main/index.html', {'selections': json_selections})

def workshop(request, workshop_id):
    querystring = {'workshop_id': workshop_id}
    r = requests.get('http://127.0.0.1:8000/api/workshop/', params=querystring)
    json_response = r.json()
    
    return render(request, 'main/workshop.html', {'Respond': json_response})


class SubscribeList(APIView):
    
    def get(self, request):
        subscribe = Subscribe.objects.all()
        serializer = SubscribeSerializer(subscribe, many=True)
        return Response(serializer.data)

    def post(self, request):
        email = request.POST.get('email', '')
        test = Subscribe.objects.filter(email=email)
        if test:
            return Response('already exists')
        else:
            try:
                subscribe_obj = Subscribe(email=email)
                subscribe_obj.save()
                return Response('add successfully', status=status.HTTP_201_CREATED)
            except:
                return Response('subscription error')

    def put(self, request):
        active = request.POST.get('active', '')
        email = request.POST.get('email', '')
        email_obj = Subscribe.objects.filter(email=email)
        if not email_obj:
            return Response('no such email')
        else:
            if (active == '0'):   
                try:
                    email_obj.update(is_active=False)
                    return Response('unsubscribed successfully', status=status.HTTP_201_CREATED)
                except:
                    return Response('unsubscription error')
            elif (active == '1'):
                try:
                    email_obj.update(is_active=True)
                    return Response('subscribed successfully', status=status.HTTP_201_CREATED)
                except:
                    return Response('subscription error')


class WorkshopsList(APIView):

    def get(self, request):
        workshop_name = request.GET.get('workshop_name')
        specializtion_id = request.GET.get('specializtion_id')
        craft_id = request.GET.get('craft_id')
        car_id = request.GET.get('car_id')
        governorate_id = request.GET.get('governorate_id')
        zone_id = request.GET.get('zone_id')
        ordered_by = request.GET.get('ordered_by')

        query = Q(is_visible = True)
        if workshop_name != '':
            query &= Q(name__icontains = workshop_name)
        if specializtion_id != '0':
            query &= Q(specializations = specializtion_id)
        if craft_id != '0':
            query &= Q(crafts = craft_id)
        if car_id != '0':
            query &= Q(cars = car_id)
        if governorate_id != '0':
            query &= Q(governorate = governorate_id)
        if zone_id != '0':
            query &= Q(zone = zone_id)

        # ordering by    
        if ordered_by == 'newest':
            order = '-id'
        elif ordered_by == 'rank':
            order = 'name'              #####
        elif ordered_by == 'views':
            order = 'owner'             #####
        else:
            order = '-id'

        workshops = Workshops.objects.filter(query).order_by(order)
        serializer = WorkshopsListSerializer(workshops, many=True)
        return Response(serializer.data)


class WorkshopDetails(APIView):
    
    def get(self, request):
        workshop_id = request.GET.get('workshop_id')        
        workshop = Workshops.objects.filter(pk=workshop_id)
        serializer = WorkshopSerializer(workshop, many=True)
        return Response(serializer.data)
        

class Selections(APIView):
    
    def get(self, request):
        
        cars = Cars.objects.all()
        c_serializer = CarsSerializer(cars, many=True)

        specializations = Specializations.objects.all()
        s_serializer = SpecializationsSerializer(specializations, many=True)

        crafts = Crafts.objects.all()
        cr_serializer = CraftsSerializer(crafts, many=True)

        governorates = Governorates.objects.all()
        g_serializer = GovernoratesSerializer(governorates, many=True)

        zones = Zones.objects.all()
        z_serializer = ZonesSerializer(zones, many=True)
        
        data = {
            'cars': c_serializer.data,
            'specializations': s_serializer.data,
            'crafts': cr_serializer.data,
            'governorates': g_serializer.data,
            'zones': z_serializer.data,
        }

        return Response(data)

        

