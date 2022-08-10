from rest_framework import serializers
from main.models import ShippingCompany
from .models import Demurage, DemurageSize
from rest_framework.exceptions import ValidationError


class SizeSerializer(serializers.ModelSerializer):
    shipping_company_detail = serializers.ReadOnlyField()
    
    class Meta:
        model = DemurageSize
        fields = '__all__'
        
    def validate_shipping_company(self, data):
        if data is None:
            raise ValidationError(["This field cannot be null"])
        
        try:
            obj = ShippingCompany.objects.get(id=data, is_active=True)
        except ShippingCompany.DoesNotExist:
            raise ValidationError(["Enter a valid shipping company id"])
        return obj
    
        
class DemurageSerializer(serializers.ModelSerializer):
    shipping_company_detail = serializers.ReadOnlyField()
    size_detail = serializers.ReadOnlyField()
    class Meta:
        model = Demurage
        fields = '__all__'
        write_only_fields = ['shipping_company', 'size']
        
        
    def validate_size(self, data):
        if data is None:
            raise ValidationError(["This field cannot be null"])
        
        return data
    
class CalculatorSerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    free_days = serializers.IntegerField()
    shipping_company = serializers.UUIDField()
    size = serializers.UUIDField()
    demurage_type = serializers.CharField(max_length=6)
    
    
    def validate_shipping_company(self, data):
        try:
            company = ShippingCompany.objects.get(id=data, is_active=True)
        except ShippingCompany.DoesNotExist:
            raise ValidationError(detail="shipping company does not exist")
        return company
    
    def validate_size(self, data):
        try:
            size = DemurageSize.objects.get(id=data, is_active=True)
        except DemurageSize.DoesNotExist:
            raise ValidationError(detail="This is not a valid size")
        return size
    
    def validate_demurage_type(self, data):
        choice = ("import", "export")
        if data.lower() not in choice:
            raise ValidationError(detail="Choices are either 'import' or 'export'")
        
        return data.lower()
    
    
    
# class SendEmailSerializer(serializers.Serializer):
#     container_type = serializers.CharField(max_length=250)
#     start_date =  serializers.CharField(max_length=250)  
#     chargeable_days = serializers.CharField(max_length=250)
#     amount =  serializers.CharField(max_length=250)
#     vat_amount = serializers.CharField(max_length=250)
#     total =  serializers.CharField(max_length=250)
#     currency = serializers.CharField(max_length=250)
    
    