import jwt
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Wallet, Exchange, Deposit, Withdrawal, Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ("id", 'message',)


class ExchangeraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exchange
        fields = ('user_id', 'cryptoType_from', 'cryptoType_to','cryptoAmount_from','cryptoAmount_to','date')

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = (
            'BTC', "ETH", 'BNB', 'USDT', 'BUSD', 'ADA', 'XRP', 'SOL', 'DOGE', 'DOT', "ETC", 'TRX', "ETC", 'XLM', 'ATOM',
            'NEAR')


class WalletIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ("id",)


class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit
        fields = ('id', 'user_id', 'crypto_type', 'amount', 'date')


class HistorySerializer(serializers.Serializer):
    type = serializers.CharField(read_only=True)
    cryptoType_from = serializers.CharField(read_only=True)
    cryptoType_to = serializers.CharField(read_only=True)
    cryptoAmount_from = serializers.DecimalField(max_digits=100, decimal_places=10, read_only=True)
    cryptoAmount_to = serializers.DecimalField(max_digits=100, decimal_places=10, read_only=True)
    crypto_type = serializers.CharField(read_only=True)
    amount = serializers.DecimalField(max_digits=100, decimal_places=10, read_only=True)

    def to_representation(self, instance):
        if isinstance(instance, Exchange):
            self.fields['type'] = serializers.CharField(default='exchange')
        elif isinstance(instance, Deposit):
            self.fields['type'] = serializers.CharField(default='deposit')
        elif isinstance(instance, Withdrawal):
            self.fields['type'] = serializers.CharField(default='withdrawal')
        return super(HistorySerializer, self).to_representation(instance)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class ExchangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exchange
        fields = (
            'id', 'user', 'cryptoType_from', 'cryptoType_to', 'cryptoAmount_from', 'cryptoAmount_to', 'date')


class UserSerializer(serializers.ModelSerializer):
    wallet = WalletSerializer(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', "wallet")
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        wallet = Wallet.objects.create(user=user)
        wallet_id = wallet.id
        user_serializer = UserSerializer(user)
        payload = {
            'id': user.id,
            'username': user.username
        }

        return {
            'user': user_serializer.data,
            "walletid": wallet_id
        }
