from accounts.permissions import IsAdminOrShippingAdmin, IsAdminorReadOnly, IsBayAdmin, IsShippingAdminOrBayAdmin
from main.models import ShippingCompany
from .models import Demurage, DemurageSize
from .serializers import CalculatorSerializer, DemurageSerializer, SizeSerializer
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError
# Create your views here.

SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')

VAT = 0.075

@swagger_auto_schema(methods=["POST"], request_body=DemurageSerializer())
@api_view(["GET", 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdminorReadOnly])
def demurage(request):
    
    if request.method=="GET":
        objs = Demurage.objects.filter(is_active=True)
        serializer= DemurageSerializer(objs, many=True)
        
        data = {"message":"success",
                "data" : serializer.data}
            
        return Response(data, status=status.HTTP_200_OK)
    
    elif request.method=='POST':
        serializer = DemurageSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            
            data = {"message":"success",
                    "data" : serializer.data}
            
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            errors = {
                "message":"failed",
                "errors":serializer.errors}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        
        

@swagger_auto_schema(methods=['PUT', 'DELETE'], request_body=DemurageSerializer())
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdminUser])
def demurage_detail(request, rate_id):
    
    try:
        obj = Demurage.objects.get(id = rate_id, is_active=True)
    
    except Demurage.DoesNotExist:
        data = {
                'message' : "Does not exist"
            }

        return Response(data, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DemurageSerializer(obj)
        
        data = {
                'status'  : True,
                'message' : "Successful",
                'data' : serializer.data,
            }

        return Response(data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = DemurageSerializer(obj, data = request.data, partial=True) 

        if serializer.is_valid():
            
            serializer.save()

            data = {
                'message' : "Successful",
                'data' : serializer.data,
            }

            return Response(data, status = status.HTTP_202_ACCEPTED)

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
    
    

@swagger_auto_schema(methods=["POST"], request_body=CalculatorSerializer())
@api_view(['POST'])
@permission_classes([AllowAny])
def calculate_demurage(request):
    
    
    if request.method=='POST':
        serializer = CalculatorSerializer(data=request.data)
        
        if serializer.is_valid():
            demurage_type = serializer.validated_data.get("demurage_type")
            company = serializer.validated_data.get("shipping_company")
            
            size = serializer.validated_data.get('size')
            size:DemurageSize
            
            day_range = (serializer.validated_data.get("end_date") - serializer.validated_data.get("start_date")).days
            
            if day_range >= size.free_days:
                days = day_range - size.free_days 
                try:
                    rate = Demurage.objects.get(shipping_company=company, 
                                        size=size, 
                                        start_day__lte=days, 
                                        end_day__gte=days, 
                                        demurage_type=demurage_type,
                                        is_active=True)
                    amount = days*rate.price_per_day
                    vat_amount = amount*VAT
                    
                    data = {"message":"success",
                            "data":{
                                "container_type":size.size,
                                "start_date":serializer.validated_data.get("start_date"),
                                "end_date":serializer.validated_data.get("end_date"),
                                "chargeable_days":days,
                                "amount" : amount,
                                "vat_amount":vat_amount,
                                "total":amount+vat_amount,
                                "currency": "NGN"
                                }}
                except Demurage.DoesNotExist:
                    errors = {"message":"failed",
                            "errors":"unable to fetch range. Not found"
                            }
                    return Response(errors, status=status.HTTP_404_NOT_FOUND)
            else:
                data = {
                    "message":"success",
                    "data":{
                                "container_type":size.size,
                                "start_date":serializer.validated_data.get("start_date"),
                                "end_date":serializer.validated_data.get("end_date"),
                                "chargeable_days":0,
                                "amount" : 0,
                                "vat_amount":0,
                                "total":0,
                                "currency": "NGN"
                    }
                }
                
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            errors = {
                "message":"failed",
                "errors":serializer.errors}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        
        
        
        
@swagger_auto_schema(methods=["POST"], request_body=SizeSerializer())
@api_view(["GET", 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdminorReadOnly])
def demurage_sizes(request):
    
    if request.method=="GET":
        objs = DemurageSize.objects.filter(is_active=True)
        serializer= SizeSerializer(objs, many=True)
        
        data = {"message":"success",
                "data" : serializer.data}
            
        return Response(data, status=status.HTTP_200_OK)
    
    elif request.method=='POST':
        serializer = SizeSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            
            data = {"message":"success",
                    "data" : serializer.data}
            
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            errors = {
                "message":"failed",
                "errors":serializer.errors}
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        
        

@swagger_auto_schema(methods=['PUT', 'DELETE'], request_body=SizeSerializer())
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdminUser])
def demurage_size_detail(request, size_id):
    
    try:
        obj = DemurageSize.objects.get(id = size_id, is_active=True)
    
    except DemurageSize.DoesNotExist:
        data = {
                'message' : "Does not exist"
            }

        return Response(data, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SizeSerializer(obj)
        
        data = {
                'status'  : True,
                'message' : "Successful",
                'data' : serializer.data,
            }

        return Response(data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = SizeSerializer(obj, data = request.data, partial=True) 

        if serializer.is_valid():
            
            serializer.save()

            data = {
                'message' : "Successful",
                'data' : serializer.data,
            }

            return Response(data, status = status.HTTP_202_ACCEPTED)

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