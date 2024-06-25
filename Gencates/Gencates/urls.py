from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from game.views import CatViewSet, UserProfileViewSet, IncubatorViewSet, StorageViewSet, CatyCoinViewSet, \
    CrossbreederViewSet, IncomeRoomViewSet, HibernationRoomViewSet, get_referral_link, register_with_referral

router = DefaultRouter()
router.register(r'cats', CatViewSet)
router.register(r'profiles', UserProfileViewSet)
router.register(r'incubators', IncubatorViewSet)
router.register(r'storages', StorageViewSet)
router.register(r'crossbreeders', CrossbreederViewSet)
router.register(r'income_rooms', IncomeRoomViewSet)
router.register(r'hibernation_rooms', HibernationRoomViewSet)
router.register(r'catycoins', CatyCoinViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('', include('game.urls')),
    path('api/get_referral_link/', get_referral_link),
    path('api/register_with_referral/', register_with_referral),

]
