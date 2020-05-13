# coding: utf-8

from flask import Flask
from flask_restful import Api
from asm.contrib.middleware import HTTPMethodOverrideMiddleware, HttpsRedirectMiddleware
from asm.api import shadowsocks, shadowsocksr, vmess

app = Flask(__name__)
api = Api(app)

api.add_resource(shadowsocks, '/ss')
api.add_resource(shadowsocksr, '/ssr')
api.add_resource(vmess, '/vmess')

# 注册中间件
app.wsgi_app = HTTPMethodOverrideMiddleware(app.wsgi_app)
app.wsgi_app = HttpsRedirectMiddleware(app.wsgi_app)
