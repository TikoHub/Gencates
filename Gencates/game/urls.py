from django.urls import path
from .views import login_view, get_referral_link, register_with_referral


urlpatterns = [
    path('login/', login_view, name='login'),
    path('get-referral-link/', get_referral_link, name='get_referral_link'),

]
