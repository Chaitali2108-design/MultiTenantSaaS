from django.utils.deprecation import MiddlewareMixin


class TenantMiddleware(MiddlewareMixin):

    def process_request(self, request):

        request.organization = None

        if request.user.is_authenticated:

            request.organization = request.user.organization