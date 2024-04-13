from rest_framework import generics
from rest_framework.response import Response
from .serializers import *
from rest_framework.authtoken.models import Token
from django.contrib.auth import  authenticate
from drf_yasg.utils import swagger_auto_schema
from .models import User, MailVerificationOTP
from . import service
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated


# APIs 
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer

    @swagger_auto_schema(
        operation_summary = 'Register Student',
        operation_description='Register with your email and password which is securely managed',
        )
    def post(self, request):
        try :
            # get data from request
            email = request.data['email']
            password = request.data['password']
            username = request.data['username']

            # check if user is already registered with the given mail
            if User.objects.filter(email = email).exists():
                raise Exception('this email is already in use for an account')

            # create user
            serializer = self.serializer_class(data = {'email' : email, 'password' : password, 'username' : username})
            serializer.is_valid(raise_exception = True)
            user = serializer.save()

            # get and store otp to verify this email    
            otp = service.get_otp_for_mail_verification(user)

            # send this otp to user's mail
            service.send_otp_for_mail_verification(otp = otp, user= user)
            return Response({'message' : 'User registered Successfully'}, status = 200)

        
        except Exception as e:
            return  Response({'message' : str(e)}, status= 400)


class ResendOTPForMailVerificationView(generics.CreateAPIView):
    serializer_class= EmailSerializer
    def post(self,request):
        try :
            email = request.data['email']
            
            if not User.objects.filter(email = email).exists():
                raise Exception('Invalid Email')
    
            user = User.objects.get(email=email)
    
            if user.is_verified:
                raise Exception('Email already verified')
    
            # get and store otp to verify this email    
            otp = service.get_otp_for_mail_verification(user)
    
            # send this otp to user's mail
            service.send_otp_for_mail_verification(otp = otp, user= user)
            return Response({'message' : 'request succesfull'}, status = 200)    
                
    
        except Exception as e :
            return Response({'message' : str(e)}, status = 400)



class MailVerificationView(generics.CreateAPIView):
    serializer_class= MailAndOTPSerializer
    def post(self,request):
        try : 
            email = request.data['email']
            otp = request.data['otp']

            if not User.objects.filter(email = email).exists():
                raise Exception('invalid email')

            user = User.objects.get(email = email)

            if user.is_verified:
                    raise Exception('Email already verified')

            if not MailVerificationOTP.objects.filter(user = user.id).exists():
                raise Exception('try resending otp')
            
            obj = MailVerificationOTP.objects.get(user = user.id)
            
            thirty_minutes_ago = timezone.now() - timezone.timedelta(minutes=30)
                
            if obj.updated_at < thirty_minutes_ago:
                raise Exception('otp expired')
            
            if obj.otp != int(otp):
                raise Exception('incorrect otp')  

            obj.delete()  
            user.is_verified = True
            user.save()


            return Response({'message' : 'verification successfull'}, status = 200)


        except Exception as e:
            return Response({'message'  : str(e)}, status = 400)


class LoginView(generics.CreateAPIView):
    serializer_class= LoginSerializer
    def post(self,request):
        try :
            email = request.data['email']
            password = request.data['password']

            user = authenticate(password = password, username = email)

            if not user :
                raise Exception('invalid credentials')

            if not user.is_verified : 
                raise Exception('email not verified')

            token, created = Token.objects.get_or_create(user=user)
            return Response({'message' : token.key}, status = 200)
        

        except Exception as e:
            return Response({'message' : str(e)}, status = 400)
        
    