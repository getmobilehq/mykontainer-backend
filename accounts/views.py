from .serializers import LoginSerializer, CustomUserSerializer, NewOtpSerializer, OTPVerifySerializer, UserDeleteSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAdminUser
from django.contrib.auth import get_user_model
from .helpers.generators import generate_password
from .permissions import IsShippingAdmin
from rest_framework.exceptions import PermissionDenied, AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import authenticate
from django.contrib.auth.signals import user_logged_in
from djoser.views import UserViewSet
from django.contrib.auth.hashers import check_password

from rest_framework.decorators import action


User = get_user_model()

class CustomUserViewSet(UserViewSet):
    
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data.get("current_password")
        
        if check_password(password, instance.password):
            
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        elif request.user.role == "admin" and check_password(password, request.user.password):
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
    
        else:
            raise AuthenticationFailed(detail={"message":"incorrect password"})
        
        
@swagger_auto_schema(methods=['POST'], request_body=CustomUserSerializer())
@api_view(['POST', 'GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdminUser])
def shipping_admin(request):
    if request.method=="GET":
        objs = User.objects.filter(is_active=True, role="shipping_admin")
        serializer = CustomUserSerializer(objs, many=True)
        
        data = {"message":"success",
                "data" : serializer.data}
            
        return Response(data, status=status.HTTP_200_OK)
    
    elif request.method=="POST":
        
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
        
            
            serializer.validated_data['password'] = generate_password()
            serializer.validated_data['is_active'] = True
            serializer.validated_data['is_admin'] = True
            serializer.save()
            
            data = {
                'message' : "success",
                'data' : serializer.data,
            }

            return Response(data, status = status.HTTP_201_CREATED)

        else:
            data = {

                'message' : "failed",
                'error' : serializer.errors,
            }

            return Response(data, status = status.HTTP_400_BAD_REQUEST)
        
        

@swagger_auto_schema(methods=['POST'], request_body=CustomUserSerializer())
@api_view(['POST', 'GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsShippingAdmin])
def bay_admin(request):
    
    if request.method=="GET":
        objs = User.objects.filter(is_active=True, role="bay_admin")
        serializer = CustomUserSerializer(objs, many=True)
        
        data = {"message":"success",
                "data" : serializer.data}
            
        return Response(data, status=status.HTTP_200_OK)
    
    elif request.method=="POST":
        
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            
            serializer.validated_data['password'] = generate_password()
            serializer.validated_data['is_active'] = True
            serializer.validated_data['is_admin'] = True
            serializer.save()
            
            data = {
                'message' : "success",
                'data' : serializer.data,
            }

            return Response(data, status = status.HTTP_201_CREATED)

        else:
            data = {

                'message' : "failed",
                'error' : serializer.errors,
            }

            return Response(data, status = status.HTTP_400_BAD_REQUEST)
        


@swagger_auto_schema(method='post', request_body=LoginSerializer())
@api_view([ 'POST'])
def user_login(request):
    
    """Allows users to log in to the platform. Sends the jwt refresh and access tokens. Check settings for token life time."""
    
    if request.method == "POST":
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            # provider = 'email'
            user = authenticate(request, email = data['email'], password = data['password'])
            if user is not None:
                if user.is_active==True:
                    if user.is_disabled == True:
                        data = {
                
                        'error': 'This account has been suspended. Please contact the administrator'
                        }
                        return Response(data, status=status.HTTP_403_FORBIDDEN)
                        
                    else:
                        try:
                            
                            refresh = RefreshToken.for_user(user)

                            user_detail = {}
                            user_detail['id']   = user.id
                            user_detail['first_name'] = user.first_name
                            user_detail['last_name'] = user.last_name
                            user_detail['email'] = user.email
                            user_detail['phone'] = user.phone
                            user_detail['role'] = user.role
                            user_detail['is_admin'] = user.is_admin
                            # user_detail['image_url'] = user.image_url
                            user_detail['access'] = str(refresh.access_token)
                            user_detail['refresh'] = str(refresh)
                            user_logged_in.send(sender=user.__class__,
                                                request=request, user=user)

                            data = {
        
                            "message":"success",
                            'data' : user_detail,
                            }
                            return Response(data, status=status.HTTP_200_OK)
                        

                        except Exception as e:
                            raise e
                
                else:
                    data = {
                    
                    'error': 'This account has not been activated'
                    }
                    return Response(data, status=status.HTTP_403_FORBIDDEN)

            else:
                data = {
                    
                    'error': 'Please provide a valid email and a password'
                    }
                return Response(data, status=status.HTTP_401_UNAUTHORIZED)
        else:
                data = {
                    
                    'error': serializer.errors
                    }
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            

@swagger_auto_schema(methods=['POST'],  request_body=NewOtpSerializer())
@api_view(['POST'])
def reset_otp(request):
    if request.method == 'POST':
        serializer = NewOtpSerializer(data = request.data)
        if serializer.is_valid():
            data = serializer.get_new_otp()
            
            return Response(data, status=status.HTTP_200_OK)
        
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        
        
            
@swagger_auto_schema(methods=['POST'], request_body=OTPVerifySerializer())
@api_view(['POST'])
def otp_verification(request):
    
    """Api view for verifying OTPs """

    if request.method == 'POST':

        serializer = OTPVerifySerializer(data = request.data)

        if serializer.is_valid():
            data = serializer.verify_otp(request)
            
            return Response(data, status=status.HTTP_200_OK)
        else:

            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdminUser])
def suspend_user(request, user_id):
    
    """Api view for suspending users """

    if request.method == 'GET':
        
        try:
            user = User.objects.get(id=user_id, is_active=True, is_disabled=False)
            user.is_disabled = True
            user.save()
            return Response({"message": "User is suspended"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:

            return Response({"message":"User not activated or has been suspended already"}, status = status.HTTP_400_BAD_REQUEST)
        
        

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdminUser])
def unsuspend_user(request, user_id):
    
    """Api view to unsuspend users """

    if request.method == 'GET':
        
        try:
            user = User.objects.get(id=user_id, is_active=True, is_disabled=True)
            user.is_disabled = False
            user.save()
            return Response({"message": "User is re-enabled"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:

            return Response({"message":"User not activated or has been re-enabled already"}, status = status.HTTP_400_BAD_REQUEST)