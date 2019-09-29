from auth_api_test.exception.error import *
from django.http import JsonResponse


def test_util(request):
    return JsonResponse(
        {
            'code': 0,
            'msg': 'util__test_util',
            'data': []
        }
    )
