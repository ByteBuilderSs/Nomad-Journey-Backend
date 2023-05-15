from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import City
from .serializers import CountrySerializer, CitySerializer


@api_view(['GET'])
def GetCountries(request):
    countries = City.objects.all().distinct('country')
    serializer = CountrySerializer(countries, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def GetCitiesOfCountry(request, rec_id):
    single_city = City.objects.get(id=rec_id)
    cities = City.objects.filter(country=single_city.country)
    serializer = CitySerializer(cities, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def GetAllCities(request):
    cities = City.objects.all()
    serializer = CitySerializer(cities[:5000], many=True)
    return Response(serializer.data)

@api_view(['POST'])
def CreateCity(request):
    serializer = CitySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)