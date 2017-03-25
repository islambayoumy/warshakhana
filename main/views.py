from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Workshops ,Subscribe
from .serializer import SubscribeSerializer
import requests

def index(request):
    workshops = Workshops.objects.all()
    return render(request, 'main/index.html', {'workshops': workshops})

def testpostrequest(request):
    #r = requests.post('http://127.0.0.1:8000/api/subscribe/', data = {'email':'aef@daf.dasf'})
    #r = requests.get('http://127.0.0.1:8000/api/subscribe/')
    pass

class SubscribeList(APIView):
    
    def get(self, request):
        subscribe = Subscribe.objects.all()
        serializer = SubscribeSerializer(subscribe, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SubscribeList(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request):
        # update
        pass

