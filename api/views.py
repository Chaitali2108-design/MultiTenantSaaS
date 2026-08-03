from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
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
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from .serializers import UserStatusSerializer
from .serializers import RoleSerializer
from .serializers import RoleCreateSerializer
from accounts.utils import assign_default_permissions
from .serializers import RoleUpdateSerializer
from accounts.models import Permission
from .serializers import PermissionSerializer
from .serializers import RolePermissionSerializer
from rest_framework.permissions import AllowAny
from .permissions import IsAdminOrOwner
from .permissions import HasOrganization
from .response import (
    success_response,
    error_response,
)

from accounts.models import UserProfile

from .serializers import ProfileImageSerializer

from .serializers import OrganizationLogoSerializer

class LoginAPIView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(
            request=request,
            username=username,
            password=password
        )

        if user is None:
            return error_response(
                "Invalid credentials",
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        # Create Django session
        refresh = RefreshToken.for_user(user)

        return Response(
            
            {
        "success": True,
        "refresh": str(refresh),
        "access": str(refresh.access_token),
        "user": UserSerializer(user).data
            },
            status=status.HTTP_200_OK

)




class ProfileAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def get(self, request):

        return success_response(
            "Profile fetched successfully",
            UserSerializer(request.user).data
    )



from django.contrib.auth import logout

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class LogoutAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def post(self, request):

        refresh_token = request.data.get(
            "refresh"
        )


        if not refresh_token:

            return Response(
                {
                    "success": False,
                    "error": "Refresh token required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )


        try:

            token = RefreshToken(
                refresh_token
            )


            token.blacklist()


            return success_response(
            "Logout successful"
            )


        except TokenError:

            return Response(
                {
                    "success": False,
                    "error": "Invalid token"
                },
                status=status.HTTP_400_BAD_REQUEST
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


        return success_response(
            "Users fetched successfully",
            serializer.data
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

            return error_response(
                "User not found",
                status_code=status.HTTP_404_NOT_FOUND
            )


        serializer = UserManagementSerializer(
            user
        )


        return success_response(
            "User fetched successfully",
            serializer.data
        )



class UserUpdateAPIView(APIView):

    permission_classes = [
        HasOrganization,
        IsAdminOrOwner
    ]


    def patch(self, request, pk):

        # Check Owner/Admin permission

        if not has_admin_permission(
            request.user
        ):

            return error_response(
                "Permission denied",
                status_code=status.HTTP_403_FORBIDDEN
            )


        # Tenant isolation

        try:

            user = User.objects.get(
                id=pk,
                organization=request.user.organization
            )


        except User.DoesNotExist:

            return error_response(
                "User not found",
                status_code=status.HTTP_404_NOT_FOUND
            )
            


        # Prevent Admin from modifying Owner

        if (
            user.role
            and user.role.name.lower() == "owner"
            and request.user.role.name.lower() == "admin"
        ):

            return error_response(
                "Admin cannot modify Owner",
                status_code=status.HTTP_403_FORBIDDEN
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


            return success_response(
                "User updated successfully",
                UserManagementSerializer(user).data
            )


        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class UserStatusAPIView(APIView):

    permission_classes = [
        HasOrganization,
        IsAdminOrOwner
    ]


    def patch(self, request, pk):

        # Owner/Admin permission check

        if not has_admin_permission(request.user):

            return error_response(
                "Permission denied",
                status_code=status.HTTP_403_FORBIDDEN
    )


        # Tenant isolation

        try:

            user = User.objects.get(
                id=pk,
                organization=request.user.organization
            )


        except User.DoesNotExist:

            return error_response(
                "User not found",
                status_code=status.HTTP_404_NOT_FOUND
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


            return success_response(
                "User status updated successfully",
                UserManagementSerializer(user).data
            )


        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class UserRemoveAPIView(APIView):

    permission_classes = [
        HasOrganization,
        IsAdminOrOwner
    ]


    def delete(self, request, pk):

        # Owner/Admin permission

        if not has_admin_permission(request.user):

            return error_response(
                "Permission denied",
                status_code=status.HTTP_403_FORBIDDEN
        )


        # Tenant isolation

        try:

            user = User.objects.get(
                id=pk,
                organization=request.user.organization
            )


        except User.DoesNotExist:

            return error_response(
                "User not found",
                status_code=status.HTTP_404_NOT_FOUND
        )

        # Protect Owner

        if (
            user.role
            and user.role.name.lower() == "owner"
        ):

            return Response(
                {
                    "success": False,
                    "error": "Owner cannot be removed"
                },
                status=status.HTTP_403_FORBIDDEN
            )


        # Remove from organization

        user.organization = None
        user.is_active = False
        user.save()


        return success_response(
            "User removed successfully"
        )


class RoleListAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        roles = Role.objects.filter(
            organization=request.user.organization
        ).order_by("id")

        serializer = RoleSerializer(
            roles,
            many=True
        )

        return Response(
            {
                "success": True,
                "roles": serializer.data
            },
            status=status.HTTP_200_OK
        )


class RoleDetailAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request, pk):

        try:

            role = Role.objects.get(
                id=pk,
                organization=request.user.organization
            )

        except Role.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "error": "Role not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = RoleSerializer(role)

        return Response(
            {
                "success": True,
                "role": serializer.data
            },
            status=status.HTTP_200_OK
        )

class RoleCreateAPIView(APIView):

    permission_classes = [
        IsAdminOrOwner,
        HasOrganization
    ]

    def post(self, request):

        if not has_admin_permission(request.user):

            return Response(
                {
                    "success": False,
                    "error": "Permission denied"
                },
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = RoleCreateSerializer(
            data=request.data
        )

        if serializer.is_valid():

            # Prevent duplicate role names
            if Role.objects.filter(
                organization=request.user.organization,
                name__iexact=serializer.validated_data["name"]
            ).exists():

                return Response(
                    {
                        "success": False,
                        "error": "Role with this name already exists."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            role = serializer.save(
                organization=request.user.organization,
                is_system=False,
                is_editable=True,
            )

            assign_default_permissions(role)

            return Response(
                {
                    "success": True,
                    "message": "Role created successfully.",
                    "role": RoleSerializer(role).data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class RoleUpdateAPIView(APIView):

    permission_classes = [
        HasOrganization,
        IsAdminOrOwner
    ]

    def patch(self, request, pk):

        if not has_admin_permission(request.user):

            return Response(
                {
                    "success": False,
                    "error": "Permission denied"
                },
                status=status.HTTP_403_FORBIDDEN
            )

        try:

            role = Role.objects.get(
                id=pk,
                organization=request.user.organization
            )

        except Role.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "error": "Role not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if role.is_system:

            return Response(
                {
                    "success": False,
                    "error": "System roles cannot be modified"
                },
                status=status.HTTP_403_FORBIDDEN
            )

        new_name = request.data.get("name")

        if new_name:

            exists = Role.objects.filter(
                organization=request.user.organization,
                name__iexact=new_name,
            ).exclude(
                id=role.id
            ).exists()

            if exists:

                return Response(
                    {
                        "success": False,
                        "error": "Role with this name already exists."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        serializer = RoleUpdateSerializer(
            role,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                {
                    "success": True,
                    "message": "Role updated successfully.",
                    "role": RoleSerializer(role).data
                },
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class RoleDeleteAPIView(APIView):

    permission_classes = [
        HasOrganization,
        IsAdminOrOwner
    ]

    def delete(self, request, pk):

        if not has_admin_permission(request.user):

            return Response(
                {
                    "success": False,
                    "error": "Permission denied"
                },
                status=status.HTTP_403_FORBIDDEN
            )

        try:

            role = Role.objects.get(
                id=pk,
                organization=request.user.organization
            )

        except Role.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "error": "Role not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if role.is_system:

            return Response(
                {
                    "success": False,
                    "error": "System roles cannot be deleted"
                },
                status=status.HTTP_403_FORBIDDEN
            )

        if User.objects.filter(role=role).exists():

            return Response(
                {
                    "success": False,
                    "error": "Role is assigned to users and cannot be deleted"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        role.delete()

        return Response(
            {
                "success": True,
                "message": "Role deleted successfully."
            },
            status=status.HTTP_200_OK
        )

class PermissionListAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        if not has_admin_permission(request.user):

            return Response(
                {
                    "success": False,
                    "error": "Permission denied"
                },
                status=status.HTTP_403_FORBIDDEN
            )


        permissions = Permission.objects.all().order_by(
            "id"
        )


        serializer = PermissionSerializer(
            permissions,
            many=True
        )


        return Response(
            {
                "success": True,
                "permissions": serializer.data
            },
            status=status.HTTP_200_OK
        )


class RolePermissionUpdateAPIView(APIView):

    permission_classes = [
        HasOrganization,
        IsAdminOrOwner
    ]


    def patch(self, request, pk):


        if not has_admin_permission(request.user):

            return Response(
                {
                    "success": False,
                    "error": "Permission denied"
                },
                status=status.HTTP_403_FORBIDDEN
            )


        try:

            role = Role.objects.get(
                id=pk,
                organization=request.user.organization
            )


        except Role.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "error": "Role not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )



        if role.is_system:

            return Response(
                {
                    "success": False,
                    "error": "System role permissions cannot be modified"
                },
                status=status.HTTP_403_FORBIDDEN
            )



        serializer = RolePermissionSerializer(
            data=request.data
        )


        if serializer.is_valid():

            permission_ids = serializer.validated_data[
                "permissions"
            ]


            permissions = Permission.objects.filter(
                id__in=permission_ids
            )


            role.permissions.set(
                permissions
            )


            return Response(
                {
                    "success": True,
                    "message": "Role permissions updated successfully",
                    "role": RoleSerializer(role).data
                },
                status=status.HTTP_200_OK
            )


        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class TokenRefreshAPIView(APIView):

    permission_classes = [
        AllowAny
    ]

    def post(self, request):

        refresh_token = request.data.get(
            "refresh"
        )


        if not refresh_token:

            return Response(
                {
                    "success": False,
                    "error": "Refresh token required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )


        try:

            refresh = RefreshToken(
                refresh_token
            )


            return Response(
                {
                    "success": True,
                    "access": str(
                        refresh.access_token
                    )
                },
                status=status.HTTP_200_OK
            )


        except TokenError:

            return Response(
                {
                    "success": False,
                    "error": "Invalid refresh token"
                },
                status=status.HTTP_401_UNAUTHORIZED
            )


class ProfileImageUploadAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def patch(self, request):

        try:

            profile = request.user.profile


        except UserProfile.DoesNotExist:

            profile = UserProfile.objects.create(
                user=request.user
            )


        serializer = ProfileImageSerializer(
            profile,
            data=request.data,
            partial=True
        )


        if serializer.is_valid():

            serializer.save()


            return success_response(
                "Profile image updated successfully",
                serializer.data
            )


        return error_response(
            "Invalid image",
            serializer.errors
        )

class OrganizationLogoUploadAPIView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdminOrOwner,
    ]


    def patch(self, request):

        organization = request.user.organization

        serializer = OrganizationLogoSerializer(
            organization,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            return success_response(
                "Organization logo updated successfully",
                serializer.data
            )

        return error_response(
            "Invalid logo",
            serializer.errors
        )