# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import base64

from flask import Flask, request, make_response

from structures import CaseInsensitiveDict

ASCII_ART = """
    -=[ teapot ]=-
       _...._
     .'  _ _ `.
    | ."` ^ `". _,
    \_;`"---"`|//
      |       ;/
      \_     _/
        `\"\"\"`
"""

REDIRECT_LOCATION = '/redirect/1'

ENV_HEADERS = (
    'X-Varnish',
    'X-Request-Start',
    'X-Heroku-Queue-Depth',
    'X-Real-Ip',
    'X-Forwarded-Proto',
    'X-Forwarded-Protocol',
    'X-Forwarded-Ssl',
    'X-Heroku-Queue-Wait-Time',
    'X-Forwarded-For',
    'X-Heroku-Dynos-In-Use',
    'X-Forwarded-For',
    'X-Forwarded-Protocol',
    'X-Forwarded-Port',
    'Runscope-Service'
)

ROBOT_TXT = """User-agent: *
Disallow: /deny
"""

ACCEPTED_MEDIA_TYPES = [
    'image/webp',
    'image/svg+xml',
    'image/jpeg',
    'image/png',
    'image/*'
]

ANGRY_ASCII ="""
          .-''''''-.
        .' _      _ '.
       /   O      O   \\
      :                :
      |                |
      :       __       :
       \  .-"`  `"-.  /
        '.          .'
          '-......-'
     YOU SHOULDN'T BE HERE
"""

def json_safe(string, content_type="application/octet-stream"):
    """Returns JSON-safe version of `string`.
    If `string` is a Unicode string or a valid UTF-8, it is returned unmodified,
    as it can safely be encoded to JSON string.
    If `string` contains raw/binary data, it is Base64-encoded, formatted and
    returned according to "data" URL scheme (RFC2397). Since JSON is not
    suitable for binary data, some additional encoding was necessary; "data"
    URL scheme was chosen for its simplicity.
    """

    try:
        string = string.encode('utf-8')
        json.dumps(string)
        return string
    except (ValueError, TypeError):
        return b''.join([b'data', content_type.encode('utf-8'), b';base64,', base64.b64encode(string)]).decode('utf-8')

def semiflatten(multi):
    """Convert a MutiDict into a regular dict. If there are more than one value
    for a key, the result will have a list of values for the key. Otherwise it
    will have the plain value."""

    # 转换成标准的字典格式
    if multi:
        result = multi.to_dict(flat=False)  
        for k, v in result.items():
            if len(v) == 1:     # 将value是1个元素的，那么去掉中括号.
                result[k] = v[0]
        return result
    else:
        return multi

def get_url(request):
    """
    Since we might be hosted behind a proxy, we need to check the
    X-Forwarded-Proto, X-Forwarded-Protocol, or X-Forwarded-SSL headers
    to find out what protocol was used to access us.
    """
    protocol = request.headers.get('X-Forwarded-Proto') or request.headers.get('X-Forwarded-Protocol')
    if protocol is None and request.headers.get('X-Forwarded-Ssl') == 'on':
        protocol = 'https'
    if protocol is None:
        return request.url

    url = list(urlparse(request.url))

    return 'error None'

def get_files():
    '''Return files dict from request context'''

    files = dict()
    for k, v in request.files.items():
        pass

    return files

def get_headers(hide_env=True):
    '''Return headers dict from request context'''

    headers = dict(request.headers.items())
    if hide_env and ("show_env" not in request.args):
        for key in ENV_HEADERS:
            try:
                del headers[key]
            except KeyError:
                pass

    return CaseInsensitiveDict(headers.items())

def get_dict(*keys, **extras):
    """Returns request dict of given keys."""

    _keys = ('url', 'args', 'form', 'data', 'origin', 'headers', 'files', 'json')

    assert all(map(_keys.__contains__, keys))
    data = request.data
    form = semiflatten(request.form)

    try:
        _json = json.loads(data.encode('utf-8'))
    except (ValueError, TypeError):
        _json = None

    d = dict(
        url = get_url(request),
        args = semiflatten(request.args),
        form = form,
        data = json_safe(data),
        origin = request.headers.get('X-Forwarded-For', request.remote_addr),
        headers = get_headers(),
        files = get_files(),
        json = _json
        )

    out_d = dict()

    for key in keys:
        out_d[key] = d.get(key)

    out_d.update(extras)
    return out_d

def status_code(code):
    """Returns response object of given status code."""

    #REDIRECT_LOCATION = '/redirect/1'

    redirect = dict(headers=dict(location=REDIRECT_LOCATION))

    code_map = {
        301 : redirect,
        302 : redirect,
        303 : redirect,
        304 : dict(data=''),
        305 : redirect,
        307 : redirect,
        401 : dict(headers={'WWW-Authenticate':'Basic realm="Fake Realm"'}),
        402 : dict(
                data='Fuck you, pay me!',
                headers={'x-more-info': 'http://vimeo.com/22053820'}),
        406 : dict(data = json.dumps({
                        'message' : 'Client did not request a supported media type.',
                        'accept' : ACCEPTED_MEDIA_TYPES}),
                        headers = {'Content-Type' : 'applicaton/json'}),
        407 : dict(headers={'Proxy-Authenticate': 'Basic realm="Fake Realm"'}),
        418 : dict(# I'm a teapot!
                data=ASCII_ART,
                headers={'x-more-info': 'http://tools.ietf.org/html/rfc2324'}),
    }

    r = make_response()
    r.status_code = code
    print r
    if code in code_map:
        m = code_map[code]
        
        print 'm>>>', m
        if 'data' in m:
            r.data = m['data']
        if 'headers' in m:
            r.headers = m['headers']
    print r
    return r

def secure_cookie():
    """Return true if cookie should have secure attribute"""
    print "request.environ>>>", request.environ
    return request.environ['wsgi.url_scheme'] == 'https'