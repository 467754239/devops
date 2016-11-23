# -*- coding: utf-8 -*-
from __future__ import unicode_literals

"""
httpbin.filters
~~~~~~~~~~~~~~~
This module provides response filter decorators.
"""

import gzip as gzip2
from six import BytesIO

from decorator import decorator
from flask import Flask, Response

app = Flask(__name__)


@decorator
def gzip(f, *args, **kwargs):
    """GZip Flask Response Decorator."""

    data = f(*args, **kwargs)
    
    if isinstance(data, Response):
        content = data.data
    else:
        content = data

    gzip_buffer = BytesIO()
    gzip_file = gzip2.GzipFile(
        mode='wb',
        compresslevel=4,
        fileobj=gzip_buffer
    )
    gzip_file.write(content)
    gzip_file.close()

    gzip_data = gzip_buffer.getvalue()

    if isinstance(data, Response):
        data.data = gzip_data
        data.headers['Content-Encoding'] = 'gzip'
        data.headers['Content-Length'] = str(len(data.data))
        return data
    else:
        return gzip_data

@decorator
def deflate(f, *args, **kwargs):
    """Deflate Flask Response Decorator."""

    data = f(*args, **kwargs)

    if isinstance(data, Response):
        content = data.data
    else:
        content = data

    deflater = zlib.compressobj()
    deflated_data = deflater.compress(content)
    deflated_data += deflater.flush()

    if isinstance(data, Response):
        data.data = deflated_data
        data.headers['Content-Encoding'] = 'deflate'
        data.headers['Content-Length'] = str(len(data.data))

        return data

    return deflated_data