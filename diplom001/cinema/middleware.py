import datetime
from django.contrib.auth import logout
from django.utils.deprecation import MiddlewareMixin


class TimeOutMiddleware(MiddlewareMixin):

    def process_request(self, request):
        shouldlogout = False
        if not request.user.is_superuser and request.user.is_authenticated:
            if 'beginSession' in request.session:
                elapsedtime = datetime.datetime.now().timestamp() - request.session['beginSession']
                if elapsedtime > 60*5*1000:
                    del request.session['beginSession']
                    shouldlogout = True
            else:
                request.session['beginSession'] = datetime.datetime.now().timestamp()
            if shouldlogout:
                logout(request)
        return self.get_response(request)
