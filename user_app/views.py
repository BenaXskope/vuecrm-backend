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

from user_app.serializers import AuthTokenSerializer, ProfileSerializer
from rest_framework import parsers, renderers
import json
import datetime

from user_app.authentication import MyTokenAuthentication
from django.contrib.auth.models import User
from user_app.models import Profile, Token, Value, BrowserData
from django.contrib.auth import logout
from django.contrib.contenttypes.models import ContentType
from user_app.query import *
# Create your views here.


def get_browser_data(request):
    browser_data = {
        'HTTP_USER_AGENT': request.META.get('HTTP_USER_AGENT'),
        'HTTP_ACCEPT': request.META.get('HTTP_ACCEPT'),
        'HTTP_ACCEPT_LANGUAGE': request.META.get('HTTP_ACCEPT_LANGUAGE'),
        'HTTP_ACCEPT_ENCODING': request.META.get('HTTP_ACCEPT_ENCODING'),
        'HTTP_X_FORWARDED_FOR': request.META.get('HTTP_X_FORWARDED_FOR'),
        'REMOTE_ADDR': request.META.get('REMOTE_ADDR'),
        'guid': request.data.get('guid'),
        'luid': request.data.get('luid'),
    }
    entities = list(Value.objects.filter(value__in=set([x for x in browser_data.values() if x])))
    pairs = dict(
        HTTP_USER_AGENT='user_agent_val',
        HTTP_ACCEPT='http_accept_val',
        HTTP_ACCEPT_LANGUAGE='accept_lang_val',
        HTTP_ACCEPT_ENCODING='accept_encoding_val',
        HTTP_X_FORWARDED_FOR='x_forwarded_val',
        REMOTE_ADDR='remote_addr_val',
        guid='guid_val',
        luid='luid_val',
    )
    new_br_data = dict()
    for k, v in browser_data.items():
        if v:
            has_value = False
            # print(len(entities))
            for item in entities:
                if item.value == v:
                    new_br_data.update({ pairs[k]: item })
                    has_value = True
                    break
            if not has_value:
                val, created = Value.objects.get_or_create(value=v)
                new_br_data.update({ pairs[k]: val })
                entities.append(val)
        else:
            new_br_data.update({ pairs[k]: None })

    return BrowserData.objects.create(**new_br_data)


class MyObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        token = Token.objects.create(user=user)

        return Response({
            'token': token.key,
            'user': {
                'username': user.username,
                'name': user.profile.name,
                'bill': user.profile.bill,
            },
        })


@api_view(['GET'])
@authentication_classes((MyTokenAuthentication, ))
#@permission_classes((IsAuthenticated, ))
def api_logout(request):
    t_obj = MyTokenAuthentication()
    try:
        t_user, token = t_obj.authenticate(request)
        token.is_active = False
        token.save()
        print('YPA')
    except:
        # save_log("api_logout", "logout get token error")
        print("api logout get token error")
    logout(request)
    return Response({'detail': "Ok"})


@api_view(['GET'])
@authentication_classes((MyTokenAuthentication, SessionAuthentication))
@permission_classes((IsAuthenticated, ))
def api_check_auth(request):
    user = request.user
    return Response({
        'user': user.username
    })


@api_view(['GET'])
@authentication_classes((MyTokenAuthentication, SessionAuthentication))
@permission_classes((IsAuthenticated, ))
def api_my_profile(request):
    serializer = ProfileSerializer(request.user.profile)
    return Response({'profile': serializer.data})


@api_view(['POST'])
@authentication_classes((MyTokenAuthentication, SessionAuthentication))
def api_register(request):
    resp = create_user(request.data)
    return Response(resp)


@api_view(['PATCH'])
@authentication_classes((MyTokenAuthentication, SessionAuthentication))
@permission_classes((IsAuthenticated, ))
def api_update_profile(request):
    update_profile(request.user, request.data)
    return Response({'user': 'test'})
