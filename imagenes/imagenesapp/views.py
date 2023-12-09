# Django views.py
import cloudinary
import cloudinary.uploader
from django.http import HttpResponse
import requests
import json

from datetime import datetime
from dateutil import parser

from bson import ObjectId
from rest_framework.response import Response

from django.http.response import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework import status

@api_view(['POST'])
def upload_image(request):
    if request.method == 'POST' and request.FILES['image']:
        uploaded_file = request.FILES['image']

        # Upload to Cloudinary
        cloudinary.config(
                cloud_name="dx4oicqhy",
                api_key="765172224316842",
                api_secret="ojkOD6jTPcuYjU5Z_77do1AI-VY"
            )
        upload_result = cloudinary.uploader.upload(uploaded_file)

            # Store Cloudinary URL in MongoDB
            # (Implement your MongoDB logic here)

        return JsonResponse({'url': upload_result['secure_url']})
    return HttpResponse(status=400)

