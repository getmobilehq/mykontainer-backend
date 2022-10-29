from datetime import timedelta, datetime
from accounts.permissions import IsAdminOrShippingAdmin, IsAdminorReadOnly, IsBayAdmin, IsShippingAdminOrBayAdmin
from main.models import ShippingCompany
from .models import Demurage, DemurageSize, DemurrageCalculations
from .serializers import CalculatorSerializer, DemurageSerializer, SizeSerializer
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError
from .demurage_helper import amount_per_day

# from django.core.mail import send_mail
# Create your views here.

SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')

VAT = 0.075

HIGHEST_DAY_START = 25

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
            email = serializer.validated_data.get('email')
            demurage_type = serializer.validated_data.get("demurage_type")
            company = serializer.validated_data.get("shipping_company")
            company:ShippingCompany
            size = serializer.validated_data.get('size')
            size:DemurageSize
            free_days = serializer.validated_data.get('free_days')
            if serializer.validated_data.get('free_days') < size.free_days:
                raise ValidationError(detail={"error":"Your value is less than allowed free days"})
            
            day_range = (serializer.validated_data.get("end_date") - serializer.validated_data.get("start_date")).days + 1
            # print(day_range)
            chargeable_days = day_range - free_days
            # print(chargeable_days)
            
            # if chargeable_days <= 0:
            if chargeable_days <= 0:
                
                data = {
                        "message":"success",
                        "data":{
                                    "container_type":f"{size.container_type} {size.size}",
                                    "start_date":serializer.validated_data.get("start_date"),
                                    "end_date":serializer.validated_data.get("end_date"),
                                    "chargeable_days":0,
                                    "free_days": free_days,
                                    "amount" : 0,
                                    "vat_amount":0,
                                    "total":0,
                                    "currency": "NGN"
                        }
                    }
                DemurrageCalculations.objects.create(**data, email=email)
                return Response(data, status=status.HTTP_201_CREATED)

            else: 
                try:                
                    
                    days_to_charge = sorted([i +1 for i in range(free_days, day_range)]) #get days
                    # print(days_to_charge)
                    amounts = [] #amounts for various days the client owes
                    rates = Demurage.objects.filter(shipping_company=company, 
                                                    size=size, 
                                                    demurage_type=demurage_type,
                                                    is_active=True)
                    
                    for day in days_to_charge:
                        if day == HIGHEST_DAY_START:
                            highest_days_amount = amount_per_day(day, rates) #get amount from 25 days and above
                            day_index = days_to_charge.index(day) #find index of 22 day in days to charge list
                            amounts.append(len(days_to_charge[day_index:])*highest_days_amount) #slice the list, get the length and multiply it by the amount to get the value of all the days above 25
                            break
                        amounts.append(amount_per_day(day, rates))        
                    # print(amounts)
                    # print(company.name)
                    # print(f"{size.container_type} {size.size}")
                    # print(list(zip(amounts,days_to_charge)))
                    
                    amount = sum(amounts) #get the amount from the amount list
                    
                    vat_amount = amount*VAT
                    
                    data = {"message":"success",
                            "data":{
                                "container_type":f"{size.container_type} {size.size}",
                                "start_date":serializer.validated_data.get("start_date"),
                                "end_date":serializer.validated_data.get("end_date"),
                                "chargeable_days":chargeable_days,
                                "free_days": free_days,
                                "amount" : round(amount, 2),
                                "vat_amount":round(vat_amount, 2),
                                "total":round(amount+vat_amount, 2),
                                "currency": "NGN"
                                }}
                    values = data['data']
                    DemurrageCalculations.objects.create(**values, email=email)
                    return Response(data, status=status.HTTP_201_CREATED)
                except  Demurage.DoesNotExist:
                    errors = {"message":"failed",
                            "errors":"Cannot make this calculation now.\nPlease try again later.",
                            }
                    return Response(errors, status=status.HTTP_404_NOT_FOUND)
            
                
            
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
        shipping_company = request.GET.get('shipping_company')
        objs = DemurageSize.objects.filter(is_active=True)
        if shipping_company:
            objs = objs.filter(shipping_company=shipping_company)
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
    
# @swagger_auto_schema(methods=["post"], request_body=SendEmailSerializer())
# @api_view(["POST"])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
# def send_demurage_invoice(request):
#     pass
    
    
    
    