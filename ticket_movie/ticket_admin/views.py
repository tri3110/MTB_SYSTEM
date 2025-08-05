from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ticket_movie.app.serializers import CinemaSerializer, MovieSerializer, ScreenSerializer, SeatSerializer, ShowtimeSerializer
from ticket_movie.models import Booking, BookingSeat, Cinema, City, Movie, Screen, Seat, Showtime, User

class CinemaView(APIView):
    
    def get(self, request):
        cinemas = Cinema.objects.all().order_by('-id')
        serializer = CinemaSerializer(cinemas, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = CinemaSerializer(data=request.data)
        if serializer.is_valid():
            cinema = serializer.save()
            return Response({
                'cinema': CinemaSerializer(cinema).data,
                'message': "Cinema created successfully"
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, id):
        try:
            with transaction.atomic():
                cinema = Cinema.objects.select_for_update().get(id=id)

                serializer = CinemaSerializer(cinema, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({
                        'cinema': serializer.data,
                        'message': "Cinema updated successfully"
                    }, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Cinema.DoesNotExist:
            return Response({'message': 'Cinema not found'}, status=status.HTTP_404_NOT_FOUND)
        
    def delete(self, request, id):
        try:
            cinema = Cinema.objects.get(id=id)
            cinema.delete()
            return Response({'message': 'Cinema deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Cinema.DoesNotExist:
            return Response({'message': 'Cinema not found'}, status=status.HTTP_404_NOT_FOUND)

class ScreenView(APIView):
    
    def get(self, request):
        screens = Screen.objects.select_related('cinema').order_by('-id')
        serializer = ScreenSerializer(screens, many=True)
        cinemas = Cinema.objects.all().order_by('-id')
        cinemas_serializer = CinemaSerializer(cinemas, many=True)
        return Response({
            "screens": serializer.data,
            "cinemas": cinemas_serializer.data,
        })
    
    def post(self, request):
        try:
            serializer = ScreenSerializer(data=request.data)
            if serializer.is_valid():
                screen = serializer.save()
                
                seats_data = request.data.get("seats", [])
                for seat in seats_data:
                    Seat.objects.create(
                        screen=screen,
                        row=seat["row"],
                        number=seat["number"],
                        type=seat.get("type", "standard"),
                        is_active=seat.get("is_active", False)
                    )
                
                return Response({
                    'screen': ScreenSerializer(screen).data,
                    'message': "Screen created successfully"
                }, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
        except:
            return Response({'message': 'Screen error'})
        
    def put(self, request, id):
        try:
            with transaction.atomic():
                data = request.data
                screen = Screen.objects.select_for_update().get(id = id)
                serializer = ScreenSerializer(screen, data=data, partial=True)
                if serializer.is_valid():
                    screen = serializer.save()
                    
                    seat_data = data.get("seats", [])
                    for seat in seat_data:
                        seat_temp = Seat.objects.select_for_update().get(id = seat.get("id"))
                        seat_temp.is_active = seat.get("is_active", seat_temp.is_active)
                        seat_temp.type = seat.get("type", seat_temp.type)
                        seat_temp.save()
                    
                    return Response({
                        'screen': ScreenSerializer(screen).data,
                        'message': "Screen update successfully"
                    }, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
        except:
            return Response({'message': 'Update error'})
    
    def delete(self, request, id):
        try:
            screen = Screen.objects.get(id=id)
            screen.delete()
            return Response({'message': 'Screen deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({'message': 'Delete error'})
        
class MovieView(APIView):
    
    def post(self, request):
        data = request.data
        serializer = MovieSerializer(data=data)
        if serializer.is_valid():
            movie = serializer.save()
            return Response({
                'movie': MovieSerializer(movie).data,
                'message': "Movie created successfully"
                }, status=status.HTTP_200_OK
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, id):
        data = request.data
        try:
            with transaction.atomic():
                movie = Movie.objects.select_for_update().get(id = id)
                serializer = MovieSerializer(movie, data=data, partial=True)
                if serializer.is_valid():
                    movie = serializer.save()
                    return Response({
                        'movie': MovieSerializer(movie).data,
                        'message': "Movie update successfully"
                    }, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
        except:
            return Response({'message': 'Update error'})
        
    def delete(self, request, id):
        try:
            with transaction.atomic():
                movie = Movie.objects.select_for_update().get(id = id)
                movie.status = "ended"
                movie.save()

                return Response({
                    'message': "Movie delete successfully"
                }, status=status.HTTP_201_CREATED)
                
        except:
            return Response({'message': 'Delete error'})
        
class ShowtimeView(APIView):
    
    def post(self, request):
        data = request.data
        serializer = ShowtimeSerializer(data=data)
        if serializer.is_valid():
            showtime = serializer.save()
            return Response({
                'showtime': ShowtimeSerializer(showtime).data,
                'message': "Showtime created successfully"
                }, status=status.HTTP_200_OK
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, id):
        data = request.data
        try:
            with transaction.atomic():
                showtime = Showtime.objects.select_for_update().get(id = id)
                serializer = ShowtimeSerializer(showtime, data=data, partial=True)
                if serializer.is_valid():
                    showtime = serializer.save()
                    return Response({
                        'showtime': ShowtimeSerializer(showtime).data,
                        'message': "Showtime update successfully"
                    }, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
        except:
            return Response({'message': 'Update error'})
        
    def delete(self, request, id):
        try:
            with transaction.atomic():
                showtime = Showtime.objects.select_for_update().get(id = id)
                showtime.status = "cancelled"
                showtime.save()

                return Response({
                    'message': "Showtime delete successfully"
                }, status=status.HTTP_201_CREATED)
                
        except:
            return Response({'message': 'Delete error'})
        
class SeatView(APIView):
    
    def get(self, request, screen_id):
        seat = Seat.objects.filter(screen_id = screen_id)
        serializer = SeatSerializer(seat, many=True)
        return Response(serializer.data)