class SubdomainMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host().split(':')[0]
        request.subdomain = host.split('.')[0] if '.' in host else ''
        return self.get_response(request)
