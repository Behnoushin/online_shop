import traceback
from django.utils.deprecation import MiddlewareMixin
from .models import ExceptionLog

class ExceptionLoggingMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        ExceptionLog.objects.create(
            title=str(exception),
            trace=traceback.format_exc(),
            url=request.build_absolute_uri(),
            request_body=request.body.decode('utf-8') if request.body else None
        )
        return None
