from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from django.contrib.auth import logout

class LoginAPIView(APIView):

    def post(self, request):

        username = request.data.get("username")
        password = request.data.get("password")


        user = authenticate(
            request=request,
            username=username,
            password=password
        )


        if user is None:

            return Response(
                {
                    "success": False,
                    "message": "Invalid credentials"
                },
                status=status.HTTP_401_UNAUTHORIZED
            )


        return Response(
            {
                "success": True,
                "message": "Login successful",
                "user": UserSerializer(user).data
            },
            status=status.HTTP_200_OK
        )





class ProfileAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def get(self, request):

        return Response(
            {
                "success": True,
                "user": UserSerializer(request.user).data
            },
            status=status.HTTP_200_OK
        )




class LogoutAPIView(APIView):

    def post(self, request):

        logout(request)

        return Response(
            {
                "success": True,
                "message": "Logout successful"
            },
            status=status.HTTP_200_OK
        )