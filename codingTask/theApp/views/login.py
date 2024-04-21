from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from theApp.serializers.usersSerializer import LoginSerializer
from theApp.models.users import RegisteredUser
from django.contrib.auth import login, logout
from rest_framework import status


@api_view(['POST', ])
@permission_classes([AllowAny])
def login_view(request) :
    data = request.data
    deserialized = LoginSerializer(data = data)

    if deserialized.is_valid() :
        phone_number = deserialized.data['phone_number']
        password = deserialized.data['password']

        try :
            user = RegisteredUser.objects.get(phone_number = phone_number)
            stored_password = user.password
            
            if(check_password(password, stored_password)) :
                
                token = Token.objects.get_or_create(user = user)
                login(request, user)
                
                return Response({
                    'message': 'Login successful',
                },
                status = status.HTTP_200_OK
                )
            
            else :
                return Response({
                    'message': 'Invalid password.',
                },
                status = status.HTTP_403_FORBIDDEN
                )

        except Exception as e :
            return Response({
                'message': 'User does not exist.',
                'Exception': str(e)
            },
            status = status.HTTP_403_FORBIDDEN
            )
        
    else :
        return Response({
            'Message': 'Something went wrong.',
            'error(s)': deserialized.errors
        },
        status = status.HTTP_403_FORBIDDEN
        )
    

@api_view(['POST', ])
@permission_classes([IsAuthenticated])
def logout_view(request):

    request.user.auth_token.delete()
    
    logout(request)
    
    return Response({
        'Message': 'User logged out successfully.'
    },
    status = status.HTTP_200_OK
    )
