from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from theApp.serializers.usersSerializer import RegisteredUserSerializer
from rest_framework import status


@api_view(['POST', ])
@permission_classes([AllowAny])
def signup_view(request) :
    data = request.data
    deserialized = RegisteredUserSerializer(data = data)

    if deserialized.is_valid() :
        deserialized.validated_data['password'] = make_password(deserialized.validated_data['password'])
        deserialized.save()
        return Response(
            {
                'Message' : f'User created successfully.',
                'Name': deserialized.data['name'],
                'Phone Number': deserialized.data['phone_number'],
                'Email': deserialized.data['email']
            },
            status = status.HTTP_200_OK
            )
    
    else :
        return Response({
            'message': 'Something went wrong.',
            'error(s)': deserialized.errors
        },
        status = status.HTTP_403_FORBIDDEN
        )
    