from django.core.handlers.wsgi import WSGIRequest
from django.utils.functional import cached_property


class MyRequest(WSGIRequest):
    """继承了HttpRequest对象"""

    @cached_property
    def PARAMS(self):
        return dict(getattr(self, self.method, None))

    def p(self, field_name):
        if not self.PARAMS:
            return None
        field_value = self.PARAMS.get(field_name, None)
        if field_value and len(field_value) == 1 and type(field_value) is list:
            return field_value[0]
        return field_value
