from django.http import HttpResponseForbidden

class WiFiAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        allowed_ip_range = '192.168.0.0/24'  # Replace with your WiFi network's IP address range

        if not request.META['REMOTE_ADDR'].startswith(allowed_ip_range):
            return HttpResponseForbidden('Access denied')

        return self.get_response(request)