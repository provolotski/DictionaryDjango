class ActiveDirectoryAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Добавляем user в request
        request.user = request.session.get('user', {'is_authenticated': False})
        return self.get_response(request)