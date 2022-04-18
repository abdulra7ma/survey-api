from django.utils.deprecation import MiddlewareMixin


class InvokeIsAdministratorUserMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, callback, callback_args, callback_kwargs):
        """
        set is_administrator attribute to request user to avoid
        swagger comman errors
        """
        if not hasattr(request.user, "is_administrator"):
            setattr(request.user, "is_administrator", False)
