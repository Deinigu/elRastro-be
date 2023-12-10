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
    if request.method == 'POST' and request.FILES.getlist('images'):
        uploaded_files = request.FILES.getlist('images')
        uploaded_urls = []

        # Upload each image to Cloudinary
        cloudinary.config(
                cloud_name="dx4oicqhy",
                api_key="765172224316842",
                api_secret="ojkOD6jTPcuYjU5Z_77do1AI-VY"
            )

        for file in uploaded_files:
            upload_result = cloudinary.uploader.upload(
                file,
                folder='elRastro_cloudinary_folder'
            )
            uploaded_urls.append(upload_result['secure_url'])
        return JsonResponse({'urls': uploaded_urls})
    return HttpResponse(status=400)

