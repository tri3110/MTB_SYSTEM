from rest_framework import serializers
from ticket_movie.models import Cinema, City, Movie, Screen, Seat, Showtime
from datetime import date, datetime
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

class MovieSerializer(serializers.ModelSerializer):
    poster_url = serializers.CharField()
    
    class Meta:
        model = Movie
        fields = [
            'id',
            'title',
            'description',
            'duration',
            'release_date',
            'genre',
            'director',
            'movie_cast',
            'poster_url',
            'trailer_url',
            'rating',
            'status',
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'title': {'required': True},
            'director': {'required': True},
            'movie_cast': {'required': True},
            'poster_url': {'required': True},
            'trailer_url': {'required': True},
            'rating': {'read_only': True},
        }

    def validate_duration(self, value):
        if value <= 0:
            raise serializers.ValidationError("Thời lượng phim phải lớn hơn 0 phút.")
        return value

    def validate_release_date(self, value):
        if value < date(1900, 1, 1):
            raise serializers.ValidationError("Ngày phát hành không hợp lệ.")
        return value
    
class CitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = [
            'id',
            'name',
            'country',
        ]
        extra_kwargs = {
            'country': {'read_only': True}, 
        }
        
class CinemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cinema
        fields = '__all__'
        extra_kwargs = {
            'name': {'required': True},
            'address': {'required': True},
            'phone': {'required': True}
        }
    
    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Please enter cinema name")
        return value
    
    def validate_address(self, value):
        if not value.strip():
            raise serializers.ValidationError("Please enter cinema address")
        return value
    
    def validate_phone(self, value):
        if not value.strip() or len(value) < 10:
            raise serializers.ValidationError("Please enter cinema phone number with at least 10 digits.")
        return value
    
class ScreenSerializer(serializers.ModelSerializer):
    
    cinema = CinemaSerializer(read_only=True)
    cinema_id = serializers.PrimaryKeyRelatedField(
        queryset=Cinema.objects.all(),
        write_only=True,
        source='cinema'
    )
    
    class Meta:
        model = Screen
        fields = '__all__'
        extra_kwargs = {
            'name': {'required': True},
            'type': {'required': True},
            'capacity': {'required': True}
        }
    
    def validate_type(self, value):
        if len(value) > 20:
            raise serializers.ValidationError("Please enter cinema type with at most 20")
        return value
    
    def validate_capacity(self, value):
        if value < 1:
            raise serializers.ValidationError("Please enter cinema capacity number with at least 1 digits.")
        return value

class ShowtimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Showtime
        fields = '__all__'
        extra_kwargs = {
            'start_time': {'required': True},
            'end_time': {'required': True},
            'base_price': {'required': True},
            'available_seats': {'required': True},
            'status': {'required': True},
            'movie': {'required': True},
            'screen': {'required': True}
        }
    
    def validate(self, data):
        try:
            start_time = data.get("start_time")
            end_time = data.get("end_time")

            if isinstance(start_time, str):
                start_time = datetime.fromisoformat(start_time)

            if isinstance(end_time, str):
                end_time = datetime.fromisoformat(end_time)

            if start_time >= end_time:
                raise serializers.ValidationError("End time must be after start time.")
        except Exception:
            raise serializers.ValidationError("Invalid date format. Use ISO format: YYYY-MM-DDTHH:MM:SS±HH:MM")
        
        return data
    
class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = [
            'id',
            'row',
            'number',
            'type',
            'is_active',
        ]