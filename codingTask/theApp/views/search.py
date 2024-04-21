from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from theApp.models.users import RegisteredUser, Contact
from theApp.models.spam import Spam
from rest_framework import status


@api_view(['POST', ])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def search_by_name_view(request) :
    data = request.data

    try :
        query_name = data.get('name')
        if query_name is None :
            return Response({
                'Message': 'Name is required.'
            },
            status = status.HTTP_400_BAD_REQUEST
            )

        # To retrieve contacts whose names start with the search query
        contact_starts_with_results = Contact.objects.filter(name__istartswith = query_name)
        # To retrieve contacts whose names contain but don't start with the search query
        contact_contains_results = Contact.objects.filter(name__icontains = query_name).exclude(name__istartswith = query_name)
        
        # To retrieve registered users whose names start with the search query
        registered_user_starts_with_results = RegisteredUser.objects.filter(name__istartswith = query_name)
        # To retrieve registered users whose names contain but don't start with the search query
        registered_user_contains_results = RegisteredUser.objects.filter(name__icontains = query_name).exclude(name__istartswith = query_name)

        # To combine all result sets
        search_results = list(registered_user_starts_with_results) + list(contact_starts_with_results) + list(registered_user_contains_results) + list(contact_contains_results)
        
        # Sort the combined results based on the requirement
        search_results.sort(key = lambda x: (not x.name.startswith(query_name), x.name))

        serialized_results = []

        # To get spam likelihood for each search result
        for result in search_results:
            spam_likelihood = Spam.objects.filter(phone_number = result.phone_number).first()
            
            if spam_likelihood is not None :
                spam_likelihood_count = spam_likelihood.spam_reported_count
            else:
                spam_likelihood_count = 0

            serialized_result = {
                'name': result.name,
                'phone_number': result.phone_number,
                'spam_likelihood (number of times this number is reported as a spam)': spam_likelihood_count
            }

            # To check whether the user who is searching is in registered_user's contact list or not.
            if isinstance(result, RegisteredUser):
                is_contact = result.contacts.filter(phone_number = request.user.phone_number).exists()
                if is_contact : 
                    serialized_result['email'] = result.email

            serialized_results.append(serialized_result)
                
        result = {
            'query_name': query_name,
            'search_results': serialized_results if len(serialized_results) > 0 else 'No matching results found.'
        }
        return Response({
            'Results': result
        },
        status = status.HTTP_200_OK
        )
    
    except Exception as e :
        return Response({
            'Message': 'An exception occured',
            'Exception': str(e)
        })


@api_view(['POST', ])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def search_by_number_view(request) :
    data = request.data
    
    try :
        query_number = data.get('phone_number')
        if query_number is None :
            return Response({
                'Message': 'Phone number is required.'
            },
            status = status.HTTP_400_BAD_REQUEST
            )
        
        # To search if there is a registered user with the provided phone number or not
        registered_user = RegisteredUser.objects.filter(phone_number = query_number).first()

        # If a registered user exists
        if registered_user is not None :
            
            # To get spam likelihood
            spam_likelihood = Spam.objects.filter(phone_number = registered_user.phone_number).first()
            if spam_likelihood is not None :
                spam_likelihood_count = spam_likelihood.spam_reported_count
            else:
                spam_likelihood_count = 0

            # To check whether the user who is searching is in registered_user's contact list or not.
            is_contact = registered_user.contacts.filter(id = request.user.id).exists()

            if is_contact :
                serialized_result = {
                    'name': registered_user.name,
                    'phone_number': registered_user.phone_number,
                    'email': registered_user.email,
                    'spam_likelihood (number of times this number is reported as a spam)': spam_likelihood_count
                }

            else :
                serialized_result = {
                    'name': registered_user.name,
                    'phone_number': registered_user.phone_number,
                    'spam_likelihood (number of times this number is reported as a spam)': spam_likelihood_count
                }

            result = {
                'query_name': query_number,
                'search_results': serialized_result
            }

            return Response({
                'Results': result
            },
            status = status.HTTP_200_OK
            )
        
        # If a registered user does not exist
        else :
            contacts = Contact.objects.filter(phone_number = query_number)
            if contacts.exists() :
                
                serialized_results = []

                for contact in contacts :
                    spam_likelihood = Spam.objects.filter(phone_number = contact.phone_number).first()
            
                    if spam_likelihood is not None :
                        spam_likelihood_count = spam_likelihood.spam_reported_count
                    else:
                        spam_likelihood_count = 0

                    serialized_result = {
                        'name': contact.name,
                        'phone_number': contact.phone_number,
                        'spam_likelihood (number of times this number is reported as a spam)': spam_likelihood_count
                    }

                    serialized_results.append(serialized_result)

                result = {
                    'query_name': query_number,
                    'search_results': serialized_results
                }
            
                return Response({
                    'Results': result
                },
                status = status.HTTP_200_OK
                )
            
            else :
                result = {
                    'query_name': query_number,
                    'search_results': 'No matching results found.'
                }
                
                return Response({
                    'Results': result
                },
                status = status.HTTP_200_OK
                )

    except Exception as e :
        return Response({
            'Message': 'An exception occured',
            'Exception': str(e)
        })
