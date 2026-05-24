from django.http import HttpResponseForbidden

def csrf_failure(request, reason=""):
    return HttpResponseForbidden("Forbidden (403)")
