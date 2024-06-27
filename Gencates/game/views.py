from rest_framework import viewsets
from .models import Cat, UserProfile, Incubator, Storage, Crossbreeder, IncomeRoom, HibernationRoom, CatyCoin
from .serializers import CatSerializer, UserProfileSerializer, IncubatorSerializer, StorageSerializer, \
    CrossbreederSerializer, IncomeRoomSerializer, HibernationRoomSerializer, CatyCoinSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
import requests

TELEGRAM_BOT_TOKEN = settings.TELEGRAM_TOKEN
GAME_SHORT_NAME = 'Gencates'
GAME_URL = 'https://takumishiawase.github.io/genecats/'


class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class IncubatorViewSet(viewsets.ModelViewSet):
    queryset = Incubator.objects.all()
    serializer_class = IncubatorSerializer

    @action(detail=True, methods=['post'])
    def spawn_cat(self, request, pk=None):
        incubator = self.get_object()
        incubator.spawn_cat()
        return Response({'status': 'cat spawned'})


class StorageViewSet(viewsets.ModelViewSet):
    queryset = Storage.objects.all()
    serializer_class = StorageSerializer


class CrossbreederViewSet(viewsets.ModelViewSet):
    queryset = Crossbreeder.objects.all()
    serializer_class = CrossbreederSerializer

    @action(detail=True, methods=['post'])
    def breed_cats(self, request, pk=None):
        crossbreeder = self.get_object()
        crossbreeder.breed_cats()
        return Response({'status': 'cats bred'})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'game/login.html', {'form': form})


class IncomeRoomViewSet(viewsets.ModelViewSet):
    queryset = IncomeRoom.objects.all()
    serializer_class = IncomeRoomSerializer

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        room = self.get_object()
        room.is_active = True
        room.save()
        return Response({'status': 'room activated'})

    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        room = self.get_object()
        room.is_active = False
        room.save()
        return Response({'status': 'room deactivated'})


class HibernationRoomViewSet(viewsets.ModelViewSet):
    queryset = HibernationRoom.objects.all()
    serializer_class = HibernationRoomSerializer

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        room = self.get_object()
        room.is_active = True
        room.save()
        return Response({'status': 'room activated'})

    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        room = self.get_object()
        room.is_active = False
        room.save()
        return Response({'status': 'room deactivated'})


class CatyCoinViewSet(viewsets.ModelViewSet):
    queryset = CatyCoin.objects.all()
    serializer_class = CatyCoinSerializer

    @action(detail=True, methods=['post'])
    def add_coins(self, request, pk=None):
        coin = self.get_object()
        amount = request.data.get('amount', 0)
        coin.balance += int(amount)
        coin.save()
        return Response({'status': 'coins added', 'new_balance': coin.balance})

    @action(detail=True, methods=['post'])
    def subtract_coins(self, request, pk=None):
        coin = self.get_object()
        amount = request.data.get('amount', 0)
        coin.balance -= int(amount)
        coin.save()
        return Response({'status': 'coins subtracted', 'new_balance': coin.balance})


@api_view(['GET'])
def get_referral_link(request):
    user = request.user
    if not user.is_authenticated:
        return Response({'error': 'User not authenticated'}, status=400)

    referral_link = f"http://127.0.0.1:3000/register?ref={user.userprofile.referral_code}"
    return Response({'referral_link': referral_link})


@api_view(['POST'])
def register_with_referral(request):
    referral_code = request.data.get('referral_code')
    user = request.user
    if not user.is_authenticated or not referral_code:
        return Response({'error': 'Invalid request'}, status=400)

    referrer = get_object_or_404(UserProfile, referral_code=referral_code)
    user.userprofile.referred_by = referrer
    user.userprofile.save()

    # Example of adding bonus coins
    referrer.coins += 100
    referrer.save()
    user.userprofile.coins += 50
    user.userprofile.save()

    return Response({'status': 'User registered with referral'})


@csrf_exempt
def telegram_webhook(request):
    if request.method == 'POST':
        try:
            update = json.loads(request.body)
            print(f"Update received: {update}")  # Логирование обновлений
            if 'message' in update:
                chat_id = update['message']['chat']['id']
                text = update['message']['text']
                handle_message(chat_id, text)
            return JsonResponse({'status': 'ok'})
        except Exception as e:
            print(f"Error handling webhook: {e}")
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'not allowed'})

def handle_message(chat_id, text):
    print(f"Handling message: {text} from chat_id: {chat_id}")  # Логирование сообщений
    if text == '/start':
        send_message(chat_id, 'Welcome to the game! Click /play to start.')
    elif text == '/play':
        start_game(chat_id)

def send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    payload = {'chat_id': chat_id, 'text': text}
    requests.post(url, json=payload)

def start_game(chat_id):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendGame'
    payload = {'chat_id': chat_id, 'game_short_name': GAME_SHORT_NAME}
    response = requests.post(url, json=payload)
    print(f"Start game response: {response.json()}")

'''def start_demo(chat_id):
     send_message(chat_id, f"Click the link to play the demo: {DEMO_URL}")'''