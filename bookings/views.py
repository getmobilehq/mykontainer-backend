from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render
from accounts.helpers.generators import generate_code
from django.utils import timezone
from accounts.permissions import IsBayAdmin, IsShippingAdminOrBayAdmin
from .models import Booking, ShippingCompany, BayArea
from .serializers import AddBookingSerializer, BookingCompleteSerializer, BookingSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from config.settings import Common
from django.template.loader import render_to_string
from xhtml2pdf import pisa


# Create your views here.

SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')

User = get_user_model()
    
@swagger_auto_schema(methods=["POST"], request_body=AddBookingSerializer())
@api_view([ 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def booking(request):
    
    if request.method=='POST':
        serializer = AddBookingSerializer(data=request.data)
        
        if serializer.is_valid():
            bay = serializer.validated_data['bay_area']
            bay:BayArea
            
            if bay.available_space ==0:
                raise ValidationError({"message":"Available spaces for this bay area has been used up."})

            
            data = serializer.create(serializer.validated_data,request)
            


            return Response(data, status=status.HTTP_201_CREATED)
        else:
            errors = {
                "message":"failed",
                "errors":serializer.errors}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
 

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_booking(request):       
    if request.method=="GET":
            if request.user.role == "shipping_admin":
                objs = Booking.objects.filter(shipping_company = request.user.shipping_company, is_active=True)
            elif request.user.role == "bay_admin":
                objs = Booking.objects.filter(bay_area = request.user.bay_area, is_active=True)
            elif request.user.role == "admin":
                objs = Booking.objects.filter(is_active=True)
            else:
                raise PermissionDenied({
                'message' : "You do not have the permission to perform this action"
            })
                
            serializer = BookingSerializer(objs, many=True)
            
            data = {"message":"success",
                    "data" : serializer.data}
                
            return Response(data, status=status.HTTP_200_OK)
        
        

@swagger_auto_schema(methods=['PUT', 'DELETE'], request_body=BookingSerializer())
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def booking_detail(request, booking_id):
    """"""
    
    try:
        obj = Booking.objects.get(id = booking_id, is_active=True)
    
    except Booking.DoesNotExist:
        data = {
                'message' : "Does not exist"
            }

        return Response(data, status=status.HTTP_404_NOT_FOUND)
    
    if request.method not in SAFE_METHODS and request.user != obj.user:
        raise PermissionDenied({
                'message' : "You do not have the permission to perform this action"
            })
        
        
    if request.method == 'GET':
        serializer = BookingSerializer(obj)
        
        data = {
                'message' : "success",
                'data' : serializer.data,
            }

        return Response(data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = BookingSerializer(obj, data = request.data, partial=True) 

        if serializer.is_valid():
            
            serializer.save()

            data = {
                'message' : "Successful",
                'data' : serializer.data,
            }

            return Response(data, status = status.HTTP_201_CREATED)

        else:
            data = {

                'message' : "Unsuccessful",
                'error' : serializer.errors,
            }

            return Response(data, status = status.HTTP_400_BAD_REQUEST)

    #delete the account
    elif request.method == 'DELETE':
        obj.delete()


        return Response({}, status = status.HTTP_204_NO_CONTENT)
    
    

@swagger_auto_schema(methods=["POST"], request_body=BookingCompleteSerializer())
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsBayAdmin])
def booking_complete(request):
    """"""
    
    if request.method == "POST":
        serializer = BookingCompleteSerializer(data=request.data)
        
        if serializer.is_valid():
            data = serializer.verify(request)
            
            return Response(data, status = status.HTTP_201_CREATED)

        else:
            data = {

                'message' : "Unsuccessful",
                'error' : serializer.errors,
            }

            return Response(data, status = status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def user_booking(request):       
    if request.method=="GET":
        objs = Booking.objects.filter(user=request.user)
        
        dates = objs.values_list('date').distinct()
        print(dates)
        data = {}
        for date in dates:
            date=date[0]
            data_per_date = objs.filter(date=date)
            serializer = BookingSerializer(data_per_date, many=True)
            data[str(date)] = serializer.data
            
        
        data = {"message":"success",
                "data" : data}
            
        return Response(data, status=status.HTTP_200_OK)
    

@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsBayAdmin])
def bookings_pdf(request):
    # request.user = User.objects.first()
    date=timezone.now().date()

    objs = Booking.objects.filter(is_active=True, bay_area=request.user.bay_area, date=date)
    template_path = 'bookings.html'

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Bookings-{date}.pdf"'

    html = render_to_string(template_path, 
                            {'bookings': objs,
                             'date':date,
                             "user":request.user
                             })

    pisa.CreatePDF(html, dest=response)

    return response 