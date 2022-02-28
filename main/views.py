from accounts.permissions import IsAdminOrShippingAdmin, IsBayAdmin, IsShippingAdminOrBayAdmin
from .models import ShippingCompany, BayArea
from .serializers import ShippingCompanySerializer, BayAreaSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.exceptions import PermissionDenied
# Create your views here.

SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')


@swagger_auto_schema(methods=["POST"], request_body=ShippingCompanySerializer(many=True))
@api_view(["GET", 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdminUser])
def shipping_company(request):
    
    if request.method=="GET":
        objs = ShippingCompany.objects.filter(is_active=True)
        serializer= ShippingCompanySerializer(objs, many=True)
        
        data = {"message":"success",
                "data" : serializer.data}
            
        return Response(data, status=status.HTTP_200_OK)
    
    elif request.method=='POST':
        serializer = ShippingCompanySerializer(data=request.data, many=True)
        
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
        
        

@swagger_auto_schema(methods=['PUT', 'DELETE'], request_body=ShippingCompanySerializer())
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdminUser])
def shipping_company_detail(request, company_id):
    """"""
    
    try:
        obj = ShippingCompany.objects.get(id = company_id, is_active=True)
    
    except ShippingCompany.DoesNotExist:
        data = {
                'message' : "Does not exist"
            }

        return Response(data, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ShippingCompanySerializer(obj)
        
        data = {
                'status'  : True,
                'message' : "Successful",
                'data' : serializer.data,
            }

        return Response(data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = ShippingCompanySerializer(obj, data = request.data, partial=True) 

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


@swagger_auto_schema(methods=["POST"], request_body=BayAreaSerializer(many=True))
@api_view(["GET", 'POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdminOrShippingAdmin])
def bay_area(request):
    
    if request.method=="GET":
        if request.user.role == "admin":
            objs = BayArea.objects.filter(is_active=True)
        else:
            objs = BayArea.objects.filter(is_active=True, shipping_company=request.user.shipping_company)
            
        serializer = BayAreaSerializer(objs, many=True)
        
        data = {"message":"success",
                "data" : serializer.data}
            
        return Response(data, status=status.HTTP_200_OK)
    
    elif request.method=='POST':
        serializer = BayAreaSerializer(data=request.data, many=True)
        
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
        
        

@swagger_auto_schema(methods=['PUT', 'DELETE'], request_body=BayAreaSerializer())
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdminOrShippingAdmin])
def bay_area_detail(request, bay_area_id):
    """"""
    
    try:
        obj = BayArea.objects.get(id = bay_area_id, is_active=True)
    
    except BayArea.DoesNotExist:
        data = {
                'message' : "Does not exist"
            }

        return Response(data, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BayAreaSerializer(obj)
        
        data = {
                'status'  : True,
                'message' : "Successful",
                'data' : serializer.data,
            }

        return Response(data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = BayAreaSerializer(obj, data = request.data, partial=True) 

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