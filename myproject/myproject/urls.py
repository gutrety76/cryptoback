from django.urls import path
from django.contrib import admin

from crt.serializers import MyTokenObtainPairView
from crt.views import RegisterView, UserDetailView, LoginView, user_view, update_wallet, history, get_wallet, deposit, \
    withdrawel, checkWithdrawel, delete_notification, add_notification, exchanger

urlpatterns = [
    path('admin/', admin.site.urls),
    path('registration/', RegisterView.as_view(), name='register'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('login/', LoginView.as_view()),
    path('user/', user_view, name='user_view'),
    path('wallet/<int:pk>', update_wallet, name='get_wallet_id'),
    path('history/<int:pk>', history, name='history'),
    path('getwallet/<int:pk>', get_wallet),
    path('addpayment/<int:pk>/<str:cryptotype>/<str:amount>/', deposit),
    path('minuspayment/<int:pk>/<str:cryptotype>/<str:amount>/', withdrawel),
    path('checkwithdrawel/<int:pk>/<str:cryptotype>/<str:amount>/', checkWithdrawel),
    path('deletenotification/<int:pk>', delete_notification),
    path('notification/<int:pk>', add_notification),
    path('exchanges', exchanger)
]
