from rest_framework import serializers

class BaseResponseMixin:
    def finalize_response(self, request, response, *args, **kwargs):
        if isinstance(response.data, dict) and 'is_successful' not in response.data:
            response.data = {
                'is_successful': response.status_code < 400,
                'errors': None if response.status_code < 400 else response.data,
                'data': response.data if response.status_code < 400 else None
            }
        return super().finalize_response(request, response, *args, **kwargs)
    

class BaseResponseSerializer(serializers.Serializer):
    is_successful = serializers.BooleanField()
    errors = serializers.ListField(child=serializers.CharField(), allow_null=True)
    data = serializers.DictField(allow_null=True)