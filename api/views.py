from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login

from organizations.models import Organization
from .serializers import UserManagementSerializer

from .serializers import OrganizationSerializer

from rest_framework.generics import RetrieveUpdateDestroyAPIView

from accounts.models import User, Role

from .permissions import has_admin_permission
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .serializers import (
    UserManagementSerializer,
    UserUpdateSerializer,
)

from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserStatusSerializer

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

        # Create Django session
        refresh = RefreshToken.for_user(user)

        return Response(
    {
        "success": True,
        "refresh": str(refresh),
        "access": str(refresh.access_token),
        "user": UserSerializer(user).data
    }
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



from django.contrib.auth import logout

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class LogoutAPIView(APIView):

    authentication_classes = []

    permission_classes = []


    def post(self, request):

        logout(request)

        return Response(
            {
                "success": True,
                "message": "Logout successful"
            },
            status=status.HTTP_200_OK
        )


class OrganizationListCreateAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def get(self, request):

        organizations = Organization.objects.filter(
            id=request.user.organization.id
        )


        serializer = OrganizationSerializer(
            organizations,
            many=True
        )


        return Response(
            {
                "success": True,
                "organizations": serializer.data
            }
        )


    def post(self, request):

        serializer = OrganizationSerializer(
            data=request.data
        )


        if serializer.is_valid():

            organization = serializer.save()


            return Response(
                {
                    "success": True,
                    "organization": OrganizationSerializer(
                        organization
                    ).data
                },
                status=status.HTTP_201_CREATED
            )


        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class OrganizationDetailAPIView(
    RetrieveUpdateDestroyAPIView
):

    serializer_class = OrganizationSerializer

    permission_classes = [
        IsAuthenticated
    ]


    def get_queryset(self):

        return Organization.objects.filter(
            id=self.request.user.organization.id
        )

class UserListAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def get(self, request):

        users = User.objects.filter(
            organization=request.user.organization
        )


        serializer = UserManagementSerializer(
            users,
            many=True
        )


        return Response(
            {
                "success": True,
                "users": serializer.data
            },
            status=status.HTTP_200_OK
        )

class UserDetailAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def get_object(self, request, pk):

        try:

            return User.objects.get(
                id=pk,
                organization=request.user.organization
            )

        except User.DoesNotExist:

            return None


    def get(self, request, pk):

        user = self.get_object(
            request,
            pk
        )


        if not user:

            return Response(
                {
                    "error": "User not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )


        serializer = UserManagementSerializer(
            user
        )


        return Response(
            {
                "success": True,
                "user": serializer.data
            },
            status=status.HTTP_200_OK
        )



class UserUpdateAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def patch(self, request, pk):

        # Check Owner/Admin permission

        if not has_admin_permission(
            request.user
        ):

            return Response(
                {
                    "success": False,
                    "error": "Permission denied"
                },
                status=status.HTTP_403_FORBIDDEN
            )


        # Tenant isolation

        try:

            user = User.objects.get(
                id=pk,
                organization=request.user.organization
            )


        except User.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "error": "User not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )


        # Prevent Admin from modifying Owner

        if (
            user.role
            and user.role.name.lower() == "owner"
            and request.user.role.name.lower() == "admin"
        ):

            return Response(
                {
                    "success": False,
                    "error": "Admin cannot modify Owner"
                },
                status=status.HTTP_403_FORBIDDEN
            )


        # Prevent Admin from assigning Owner role

        if "role" in request.data:

            new_role_id = request.data.get(
                "role"
            )


            try:

                new_role = Role.objects.get(
                    id=new_role_id
                )


            except Role.DoesNotExist:

                return Response(
                    {
                        "success": False,
                        "error": "Invalid role"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )


            if (
                request.user.role.name.lower()
                == "admin"
                and new_role.name.lower()
                == "owner"
            ):

                return Response(
                    {
                        "success": False,
                        "error": "Admin cannot assign Owner role"
                    },
                    status=status.HTTP_403_FORBIDDEN
                )


        # Update user

        serializer = UserUpdateSerializer(
            user,
            data=request.data,
            partial=True
        )


        if serializer.is_valid():

            serializer.save()


            return Response(
                {
                    "success": True,
                    "message": "User updated successfully",
                    "user": UserManagementSerializer(
                        user
                    ).data
                },
                status=status.HTTP_200_OK
            )


        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class UserStatusAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def patch(self, request, pk):

        # Owner/Admin permission check

        if not has_admin_permission(request.user):

            return Response(
                {
                    "success": False,
                    "error": "Permission denied"
                },
                status=status.HTTP_403_FORBIDDEN
            )


        # Tenant isolation

        try:

            user = User.objects.get(
                id=pk,
                organization=request.user.organization
            )


        except User.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "error": "User not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )


        # Protect Owner account

        if (
            user.role
            and user.role.name.lower() == "owner"
        ):

            return Response(
                {
                    "success": False,
                    "error": "Owner cannot be deactivated"
                },
                status=status.HTTP_403_FORBIDDEN
            )


        serializer = UserStatusSerializer(
            user,
            data=request.data,
            partial=True
        )


        if serializer.is_valid():

            serializer.save()


            return Response(
                {
                    "success": True,
                    "message": "User status updated successfully",
                    "user": UserManagementSerializer(user).data
                },
                status=status.HTTP_200_OK
            )


        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )