from django.shortcuts import render
from .models import Workshops

def index(request):
    workshops = Workshops.objects.all()
    return render(request, 'main/index.html', {'workshops': workshops})
