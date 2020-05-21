from django.shortcuts import render
from .models import Deputy

from .serializers import DeputySerializer
from rest_framework import generics
                         
# Create your views here.
class DeputyList(generics.ListCreateAPIView):
    queryset = Deputy.objects.all()
    serializer_class = DeputySerializer

class DeputyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Deputy.objects.all()
    serializer_class = DeputySerializer