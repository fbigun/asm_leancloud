# coding: utf-8

import os

from werkzeug.wrappers import Request, Response
from werkzeug.utils import redirect
from werkzeug.exceptions import HTTPException, NotFound


class HTTPMethodOverrideMiddleware(object):
    """
    使用中间件以接受标准 HTTP 方法
    详见：https://gist.github.com/nervouna/47cf9b694842134c41f59d72bd18bd6c
    """

    allowed_methods = frozenset(['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
    bodyless_methods = frozenset(['GET', 'HEAD', 'DELETE', 'OPTIONS'])

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        request = Request(environ)
        method = request.args.get('METHOD', '').upper()
        if method in self.allowed_methods:
            method = method.encode('ascii', 'replace')
            environ['REQUEST_METHOD'] = method
        if method in self.bodyless_methods:
            environ['CONTENT_LENGTH'] = 0
        return self.app(environ, start_response)


class HttpsRedirectMiddleware(object):
    """
    生产环境下始终用 HTTPS 安全协议传输
    设置环境变量 ASM_APP_ENV='production' 时为生产环境
    """

    def __init__(self, wsgi_app):
        self.origin_app = wsgi_app

    def __call__(self, environ, start_response):
        request = Request(environ)
        is_prod = os.environ.get('ASM_APP_ENV') == 'production' or False
        if is_prod and request.headers.get('X-Forwarded-Proto') != 'https':
            url = 'https://{0}{1}'.format(request.host, request.full_path)
            return redirect(url)(environ, start_response)

        return self.origin_app(environ, start_response)


class ResourceNotFoundMiddleware(object):

    def __init__(self, wsgi_app):
        self.origin_app = wsgi_app

    def __call__(self, environ, start_response):
        response = Response(environ)
        response.status_code
        if isinstance(environ, HTTPException):
            return NotFound()

        return self.origin_app(environ, start_response)


class CORSMiddleware(object):

    def __init__(self, wsgi_app):
        self.origin_app = wsgi_app

    def __call__(self, environ, start_response):
        pass
