import os
from abc import ABC, abstractmethod

import leancloud
from leancloud import LeanCloudError


class Store(ABC):
    """
    后端类需要基于此类进行扩展
    """
    @abstractmethod
    def get_suburl(self, expires=False):
        """
        :param expires: 获取订阅链接的expires
        :type expires: bool
        :return: 返回查找到的符合条件的订阅链接list
        """
        pass

    @abstractmethod
    def set_suburl(self, url, expires=False):
        """
        :param url: 设置添加或更新订阅链接的expires
        :type url: str
        :param expires: 订阅链接的expires
        :type expires: bool
        :return: dict(status,code,)
        """
        pass

    @abstractmethod
    def get_proxy(self, expires=False):
        """
        :param expires: 获取订阅链接的expires
        :type expires: bool
        :return: 返回查找到的符合条件的订阅链接list
        """
        pass

    @abstractmethod
    def set_proxy(self, expires=False, **kwargs):
        """
        :param expires: 设置添加或更新订阅链接的expires
        :type expires: bool
        :param kwargs: 代理的字典信息
        :type kwargs: dict(type, data, message)
        """
        pass


class LeancloudStore(Store):
    """
    支持 Leancloud作为后端
    """
    def __init__(self):
        APP_ID = os.environ['LEANCLOUD_APP_ID']
        APP_KEY = os.environ['LEANCLOUD_APP_KEY']
        MASTER_KEY = os.environ['LEANCLOUD_APP_MASTER_KEY']
        leancloud.init(APP_ID, app_key=APP_KEY, master_key=MASTER_KEY)
        leancloud.use_master_key(True)
        self.suburls = leancloud.Object.extend('suburls')
        self.proxys = leancloud.Object.extend('proxys')

    def get_suburl(self, expires=False):
        return self._get_resouce(expires)

    def set_suburl(self, url, expires=False):
        self._set_resouce('url', url, expires)

    def get_proxy(self, expires=False):
        return self._get_resouce(expires)

    def set_proxy(self, proxy, expires=False, **kwargs):
        self._set_resouce('proxy', proxy, expires)

    def _get_resouce(self, expires=False):
        query = self.resouce.query
        query.equal_to('expires', expires)
        urls = query.find()
        return [item.dump() for item in urls]

    def _set_resouce(self, resoucename, resouce, expires=False, **kwargs):
        query = self.resouce.query
        query.equal_to(resoucename, resouce)
        try:
            proxy = query.first()
        except LeanCloudError as e:
            proxy = self.proxys()
        finally:
            proxy.set(resoucename, resouce)
            proxy.set('expires', expires)
            proxy.save()
