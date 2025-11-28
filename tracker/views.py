from django.http import JsonResponse
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny

def api_health_check(request):
    return JsonResponse({
        "status": "ok",
        "message": "Backend is running successfully."
    }, status=200)
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def update_status(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    try:
        data = json.loads(request.body.decode("utf-8"))
        new_status = data.get("status")

        if not new_status:
            return JsonResponse({"error": "Status is required"}, status=400)

        return JsonResponse({
            "message": "Status updated successfully",
            "new_status": new_status
        }, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
