from rest_framework import serializers
from .models import Subscribe, Workshops, Governorates, Zones, Cars, Specializations, Crafts, Contacts, Images, Comments, Rates
from django.db.models import Avg

class SubscribeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Subscribe
        fields = '__all__'


class GovernoratesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Governorates
        fields = ('id', 'governorate')


class ZonesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Zones
        fields = ('id', 'zone')


class CarsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Cars
        fields = ('id', 'model_name')


class SpecializationssSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Specializations
        fields = ('id', 'specialization')


class CraftsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Crafts
        fields = ('id', 'craft')


class ContactsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Contacts
        fields = ('number', 'num_type')


class ImagesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Images
        fields = ('image',)


class RatesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Rates
        fields = ('rate',)


class WorkshopsSerializer(serializers.ModelSerializer):

    governorate = GovernoratesSerializer()
    zone = ZonesSerializer()
    cars = CarsSerializer(many=True)
    specializations = SpecializationssSerializer(many=True)
    crafts = CraftsSerializer(many=True)
    contacts = ContactsSerializer(many=True)
    images = ImagesSerializer(many=True)

    rates_number = serializers.SerializerMethodField()
    rates_value = serializers.SerializerMethodField()

    class Meta:
        model = Workshops
        fields = (
            'id', 
            'name', 
            'owner', 
            'address', 
            'location', 
            'notes', 
            'governorate', 
            'zone', 
            'cars', 
            'specializations', 
            'crafts', 
            'contacts', 
            'images', 
            'comments',
            'rates_number',
            'rates_value'
        )
    
    def get_rates_number(self, obj):
        return obj.rates.count()

    def get_rates_value(self, obj):
        value = obj.rates.aggregate(avg=Avg('rate'))['avg']
        if value:
            return int(value)
        else:
            return 0

