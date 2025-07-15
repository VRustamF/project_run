from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.conf import settings

@api_view(['GET'])
def informationView(request):
    return Response(settings.INFORMATION)