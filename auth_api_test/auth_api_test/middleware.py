from django.http import JsonResponse
from django.conf import settings
from auth_api_test.exception.base import ApiException
from auth_api_test.api.http import MyRequest


class ExceptionMiddleware:
    """异常处理中间件"""
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.
        # print('ExceptionMiddleware _init_')

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        # 为了调用子类方法，修改class类型为子类对象
        request.__class__ = MyRequest
        # print(type(request))

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        # print('ExceptionMiddleware __call__ response')
        # if 200 == response.status_code:
        #     return response
        # else:
        #     # if settings.DEBUG:
        #     #     return response
        #     return JsonResponse({
        #         'code': response.status_code,
        #         'msg': 'Failed...' + response.reason_phrase,
        #     }, status=response.status_code)

        return response

    @classmethod
    def process_exception(cls, request, exception):
        # print('ExceptionMiddleware process_exception')
        if not issubclass(exception.__class__, ApiException):
            if not settings.DEBUG:
                return JsonResponse(data={
                    'code': 500,
                    'msg': '服务器内部错误'
                }, status=500)
            pass
        else:
            ret_json = {
                'code': getattr(exception, 'code', ''),
                'msg': getattr(exception, 'message', ''),
            }
            return JsonResponse(ret_json, status=getattr(exception, 'status_code'))



