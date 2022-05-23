from rest_framework import serializers
from main.models import ShippingCompany
from .models import Demurage, DemurageSize
from rest_framework.exceptions import ValidationError


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemurageSize
        fields = '__all__'
        
class DemurageSerializer(serializers.ModelSerializer):
    shipping_company_detail = serializers.ReadOnlyField()
    size_detail = serializers.ReadOnlyField()
    class Meta:
        model = Demurage
        fields = '__all__'
        write_only_fields = ['shipping_company', 'size']
        
        
    def validate_size(self, data):
        if data is not None:
            try:
                data = DemurageSize.objects.get(id=data)
            except DemurageSize.DoesNotExist:
                raise ValidationError(["Enter a valid size ID"])
        raise ValidationError(["This field cannot be null"])
        
        
class CalculatorSerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    shipping_company = serializers.UUIDField()
    size = serializers.CharField(max_length=255)
    
    def validate_shipping_company(self, data):
        try:
            company = ShippingCompany.objects.get(id=data, is_active=True)
        except ShippingCompany.DoesNotExist:
            raise ValidationError(detail="shipping company does not exist")
        return company
    
    def validate_size(self, data):
        sizes = ("20 feet", "40 feet")
        
        if data not in sizes:
            raise ValidationError(detail=f"Size must be either of {sizes}")
        
        return data