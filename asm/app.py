# coding: utf-8

from flask import Flask
from flask_restful import Api

app = Flask(__name__)
app = Api(app)

from asm.common.middleware import HTTPMethodOverrideMiddleware, HttpsRedirectMiddleware

# 注册中间件
app.wsgi_app = HTTPMethodOverrideMiddleware(app.wsgi_app)
app.wsgi_app = HttpsRedirectMiddleware(app.wsgi_app)

# 动态路由
# app.register_blueprint(todos_view, url_prefix='/todos')
# app.register_blueprint(users_view, url_prefix='/users')
