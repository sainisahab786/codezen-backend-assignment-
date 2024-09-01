from .models import PlatformApiCall

class PlatformApiCallMixin:
    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(request, response, *args, **kwargs)
        PlatformApiCall.objects.create(
            user=request.user,
            requested_url=request.build_absolute_uri(),
            requested_data=request.data,
            response_data=response.data
        )
        return response