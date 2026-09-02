from django.db import connection
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
@api_view(['GET'])
def health(request):
    result={'database':'healthy','redis':'configured' if settings.REDIS_URL else 'not configured'}
    try:
        connection.ensure_connection()
    except Exception: result['database']='unhealthy'
    code=200 if result['database']=='healthy' else 503
    return Response({'status':'healthy' if code==200 else 'unhealthy',**result},status=code)
