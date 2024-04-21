from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from theApp.models.spam import Spam
from theApp.serializers.spamSerializer import SpamSerializer
from rest_framework import status


@api_view(['POST', ])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def report_spam_view(request) :
    data = request.data
    deserialized = SpamSerializer(data = data)

    if deserialized.is_valid() :
        phone_number = deserialized.data['phone_number']
        
        if Spam.objects.filter(phone_number = phone_number) :
            user = Spam.objects.get(phone_number = phone_number)
            user.spam_reported_count = user.spam_reported_count + 1
            user.save()

        else :
            Spam.objects.create(
                phone_number = phone_number,
                spam_reported_count = 1
            )

        return Response({
            'message': f'Number: {phone_number} is reported as spam.',
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


@api_view(['GET', ])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_all_spam_view(request) :
    all_spams = Spam.objects.all()
    serialized = SpamSerializer(all_spams, many = True)
    return Response({
        'All Spam Numbers': serialized.data
    },
    status = status.HTTP_200_OK
    )
