from rest_framework import mixins, status
from rest_framework.views import APIView
from rest_framework.response import Response

from crowdbotics_test.animal.exceptions.response import ExceptionResponse
from .serializers import CatSerializer, DogSerializer
from .exceptions import InvalidSerializerDataException
from .models import Cat, Dog


class Animal(mixins.ListModelMixin, APIView):

    def get(self, request):
        try:
            query_params = request.query_params
            animal_type = query_params.get("type", None)
            data = None
            if animal_type == "cat":
                cats = Cat.objects.all()
                data = CatSerializer(cats, many=True).data
            elif animal_type == "dog":
                dogs = Dog.objects.all()
                data = DogSerializer(dogs, many=True).data
            else:
                raise Exception("Invalid animal type")
            return Response(data=data)
        except (InvalidSerializerDataException, Exception) as ex:
            return ExceptionResponse.get(ex)

    def post(self, request):
        try:
            query_params = request.query_params
            data = request.data
            animal_type = query_params.get("type", None)
            if animal_type == "cat":
                serializer = CatSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                else:
                    raise InvalidSerializerDataException("Cat", serializer.errors)
            elif animal_type == "dog":
                serializer = DogSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                else:
                    raise InvalidSerializerDataException("Dog", serializer.errors)
            else:
                raise Exception("Invalid animal type")
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except (InvalidSerializerDataException, Exception) as ex:
            return ExceptionResponse.get(ex)

    def put(self, request):
        try:
            query_params = request.query_params
            data = request.data
            animal_type = query_params.get("type", None)
            _id = data.get("id", None)
            if animal_type == "cat":
                cat = Cat.objects.get(id=_id)
                serializer = CatSerializer(cat, data=data)
                if serializer.is_valid():
                    serializer.save()
                else:
                    raise InvalidSerializerDataException("Cat", serializer.errors)
            elif animal_type == "dog":
                dog = Dog.objects.get(id=_id)
                serializer = DogSerializer(dog, data=data)
                if serializer.is_valid():
                    serializer.save()
                else:
                    raise InvalidSerializerDataException("Dog", serializer.errors)
            else:
                raise Exception("Invalid animal type")
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except (InvalidSerializerDataException, Exception) as ex:
            return ExceptionResponse.get(ex)

    def delete(self, request):
        try:
            query_params = request.query_params
            animal_type = query_params.get("type", None)
            pk = query_params.get("id", None)
            if animal_type == "cat":
                Cat.objects.get(id=pk).delete()
            elif animal_type == "dog":
                Dog.objects.get(id=pk).delete()
            else:
                raise Exception("Invalid animal type")
            return Response(status=status.HTTP_200_OK)
        except (InvalidSerializerDataException, Exception) as ex:
            return ExceptionResponse.get(ex)
