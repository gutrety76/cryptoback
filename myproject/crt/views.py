import json
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from rest_framework import generics, status, serializers
from rest_framework.response import Response
from django.contrib.auth import authenticate
import jwt
from rest_framework.views import APIView

from crt.models import Wallet, Exchange, Deposit, Withdrawal, Notification
from crt.serializers import UserSerializer, WalletSerializer, ExchangeSerializer, HistorySerializer, DepositSerializer, \
    NotificationSerializer, ExchangeraSerializer


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()

    password = serializers.CharField()


class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(**serializer.validated_data)
        if user:
            payload = {
                'id': user.id,
                'username': user.username
            }
            token = jwt.encode(payload, 'secret', algorithm='HS256')
            wallet = Wallet.objects.get(user=user)
            wallet_id = wallet.id
            wallet_serializer = WalletSerializer(wallet)

            return Response(
                {'token': token, 'wallet': {
                    "wallet": wallet_serializer.data,
                    "walletid": wallet.id}, 'username': {
                    "username": user.username,
                    "email": user.email,
                    "user_id": user.id
                }})
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.create(serializer.validated_data)

        return Response(user_data)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_wallet(self, obj):
        try:
            return Wallet.objects.get(user=obj)

        except Wallet.DoesNotExist:
            return 0

    def get_object(self):
        obj = super().get_object()
        obj.wallet = self.get_wallet(obj)
        return obj


from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.db.models import F


@api_view(['PUT'])
def update_wallet(request, pk):
    if request.method == 'PUT':
        req_data = json.loads(request.body.decode())
        add_currency = req_data.get('add_currency', 0)
        add_currency_type = req_data.get('add_currency_type', '')
        minus_currency = req_data.get('minus_currency', 0)
        minus_currency_type = req_data.get('minus_currency_type', '')

        try:
            wallet = Wallet.objects.get(id=pk)
            if getattr(wallet, minus_currency_type) < minus_currency:
                raise Exception(f"{minus_currency_type} balance is not enough")
            Wallet.objects.filter(id=pk).update(**{add_currency_type: F(add_currency_type) + add_currency,
                                                   minus_currency_type: F(minus_currency_type) - minus_currency})
            if wallet.user.is_authenticated:
                exchange = Exchange(user_id=wallet.id, cryptoType_from=minus_currency_type,
                                    cryptoType_to=add_currency_type, cryptoAmount_from=minus_currency,
                                    cryptoAmount_to=add_currency)
                exchange.save()
                exchange_serializer = ExchangeSerializer(exchange)
                serializer = WalletSerializer(wallet)
                try:
                    wallet.full_clean()
                except ValidationError as e:
                    return JsonResponse({'status': 'error', 'message': e.message_dict})
                return Response({"wallet": serializer.data, "exchange": exchange_serializer.data})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})


@api_view(['GET'])
def withdrawel(request, pk, cryptotype, amount):
    if request.method == 'GET':
        try:
            # Get all exchanges, deposits and withdrawels by user_id
            try:
                amount_decimal = Decimal(amount)
                wallet = Wallet.objects.get(id=pk)
                if getattr(wallet, cryptotype) < amount_decimal:
                    raise Exception(f"{cryptotype} balance is not enough")
                setattr(wallet, cryptotype, getattr(wallet, cryptotype) - Decimal(amount))
                wallet.save()
                withdrawel = Withdrawal(user_id=wallet.id, crypto_type=cryptotype, amount=Decimal(amount))
                withdrawel.save()
                notification = Notification(user_id=wallet.id, message="Your withdrawal is approved")
                notification.save()
                return Response(status=200, data={'success': 'value minused from wallet'})
            except Exception as e:
                return Response(status=500, data={'error': str(e)})
            # Serialize the history




        except ValidationError as e:
            if e.message_dict != "Field name `user` is not valid for model `Exchange`.":
                return JsonResponse({'status': 'error', 'message': e.message_dict})

        # Return the history as a JSON response
        return JsonResponse({'deposit': DepositSerializer.data})


