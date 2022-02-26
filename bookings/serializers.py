from rest_framework import serializers
from .models import Booking
from rest_framework.exceptions import ValidationError



class BookingSerializer(serializers.ModelSerializer):
    shipping_company_detail = serializers.ReadOnlyField()
    bay_area_detail = serializers.ReadOnlyField()
    
    class Meta:
        model = Booking
        fields = '__all__'
        
        
class BookingCompleteSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6)
    
    
    def verify(self):
        try:
            booking = Booking.objects.get(drop_off = self.validated_data['code'], is_active=True)
        except Booking.DoesNotExist:
            raise ValidationError({"message": "Invalid Code"})
        
        except Exception:
            raise ValidationError({"message": "Unable to verify please contact support."})
        
        booking:Booking
        if booking.status == "pending":
            booking.status = "completed"
            booking.save()
            
            booking.bay_area.available_space +=1
            booking.bay_area.save()
            
            return {"message": "Booking Completed"}
        else:
            raise ValidationError({"message": "Code already used."})
        