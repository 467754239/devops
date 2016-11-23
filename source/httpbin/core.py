# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import uuid
import json
import random
import argparse


from flask import Flask, Response, request, render_template, redirect, make_response, url_for, jsonify as flask_jsonify
from werkzeug.datastructures import MultiDict
from werkzeug.http import http_date

import filters
from helpers import ROBOT_TXT, ANGRY_ASCII, get_dict, get_headers, status_code, secure_cookie
from utils import weighted_choice
from structures import CaseInsensitiveDict



def jsonify(*args, **kwargs):
    response = flask_jsonify(*args, **kwargs)
    if not response.data.endswith(b'\n'):
        response.data += b'\n'
    return response

# Find the correct template folder when running from a different location
tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

app = Flask(__name__, template_folder=tmpl_dir)

@app.route('/')
def view_landing_page():
    ''' Generates Loading Page. '''
    tracking_enabled  = 'HTTPBIN_TRACKING' in os.environ
    return render_template('index.html', tracking_enabled=tracking_enabled)

@app.route('/html')
def view_html_page():
    ''' Simple Html Page '''

    return render_template('moby.html')

@app.route('/robots.txt')
def view_robots_page():
    ''' Simple Html Page '''

    response = make_response()
    response.data = ROBOT_TXT
    response.content_type = 'text/plain'
    return response

@app.route('/deny')
def view_deny_page():
    '''Simple Html Page '''
    response = make_response()
    response.data = ANGRY_ASCII
    response.content_type = 'text/plain'
    return response
    # return "YOU SHOULDN'T BE HERE"

@app.route('/ip')
def view_origin():
    """Return Origin IP"""

    return jsonify(origin=request.headers.get('X-Forwarded-For', request.remote_addr))

@app.route('/headers')
def view_headers():
    '''Return HTTP HEADERS'''

    return jsonify(get_dict('headers'))

@app.route('/user-agent')
def view_user_agent():
    '''Return User-Agent'''

    headers = get_headers()
    return jsonify({"User-Agent" : headers['User-Agent']})

@app.route('/get', methods=['GET'])
def view_get():
    '''Return GET Data.'''

    return jsonify(get_dict('url', 'args', 'headers', 'origin'))

@app.route('/post', methods=['POST'])
def view_post():
    '''Return POST Data'''

    return jsonify(get_dict('url', 'args', 'form', 'data', 'origin', 'headers', 'files', 'json'))

@app.route('/gzip')
@filters.gzip
def view_gzip_encoded_content():
    '''Return gzip-encoded Data'''

    return jsonify(get_dict('origin', 'headers', method=request.method, gzipped=True))

@app.route('/deflate')
@filters.deflate
def view_deflate_encoded_content():
    """Returns Deflate-Encoded Data."""

    return jsonify(get_dict(
        'origin', 'headers', method=request.method, deflated=True))

@app.route('/redirect/<int:n>')
def redirect_n_time(n):
    '''302 Redirects n times'''

    '''
    如果为真则pass，否则抛出AssertionError错误
    '''
    assert n > 0

    '''
    如果此url没有传递参数 或者 参数absolute是True； absolute为True， 其它情况都为False.
    '''
    absolute = request.args.get('absolute', 'false').lower() == 'true'

    if n == 1:
        return redirect(url_for('view_get', _external=absolute))

    if absolute:
        return _redirect('absolute', n, True)  # 绝对
    else:
        print "absolute>>>", absolute
        return _redirect('relative', n, True)  # 相对

def _redirect(kind, n, external):
    print "_redirect>>>", kind, n, external
    return redirect(url_for('{0}_redirect_n_times'.format(kind), n=n-1, _external=external))

@app.route('/relative-redirect/<int:n>')
def relative_redirect_n_times(n):
    """302 Redirects n times."""
    print 'relative>>>', type(n), n
    assert n > 0
    print 'pass>>>', n
    response = app.make_response('')
    response.status_code = 302

    if n == 1:
        response.headers['Location'] = url_for('view_get')
        return response
    
    response.headers['Location'] = url_for('relative_redirect_n_times', n=n-1)
    return response

@app.route('/absolute-redirect/<int:n>')
def absolute_redirect_n_times(n):
    """302 Redirects n times."""

    assert n > 0
    if n == 1:
        return redirect(url_for('view_get', _external=True))
    
    return _redirect('absolute', n, True)

@app.route('/cookies', methods=['GET', 'POST'])     # 没有成功
def view_cookies(hide_env=True):
    """Returns cookie data."""

    cookies = dict(request.cookies.items())
    print cookies
    print request.headers.get('cookies')
    print request.cookies.get('name')
    print request.cookies.get('username')  
    return ''

@app.route('/forms/post')
def view_forms_post():
    """Simple HTML form."""

    return render_template('forms-post.html')

@app.route('/cookies/set/<name>/<value>')
def set_cookie(name, value):
    """Sets a cookie and redirects to cookie list."""

    r = app.make_response(redirect(url_for('view_cookies')))
    r.set_cookie(key=name, value=value, secure=secure_cookie())
    return r

@app.route('/cookies/set')
def set_cookies():
    """Sets cookie(s) as provided by the query string and redirects to cookie list."""

    cookies = dict(request.args.items())
    r = make_response(redirect(url_for('view_cookies')))
    print cookies
    return ''

