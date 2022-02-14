# class RestAuthMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#     @staticmethod
#     def get_user(request):
#         user = get_user(request)
#         if user.is_authenticated:
#             return user
#         token_authentication = TokenAuthentication()
#         try:
#             user, token = token_authentication.authenticate(request)
#         except:
#             pass
#         return user
#     def __call__(self, request):
#         request.user = SimpleLazyObject(lambda: self.__class__.get_user(request))
#         response = self.get_response(request)
#         return response


class TokenAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        return self.get_response(request)