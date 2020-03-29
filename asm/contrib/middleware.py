# coding: utf-8

import os

from werkzeug.wrappers import Request, Response
from werkzeug.utils import redirect
from werkzeug.exceptions import HTTPException, NotFound

from . import utils


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


class LeancloudCORSMiddleware(object):
    ALLOW_ORIGIN = utils.to_native('*')
    ALLOW_HEADERS = utils.to_native(', '.join([
        'Content-Type',
        'X-AVOSCloud-Application-Id',
        'X-AVOSCloud-Application-Key',
        'X-AVOSCloud-Application-Production',
        'X-AVOSCloud-Client-Version',
        'X-AVOSCloud-Request-sign',
        'X-AVOSCloud-Session-Token',
        'X-AVOSCloud-Super-Key',
        'X-Requested-With',
        'X-Uluru-Application-Id,'
        'X-Uluru-Application-Key',
        'X-Uluru-Application-Production',
        'X-Uluru-Client-Version',
        'X-Uluru-Session-Token',
        'X-LC-Hook-Key',
        'X-LC-Id',
        'X-LC-Key',
        'X-LC-Prod',
        'X-LC-Session',
        'X-LC-Sign',
        'X-LC-UA',
    ]))
    ALLOW_METHODS = utils.to_native(', '.join(['PUT', 'GET', 'POST', 'DELETE', 'OPTIONS']))
    MAX_AGE = utils.to_native('86400')

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        if environ['REQUEST_METHOD'] == 'OPTIONS':
            start_response(
                utils.to_native('200 OK'),
                [(utils.to_native('Access-Control-Allow-Origin'), environ.get('HTTP_ORIGIN', self.ALLOW_ORIGIN)),
                 (utils.to_native('Access-Control-Allow-Headers'), self.ALLOW_HEADERS),
                 (utils.to_native('Access-Control-Allow-Methods'), self.ALLOW_METHODS),
                 (utils.to_native('Access-Control-Max-Age'), self.MAX_AGE)])
            return [utils.to_native('')]
        else:

            def cors_start_response(status, headers, exc_info=None):
                headers.append((utils.to_native('Access-Control-Allow-Origin'), self.ALLOW_ORIGIN))
                headers.append((utils.to_native('Access-Control-Allow-Headers'), self.ALLOW_HEADERS))
                headers.append((utils.to_native('Access-Control-Allow-Methods'), self.ALLOW_METHODS))
                headers.append((utils.to_native('Access-Control-Max-Age'), self.MAX_AGE))
                return start_response(status, headers, exc_info)

            return self.app(environ, cors_start_response)