@api_view(['GET'])
def checkWithdrawel(request, pk, cryptotype, amount):
    if request.method == 'GET':
        try:
            # Get all exchanges, deposits and withdrawels by user_id
            try:
                amount_decimal = Decimal(amount)
                wallet = Wallet.objects.get(id=pk)
                if getattr(wallet, cryptotype) < amount_decimal:
                    raise Exception(f"{cryptotype} balance is not enough")
                return Response(status=200, data={'success': 'true'})
            except Exception as e:
                return Response(status=500, data={'error': str(e)})
            # Serialize the history




        except ValidationError as e:
            if e.message_dict != "Field name `user` is not valid for model `Exchange`.":
                return JsonResponse({'status': 'error', 'message': e.message_dict})

        # Return the history as a JSON response
        return JsonResponse({'deposit': DepositSerializer.data})


@api_view(['GET'])
def deposit(request, pk, cryptotype, amount):
    if request.method == 'GET':
        try:
            # Get all exchanges, deposits and withdrawels by user_id

            try:
                wallet = Wallet.objects.get(id=pk)
                setattr(wallet, cryptotype, getattr(wallet, cryptotype) + Decimal(amount))
                wallet.save()
                deposit = Deposit(user_id=wallet.id, crypto_type=cryptotype, amount=Decimal(amount))
                deposit.save()
                notification = Notification(user_id=wallet.id, message="Your deposit is approved")
                notification.save()
                return Response(status=200, data={'success': 'value added to wallet'})
            except Exception as e:
                return Response(status=500, data={'error': str(e)})
            # Serialize the history




        except ValidationError as e:
            if e.message_dict != "Field name `user` is not valid for model `Exchange`.":
                return JsonResponse({'status': 'error', 'message': e.message_dict})

        # Return the history as a JSON response
        return JsonResponse({'deposit': DepositSerializer.data})


@api_view(['GET'])
def history(request, pk):
    if request.method == 'GET':

        try:
            # Get all exchanges, deposits and withdrawels by user_id
            exchanges = Exchange.objects.filter(user_id=pk)
            deposits = Deposit.objects.filter(user_id=pk)
            withdrawal = Withdrawal.objects.filter(user_id=pk)

            # Merge the querysets
            history = list(exchanges) + list(deposits) + list(withdrawal)
            history = sorted(history, key=lambda x: x.date)
            history_serializer = HistorySerializer(history, many=True)

            # Serialize the history




        except ValidationError as e:
            if e.message_dict != "Field name `user` is not valid for model `Exchange`.":
                return JsonResponse({'status': 'error', 'message': e.message_dict})

        # Return the history as a JSON response
        return JsonResponse({'status': 'success', 'history': history_serializer.data})


@api_view(['GET'])
def get_wallet(request, pk):
    try:
        wallet = Wallet.objects.get(pk=pk)
        serializer = WalletSerializer(wallet)
        notification = Notification.objects.filter(user_id=pk)

        sserialer = NotificationSerializer(notification, many=True)

        return Response({"wallet": serializer.data, "notifications": sserialer.data})
    except Wallet.DoesNotExist:
        return Response({"error": "Wallet not found."}, status=404)
    except Notification.DoesNotExist:
        return Response({"wallet": serializer.data})


@api_view(['GET'])
def delete_notification(request, pk):
    try:
        notification = Notification.objects.get(pk=pk)
        notification.delete()
        return Response({'status': "success"})
    except:
        return Response({"status": "error"})
@api_view(['GET'])
def add_notification(request, pk):
    try:
        notification = Notification(user_id=pk, message="Dear customer! Your funds are blocked due to exceeding the limit of funds without proof of citizenship in the United Kingdom")
        notification.save()
        return Response({'status': "success"})
    except:
        return Response({"status": "error"})
@api_view(['GET'])
def exchanger(request):
    try:

        exchanges = Exchange.objects.all().order_by('-date')[:10]
        serializer = ExchangeraSerializer(exchanges, many=True)

        return Response(serializer.data)
    except:
        return Response({"status": "error"})



@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_view(request):
    if request.user.is_authenticated:
        user = request.user
        return Response({'username': user.username})
    else:
        return Response({'error': 'You are not authenticated'})
