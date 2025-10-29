from django.urls import path
from django.http import JsonResponse
import boto3, os

def whoami_s3(request):
    sts = boto3.client(
        "sts",
        region_name=os.environ.get("AWS_S3_REGION_NAME") or os.environ.get("AWS_DEFAULT_REGION", "us-east-2"),
    )
    ident = sts.get_caller_identity()   # normalmente não precisa de policy explícita
    return JsonResponse(ident)

urlpatterns = [
    # ... suas rotas
    path("whoami-s3/", whoami_s3),
]
