from datetime import datetime
from django.contrib.auth.hashers import make_password, check_password
from random import randint
from django.shortcuts import render
import re
import pytz
from datetime import timedelta
from django.conf import settings

from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status

from .models import PhoneOTP, User
from .serializers import UserSerializer, UserSerializerWithToken

from ippanel import Client

# Create your views here.
utc = pytz.UTC

def validate_phone(phone):
    pattern = re.compile("^09[0|1|2|3][0-9]{8}$", re.IGNORECASE)
    return pattern.match(phone) is not None

def get_otp_code(phone):
    if phone:
        key = randint(99999, 999999)
        print(key)
        return key
    else:
        return False

def send_otp_code(phone, code):
    pid = '3mny8j14tj50mxk'
    fnum = '500010400000144'

    api_key = settings.OTP_API_KEY

    print(api_key)

    sms = Client(api_key)

    pattern_values = {
        'code': code,
    }

    bulk_id = sms.send_pattern(
        pid,
        f'+98{fnum}',
        f'98{phone}',
        pattern_values
    )

@api_view(['POST'])
def verify_phone_send_otp(request):
    phone_number = request.data.get('phone')

    if phone_number:
        phone = str(phone_number)

        if validate_phone(phone):
            key = get_otp_code(phone)

            if key:
                phone_otp = PhoneOTP.objects.filter(phone__iexact=phone)
                now = datetime.now().replace(tzinfo=utc)

                if phone_otp.exists():
                    phone_otp = phone_otp.first()
                    created_at = phone_otp.created_at.replace(tzinfo=utc)
                    obj_expiration_date = created_at + timedelta(days=1)

                    if now > obj_expiration_date:
                        phone_otp.delete()

                        new_phone_otp = PhoneOTP.objects.create(
                            phone = phone,
                            otp = str(key),
                            resend_at = now + timedelta(minutes=3),
                            expire_at = now + timedelta(minutes=3)
                        )

                        send_otp_code(phone[1:], str(key))

                        return Response({'detail': 'کد شش رقمی با موفقیت به موبایل شما ارسال شد.', 'phone': phone, 'resend_at': new_phone_otp.resend_at, 'expire_at': new_phone_otp.expire_at})
                    else:
                        count = phone_otp.count

                        if count <= 10:
                            resend_at = phone_otp.resend_at.replace(tzinfo=utc)

                            if now > resend_at:
                                phone_otp.otp = str(key)
                                phone_otp.resend_at = now + timedelta(minutes=3)
                                phone_otp.expire_at = now + timedelta(minutes=3)
                                phone_otp.count = count + 1
                                phone_otp.save()

                                send_otp_code(phone[1:], str(key))

                                return Response({'detail': 'کد شش رقمی با موفقیت به موبایل شما ارسال شد.', 'phone': phone, 'resend_at': phone_otp.resend_at, 'expire_at': phone_otp.expire_at})                
                            else:
                                return Response({'detail': 'لطفا منتظر بمانید تا امکان ارسال مجدد کد برای شما فعال شود. سپس یکبار صفحه را رفرش کنید.'}, status=status.HTTP_400_BAD_REQUEST)
                        else:
                            return Response({'detail': 'شما تا 24 ساعت مجاز به دریافت کد جدید نیستید.'}, status=status.HTTP_403_FORBIDDEN)
                else:
                    new_phone_otp = PhoneOTP.objects.create(
                        phone = phone,
                        otp = str(key),
                        resend_at = now + timedelta(minutes=3),
                        expire_at = now + timedelta(minutes=3)
                    )

                    send_otp_code(phone[1:], str(key))

                    return Response({'detail': 'کد شش رقمی با موفقیت به موبایل شما ارسال شد.', 'phone': phone, 'resend_at': new_phone_otp.resend_at, 'expire_at': new_phone_otp.expire_at})
            else:
                return Response({'detail': 'خطایی در هنگام ارسال کد پیش آمد.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'detail': 'شماره موبایل وارد شده اشتباه است.'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'detail': 'لطفا شماره موبایل خود را وارد کنید.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def verify_otp(request):
    phone_number = request.data.get('phone')
    sent_otp = request.data.get('otp')

    if phone_number and sent_otp:
        phone = str(phone_number)

        if validate_phone(phone):
            phone_otp = PhoneOTP.objects.filter(phone__iexact=phone)

            if phone_otp.exists():
                phone_otp = phone_otp.first()
                otp = phone_otp.otp
                now = datetime.now().replace(tzinfo=utc)
                expire_at = phone_otp.expire_at.replace(tzinfo=utc)

                if now <= expire_at:
                    if str(sent_otp) == str(otp):
                        phone_otp.is_validated = True
                        phone_otp.save()

                        user = User.objects.filter(phone__iexact=phone)

                        user_exists = False
                        is_admin_user = False

                        if user.exists():
                            user_exists = True

                            user = user.first()
                            is_admin_user = user.is_staff

                        return Response({'detail': 'درستی کد با موفقیت تایید شد. وارد شوید یا ثبت نام کنید.', 'user_exists': user_exists, 'is_admin_user': is_admin_user})
                    else:
                        return Response({'detail': 'کد وارد شده اشتباه است.'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'detail': 'کد ارسالی منقضی شده است. به مرحله قبل بازگردید و کد را مجددا ارسال کنید.'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                return Response({'detail': 'ابتدا باید شماره موبایل خود را تایید کنید.'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'detail': 'شماره موبایل وارد شده اشتباه است.'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'detail': 'لطفا شماره موبایل و کد ارسال شده را وارد کنید.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def register(request):
    phone_number = request.data.get('phone')
    name = request.data.get('name')

    if phone_number and name:
        phone = str(phone_number)

        if validate_phone(phone):
            phone_otp = PhoneOTP.objects.filter(phone__iexact=phone)
            user = User.objects.filter(phone__iexact=phone)

            if user.exists():
                return Response({'detail': 'کاربری با این شماره موبایل درحال حاضر وجود دارد.'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                if phone_otp.exists():
                    phone_otp = phone_otp.first()

                    if phone_otp.is_validated:
                        user = User.objects.create_user(
                            phone = phone,
                            name = str(name),
                            password = phone_otp.otp,
                        )
                        user.logged_in = True
                        user.save()

                        serializer = UserSerializerWithToken(user, many=False)
                        return Response(serializer.data)
                    else:
                        return Response({'detail': 'ابتدا باید کد ارسال شده را تایید کنید.'}, status=status.HTTP_403_FORBIDDEN)
                else:
                    return Response({'detail': 'ابتدا باید شماره موبایل خود را تایید کنید.'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'detail': 'شماره موبایل وارد شده اشتباه است.'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'detail': 'لطفا نام و شماره موبایل خود را وارد کنید.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    phone_number = request.data.get('phone')

    if phone_number:
        phone = str(phone_number)
        
        if validate_phone(phone):
            phone_otp = PhoneOTP.objects.filter(phone__iexact=phone)

            if phone_otp.exists():
                phone_otp = phone_otp.first()
                
                if phone_otp.is_validated:
                    user = User.objects.filter(phone__iexact=phone)

                    if user.exists():
                        user = user.first()
                        user.logged_in = True
                        user.password = make_password(phone_otp.otp)
                        user.save()

                        serializer = UserSerializerWithToken(user, many=False)

                        return Response(serializer.data)
                    else:
                        return Response({'detail': 'ابتدا باید ثبت نام کنید.'}, status=status.HTTP_403_FORBIDDEN)
                else:
                    return Response({'detail': 'ابتدا باید کد ارسال شده را تایید کنید.'}, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({'detail': 'ابتدا باید شماره موبایل خود را تایید کنید.'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'detail': 'شماره موبایل وارد شده اشتباه است.'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'detail': 'لطفا شماره موبایل خود را وارد کنید.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_admin(request):
    phone_number = request.data.get('phone')
    password = request.data.get('password')

    if phone_number:
        phone = str(phone_number)

        if validate_phone(phone):
            phone_otp = PhoneOTP.objects.filter(phone__exact=phone)

            if phone_otp.exists():
                phone_otp = phone_otp.first()

                if phone_otp.is_validated:
                    user = User.objects.filter(phone__iexact=phone)

                    if user.exists():
                        user = user.first()

                        if user.is_staff:
                            password = str(password)

                            if password != '':
                                if check_password(password, user.password):
                                    user.logged_in = True
                                    user.save()

                                    serializer = UserSerializerWithToken(user, many=False)
                                    return Response(serializer.data)
                                else:
                                    return Response({'detail': 'پسورد اشتباه است.'}, status=status.HTTP_400_BAD_REQUEST)
                            else:
                                return Response({'detail': 'لطفا پسورد را وارد کنید.'}, status=status.HTTP_400_BAD_REQUEST)
                        else:
                            return Response({'detail': 'شما کاربر ادمین نیستید.'}, status=status.HTTP_403_FORBIDDEN)
                    else:
                        return Response({'detail': 'چنین کاربری در سامانه وجود ندارد.'}, status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response({'detail': 'ابتدا باید کد ارسال شده را تایید کنید.'}, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({'detail': 'ابتدا باید شماره موبایل خود را تایید کنید.'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'detail': 'شماره موبایل وارد شده اشتباه است.'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'detail': 'لطفا شماره موبایل خود را وارد کنید.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def logout(request):
    phone_number = request.data.get('phone')

    if phone_number:
        phone = str(phone_number)

        if validate_phone(phone):
            user = User.objects.filter(phone__iexact=phone)

            if user.exists():
                user = user.first()
                user.logged_in = False
                user.save()

                phone_otp = PhoneOTP.objects.get(phone__iexact=phone)
                phone_otp.is_validated = False
                phone_otp.save()

                return Response({'detail': 'کاربر با موفقیت خارج شد.'})
            else:
                return Response({'detail': 'چنین کاربری در سامانه وجود ندارد.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': 'شماره موبایل وارد شده اشتباه است.'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'detail': 'لطفا شماره موبایل خود را وارد کنید.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated,])
def get_profile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated,])
def update_profile(request):
    user = request.user
    data = request.data

    user.name = data.get('name')
    user.phone = data.get('phone')
    user.email = data.get('email')

    user.save()

    serializer = UserSerializerWithToken(user, many=False)

    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def upload_profile_image(request):
    user = request.user
    
    user.image = request.FILES.get('image')
    user.save()

    return Response({'detail': 'عکس با موفقیت آپلود شد. لطفا یکبار صفحه را رفرش کنید.'})