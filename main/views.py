from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Workshops ,Subscribe
from .serializer import SubscribeSerializer, WorkshopsListSerializer, WorkshopSerializer
import requests, json
from django.db.models import Q

## testing
def about(request):
    render (request, 'main/index.html')

## index page
def index(request):
    workshops = Workshops.objects.all()
    return render(request, 'main/index.html', {'workshops': workshops})

## testing
def testpostrequest(request):
    #r = requests.post('http://127.0.0.1:8000/api/subscribe/', data={'email':'admin12@mysite.com'})
    querystring = {'name': 'aerv', 'zone_id': '1'}
    r = requests.get('http://127.0.0.1:8000/api/workshops/', params=querystring)
    #r = requests.put('http://127.0.0.1:8000/api/subscribe/', data = {'email':'admin19@mysite.com', 'active': '1'})
    return render(request, 'main/test.html', {'respond': r})

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
        workshop_name = request.GET.get('name')
        specializtion_id = request.GET.get('specializtion_id')
        craft_id = request.GET.get('craft_id')
        car_id = request.GET.get('car_id')
        governorate_id = request.GET.get('governorate_id')
        zone_id = request.GET.get('zone_id')
        orderedBy = request.GET.get('orderedBy')

        query = Q(is_visible = True)
        if workshop_name is not None:
            query &= Q(name__contains = workshop_name )
        if specializtion_id is not None:
            query &= Q(specializtions = specializtion_id )
        if craft_id is not None:
            query &= Q(crafts = craft_id )
        if car_id is not None:
            query &= Q(cars = car_id )
        if governorate_id is not None:
            query &= Q(governorate = governorate_id )
        if zone_id is not None:
            query &= Q(zone = zone_id )

        # ordering by    
        #if orderedBy is not None:
            #query &= Q(orderedBy = zone_id )

        workshops = Workshops.objects.filter(query).order_by('-id')
        serializer = WorkshopsListSerializer(workshops, many=True)
        return Response(serializer.data)


class WorkshopDetails(APIView):
    
    def get(self, request):
        workshop_id = request.GET.get('workshop_id')        
        workshop = Workshops.objects.filter(pk=workshop_id)
        serializer = WorkshopSerializer(workshop, many=True)
        return Response(serializer.data)
        

