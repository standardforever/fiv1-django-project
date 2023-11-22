from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, HistorySerializer
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .models import User, History
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def room(request):
    return render(request, "room.html")

# Create your views here.
@api_view(['POST'])
def register_user(request):
    """ Endpoint where user can register
    """
    data = {"first_name": "admin", "last_name": "admin", "username": "admin", "password": "admin"}
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        new_user = {"first_name": serializer.data.get('first_name'), 'last_name': serializer.data.get('last_name'), "email": serializer.data.get('username')} 


    if request.method == 'POST':
        try:
            User.objects.get(first_name=request.data.get('first_name'))
            return Response({'error': 'User with these Name Already Exits'}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            pass

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            new_user = {"first_name": serializer.data.get('first_name'), 'last_name': serializer.data.get('last_name'), "email": serializer.data.get('username')}
            return Response(new_user, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def user_login(request):
    """ Login Endpoint, where users get there token
    """
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        # Check if it is a valid email address
        if '@' in username:
            try:
                User.objects.get(username=username)
            except ObjectDoesNotExist:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        authenticated_user = authenticate(username=username, password=password)

        if authenticated_user:
            token, _ = Token.objects.get_or_create(user=authenticated_user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    """ Endpoint where user logout
    """
    if request.method == 'POST':
        try:
            request.user.auth_token.delete()
            return Response({'message': "Successfully logged out"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 1- User (Signup and sign in authentication with django ready model, create user "email, password required", if user has account login "check if username, passowrd are in database" )
# 2- Letters (capacity can select up to four letters max "we have 9 letters from a to e some of letters can repeated",word is formed from the selected letters, letters capacity updated after every order) 
# 3- Words (the selected letters constitute the word, word must be kept according to the arrangement in which the letters were chosen)
# 4- Location (location of the letter on the transport belt) 
# 5- Order (if the user has an account and he signin then the order is done after checking if the required letters are available and update the capacity after every order)
# 6- ErrorLog (If the user makes a order and the number of remaining characters is not enough to complete the order, then an error message is sent showing which character is not available) 
# 7- Orders history (as a record with username letters word error date)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def order_history(request):
    """ TO save the record
    """
    if request.method == 'POST':
        user = User.objects.get(username = 'admin')
        response = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0, 'I': 0}
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
        history = {}
        word = request.data.get('word')

        history['word'] = word
        history['user']= request.user.id
        history['user_name'] = request.user.username
        
        serializer = HistorySerializer(data=history)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

        for i in word:
            # Check if the letters are correct
            if i not in letters:
                history["is_error"] = True
                history["error"] = "Letter '{}' not allow".format(i)
                return Response({'error': "These letter '{}' is not allowed".format(i)}, status=status.HTTP_400_BAD_REQUEST)
            
            # Check if there is still available capacity for the selecte letters
            count = getattr(user, i)
            if (count - 1 < 0):
                history["is_error"] = True
                history["error"] = "No enough '{}' to complete the Order".format(i)
                return Response({'error': "You don't have enough '{}' to complete the Order".format(i)})
            setattr(user, i, count - 1)
            response[i] = response[i] + 1

        # Update the user record
        serializer = HistorySerializer(data=history)
        if serializer.is_valid():
            serializer.save()
            user.save()

            channel_layer = get_channel_layer()

            # Define the message you want to send
            test_message = "This is a test message from the HTTP view!"

            # Send the message to the "raspberry_pi_group" WebSocket group
            async_to_sync(channel_layer.group_send)(
                "raspberry_pi",
                {
                    "type": "raspberry_pi.message",
                    "message": response
                }
            )
    
            return Response({"success": True}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

