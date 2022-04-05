from rest_framework import serializers
from accounts.helpers.generators import generate_code

from main.models import BayArea, ShippingCompany
from .models import Booking
from rest_framework.exceptions import ValidationError

from accounts.models import User


class BookingSerializer(serializers.ModelSerializer):
    shipping_company_detail = serializers.ReadOnlyField()
    bay_area_detail = serializers.ReadOnlyField()
    
    class Meta:
        model = Booking
        fields = '__all__'
        
        

class BookingDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["date","laden_number", "container_number","container_size"]
        

class AddBookingSerializer(serializers.Serializer):
    shipping_company = serializers.UUIDField()
    bay_area = serializers.UUIDField()
    containers = BookingDetailSerializer(many=True)
    
    def validate(self, attr):
        error = {}
        valid = True
        try:
            company = ShippingCompany.objects.get(id=attr['shipping_company'], is_active=True)
            attr['shipping_company'] = company
        except ShippingCompany.DoesNotExist:
            error['shipping_company'] = "This company does not exist"
            valid=False
        
        try:
            bay = BayArea.objects.get(id=attr['bay_area'],shipping_company=attr['shipping_company'] ,is_active=True)
            
            attr['bay_area'] = bay
        except BayArea.DoesNotExist:
            error['bay_area'] = "This holding bay does not exist for the selected shipping company."
            valid=False
        
        if valid:
            return attr
        else:
            raise ValidationError(detail=error, code=400)
        
        
    
    def create(self, validated_data, request):
  
        shipping_company = validated_data.pop('shipping_company')
        bay_area = validated_data.pop("bay_area")
        containers = validated_data.pop('containers')
        
        total_containers = len(containers)
        
        if total_containers > bay_area.available_space:
            raise ValidationError({"message":"Available space not sufficient for your containers."})
        
        bookings = []
        for container in containers :
            bookings.append(Booking(**container, user=request.user,shipping_company=shipping_company, bay_area=bay_area, drop_off=generate_code(6)))
        
        Booking.objects.bulk_create(bookings)
        bay_area.available_space-=total_containers
        bay_area.save()
        
        return {"message": f"Successfully booked space for {total_containers} container(s)"}
            
            
        
        
        
            
        
class BookingCompleteSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6)
    
    
    def verify(self, request):
        try:
            booking = Booking.objects.get(drop_off = self.validated_data['code'], is_active=True, bay_area=request.user.bay_area, )
        except Booking.DoesNotExist:
            raise ValidationError({"message": "Invalid Code"})
        
        except Exception:
            raise ValidationError({"message": "Unable to verify please contact support."})
        
        booking:Booking
        if booking.status == "pending":
            booking.status = "completed"
            booking.save()
            serializer = BookingSerializer(booking)
            
            
            return {"message": "Booking Completed", 
                    'data':serializer.data}
        else:
            raise ValidationError({"message": "Code already used."})
        