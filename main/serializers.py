from rest_framework import serializers
from .models import ShippingCompany, BayArea
from rest_framework.exceptions import ValidationError

class ShippingCompanySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ShippingCompany
        fields = '__all__'
        
        

class BayAreaSerializer(serializers.ModelSerializer):
    shipping_company_detail = serializers.ReadOnlyField()
    
    class Meta:
        model = BayArea
        fields = '__all__'

