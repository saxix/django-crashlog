import logging
import socket
import sys

from django.views.debug import ExceptionReporter

from crashlog.config import conf

from .models import Error

logger = logging.getLogger('crashlog')


def process_exception(exception, request=None, message_user=False):
    if exception.__class__ in conf._ignore_exceptions:
        return
    reporter = ExceptionReporter(request, *sys.exc_info())
    server_name = socket.gethostname()
    tb_text = reporter.get_traceback_html()
    class_name = exception.__class__.__name__

    if request:
        url = request.build_absolute_uri()
        user = getattr(request, 'user', None)
    else:
        url = 'N/A'
        user = 'N/A'

    defaults = dict(
        class_name=class_name,
        message=str(exception),
        url=url,
        server_name=server_name,
        traceback=tb_text,
        username=str(user)
    )

    try:
        err = Error.objects.create(**defaults)
        if message_user and request:
            err.message_user(request, str(exception))
        return err
    except Exception as exc:  # pragma: no cover
        logger.critical(exc)


class CrashLogMiddleware:

    def __init__(self, get_response=None):
        self.get_response = get_response
        super().__init__()

    def process_exception(self, request, exception):
        process_exception(exception, request)

    def __call__(self, request):
        return self.get_response(request)
