from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Workshops ,Subscribe
from .serializer import SubscribeSerializer
import requests, json

def index(request):
    workshops = Workshops.objects.all()
    return render(request, 'main/index.html', {'workshops': workshops})

def testpostrequest(request):
    r = requests.post('http://127.0.0.1:8000/api/subscribe/', data={'email':'admin12@mysite.com'})
    #r = requests.get('http://127.0.0.1:8000/api/subscribe/')
    #r = requests.put('http://127.0.0.1:8000/api/subscribe/', data = {'email':'admin19@mysite.com', 'active': '1'})
    return render(request, 'main/test.html', {'respond': r})

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
