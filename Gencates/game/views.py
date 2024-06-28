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
from django.http import JsonResponse
TELEGRAM_BOT_TOKEN = settings.TELEGRAM_TOKEN
CHANNEL_USERNAME = '@Gene_Cats'


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


def check_subscription(user_id):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getChatMember'
    payload = {
        'chat_id': CHANNEL_USERNAME,
        'user_id': user_id
    }
    response = requests.get(url, params=payload)
    data = response.json()

    if data['ok']:
        status = data['result']['status']
        return status in ['member', 'administrator', 'creator']
    return False

@api_view(['GET'])
def get_referral_link(request):
    user = request.user
    if not user.is_authenticated:
        return Response({'error': 'User not authenticated'}, status=400)

    telegram_user_id = user.profile.telegram_user_id  # Assuming you store Telegram user ID in the user's profile
    if not check_subscription(telegram_user_id):
        return Response({'error': 'You must subscribe to the channel first'}, status=400)

    domain = 'http://127.0.0.1:8000'
    referral_link = f"{domain}/register?ref={user.userprofile.referral_code}"
    return Response({'referral_link': referral_link})


@api_view(['POST'])
def register_with_referral(request):
    referral_code = request.data.get('referral_code')
    user = request.user
    if not user.is_authenticated or not referral_code:
        return Response({'error': 'Invalid request'}, status=400)

    referrer = get_object_or_404(UserProfile, referral_code=referral_code)
    user_profile = user.userprofile
    user_profile.referred_by = referrer
    user_profile.save()

    # Увеличение уровня у реферера и добавление монет
    referrer.coins += 100
    referrer.referrals_count += 1
    referrer.increase_level()  # Увеличение уровня
    referrer.save()

    user_profile.coins += 50
    forest_moggy = Cat.objects.get(name="Forest Moggy")
    user_profile.cats.add(forest_moggy)
    user_profile.save()

    return Response({'status': 'User registered with referral'})

