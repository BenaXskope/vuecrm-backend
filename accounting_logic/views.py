from django.shortcuts import render
from django.db.models import Count
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
import rest_framework
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from accounting_logic.serializer import CategorySerializer, RecordSerializer
from user_app.serializers import AuthTokenSerializer, ProfileSerializer
from rest_framework import parsers, renderers
import json
import datetime

from user_app.authentication import MyTokenAuthentication
from django.contrib.auth.models import User
from user_app.models import Profile, Token, Value, BrowserData
from django.contrib.auth import logout
from django.contrib.contenttypes.models import ContentType
from accounting_logic.query import *
from accounting_logic.models import Record, Category
# Create your views here.
# Create your views here.


@api_view(['GET'])
@authentication_classes((MyTokenAuthentication, SessionAuthentication))
@permission_classes((IsAuthenticated, ))
def api_get_categories(request):
    categories = get_categories(request.user)
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


@api_view(['PATCH'])
@authentication_classes((MyTokenAuthentication, SessionAuthentication))
@permission_classes((IsAuthenticated, ))
def api_get_category_by_id(request):
    print(request.data)
    category = get_category_by_id(request.user, request.data)
    serializer = CategorySerializer(category)
    return Response(serializer.data)


@api_view(['POST'])
@authentication_classes((MyTokenAuthentication, SessionAuthentication))
@permission_classes((IsAuthenticated, ))
def api_create_category(request):
    category = create_category(request.user, request.data)
    return Response(CategorySerializer(category).data)


@api_view(['PATCH'])
@authentication_classes((MyTokenAuthentication, SessionAuthentication))
@permission_classes((IsAuthenticated, ))
def api_edit_category(request):
    category = edit_category(request.user, request.data)
    return Response(CategorySerializer(category).data)


@api_view(['GET'])
@authentication_classes((MyTokenAuthentication, SessionAuthentication))
@permission_classes((IsAuthenticated, ))
def api_get_all_records(request):
    records = get_all_records(request.user)
    serializer = RecordSerializer(records, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@authentication_classes((MyTokenAuthentication, SessionAuthentication))
@permission_classes((IsAuthenticated, ))
def api_create_record(request):
    print(request.data)
    record = create_record(request.user, request.data)
    return Response(RecordSerializer(record).data)


@api_view(['PATCH'])
@authentication_classes((MyTokenAuthentication, SessionAuthentication))
@permission_classes((IsAuthenticated, ))
def api_get_record_by_id(request):
    print(request.data)
    record = get_record_by_id(request.user, request.data)
    return Response(RecordSerializer(record).data)


@api_view(['GET'])
@authentication_classes((MyTokenAuthentication, SessionAuthentication))
@permission_classes((IsAuthenticated, ))
def api_get_category_records(response):
    print(response.GET)
    return Response({'test': 'OK'})
