from django.http import HttpResponse
from django.utils import timezone

class PasscodeRateLimitMiddleware:
    def __init__(self, get_response): self.get_response = get_response
    def __call__(self, request):
        lock_until = request.session.get('passcode_lock_until')
        if request.path == '/passcode/' and lock_until and timezone.now().timestamp() < lock_until:
            return HttpResponse('Too many attempts. Try again later.', status=429)
        return self.get_response(request)