@app.route('/status/<codes>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'TRACE'])
def view_status_code(codes):
    """Return status code or random status code if more than one are given"""

    if ',' not in codes:
        code = int(codes)
        return status_code(code)

    choices = []
    for choice in codes.split(','):
        print choice
        if ':' not in choice:
            code = choice
            weight = 1
        else:
            code, weight = choice.split(':')
        choices.append((int(code), float(weight)))

    code = weighted_choice(choices)
    print code
    return status_code(code)

@app.route('/stream/<int:n>')   # int为2的时候提示语法错误
def stream_n_messages(n):
    """Stream n JSON messages"""

    response = get_dict('url', 'args', 'headers', 'origin')
    print response
    n = min(n, 100)
    print n

    def generate_stream():
        for i in range(n):
            response['id'] = i
            print response
            yield json.dumps(response) + '\n'

    return Response( generate_stream(), headers={'Content-Type' : 'application/json'} )

@app.route('/response-headers')
def response_headers():
    """Returns a set of response headers from the query string """
    headers = MultiDict(request.args.items(multi=True))
    response = jsonify(list(headers.lists()))

    while True:
        original_data = response.data
        d = {}
        for key in response.headers.keys():
            value = response.headers.get_all(key)
            if len(value) == 1:
                value = value[0]
            d[key] = value
        response = jsonify(d)
        for key, value in headers.items(multi=True):
            response.headers.add(key, value)
        response_has_changed = response.data != original_data
        if not response_has_changed:
            break
    return response









    return '->'

@app.route('/bytes/<int:n>')
def random_bytes(n):
    """Returns n random bytes generated with given seed."""

    n = min(n, 100 * 1024) # set 100KB limit

    arg = request.args.items()
    params = CaseInsensitiveDict(request.args.items())
    print arg
    print params

    if 'seed' in params:
        pass

    response = make_response()

    # Note: can't just use os.urandom here because it ignores the seed
    response.data = bytearray(random.randint(0, 255) for i in range(n))
    response.content_type = 'application/octet-stream'
    return response

@app.route('/cache')
def cache():
    """Returns a 304 if an If-Modified-Since header or If-None-Match is present. Returns the same as a GET otherwise."""
    is_conditional = request.headers.get('If-Modified-Since') or request.headers.get('If-None-Match')
    if is_conditional is None:
        response = view_get()
        response.headers['Last-Modified'] = http_date()
        response.headers['ETag'] = uuid.uuid4().hex
        return response
    else:
        return status_code(304)

@app.route('/cache/<int:value>')
def cache_control(value):
    """Sets a Cache-Control header."""

    response = view_get()

    # http://condor.depaul.edu/dmumaugh/readings/handouts/SE435/HTTP/node24.html
    response.headers['Cache-Control'] = 'public, max-age={0}'.format(value)
    return response

@app.route('/encoding/utf8')
def encoding():
    return render_template('UTF-8-demo.txt')

@app.route('/links/<int:n>')
def link(n):
    """Redirect to first links page."""

    return redirect(url_for('link_page', n=n, offset=0))

@app.route('/links/<int:n>/<int:offset>')
def link_page(n, offset):
    """Generate a page containing n links to other pages which do the same."""

    # limit to between 1 and 200 links
    n = min(max(1, n), 200)

    link = "<a href='{0}'>{1}</a> "

    html = ['<html><head><title>Links</title></head><body>']
    for i in xrange(n):
        if i == offset:
            html.append("{0}".format(i))
        else:
            html.append(link.format(url_for('link_page', n=n, offset=i), i))

    print html
    html.append('</body></html>')
    return ''.join(html)

@app.route('/image')
def image():
    """Returns a simple image of the type suggest by the Accept header."""
    
    headers = get_headers()
    print headers
    if "accept" not in headers:
        return redirect('/image/png')   # Default media type to png

    accept = headers['accept'].lower()
    print accept
    # image_type = ['image/webp', 'image/svg+xml', 'image/jpeg', 'image/png']
    if 'image/webp' in accept:
        return redirect('/image/webp')
    elif 'image/svg+xml' in accept:
        return redirect('/image/svg')
    elif 'image/jpeg' in accept:
        return redirect('/image/jpeg')
    elif 'image/png' in accept:
        return redirect('/image/png')
    else:
        return status_code(406) # Unsupported media type

@app.route('/image/png')
def image_png():
    data = resource('images/pig_icon.png')
    headers = {'Content-Type' : 'image/png'}
    return Response(data, headers=headers)

@app.route('/image/jpeg')
def image_jpeg():
    data = resource('images/jackal.jpg')
    return Response(data, headers={'Content-Type': 'image/jpeg'})

@app.route('/image/webp')
def image_webp():
    data = resource('images/wolf_1.webp')
    return Response(data, headers={'Content-Type': 'image/webp'})

@app.route('/image/svg')
def image_svg():
    data = resource('images/svg_logo.svg')
    return Response(data, headers={'Content-Type': 'image/svg+xml'})

def resource(filename):
    path = os.path.join(tmpl_dir, filename)
    return open(path, 'r').read()

@app.route('/xml')
def xml():
    response = make_response(render_template('sample.xml'))
    response.headers['Content-Type'] = "application/xml"
    return response








if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--host", default="127.0.0.1")
    args = parser.parse_args()
    app.run(port=args.port, host=args.host, debug=True)
