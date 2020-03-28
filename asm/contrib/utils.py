import six
import hashlib


def sign_by_key(timestamp, key):
    s = '{0}{1}'.format(timestamp, key)
    return hashlib.md5(s.encode('utf-8')).hexdigest()


if six.PY2:

    def to_native(s):
        if isinstance(s, unicode):  # NOQA
            return s.encode('utf-8')
        return s
else:

    def to_native(s):
        if isinstance(s, bytes):
            return s.decode('utf-8')
        return s
