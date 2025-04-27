import traceback
from django.utils.deprecation import MiddlewareMixin
from .models import ExceptionLog

class ExceptionLoggingMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        try:
            request_body = None
            if request.body:
                try:
                    request_body = request.body.decode('utf-8')
                except UnicodeDecodeError:
                    request_body = '[Non UTF-8 Request Body]'
                    
            ExceptionLog.objects.create(
                title=str(exception),
                trace=traceback.format_exc(),
                url=request.build_absolute_uri(),
                request_body=request_body,
            )
        except Exception as e:
            print("Exception while logging an exception:", str(e))
        return None
