import requests
from django.conf import settings


class TokenAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        print(request.user)
        return self.get_response(request)