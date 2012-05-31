# -*- coding: utf-8 -*-

"""
cghub_api.models
~~~~~~~~~~~~~~~~

This module contains the primary objects that power Requests.
"""

from .exceptions import (
        RequestException, QueryRequired)


class Request(object):
    """The :class:`Request <Request>` object. It carries out all functionality of
    Requests. Recommended interface is with the Requests functions.
    """

    def __init__(self,
            query=None,
            filename=None):
        self.query = query

    def __repr__(self):
        return '<Request [%s]>' % (self.query)


    def register_hook(self, event, hook):
        """Properly register a hook."""

        self.hooks[event].append(hook)

    def deregister_hook(self, event, hook):
        """Deregister a previously registered hook.
        Returns True if the hook existed, False if not.
        """

        try:
            self.hooks[event].remove(hook)
            return True
        except ValueError:
            return False

    def send(self, anyway=False, prefetch=False):
        """Sends the request. Returns True if successful, False if not.
        If there was an HTTPError during transmission,
        self.response.status_code will contain the HTTPError code.

        Once a request is successfully sent, `sent` will equal True.

        :param anyway: If True, request will be sent, even if it has
        already been sent.
        """

        # Build the URL
        url = self.full_url

        # Pre-request hook.
        r = dispatch_hook('pre_request', self.hooks, self)
        self.__dict__.update(r.__dict__)

        # Logging
        if self.config.get('verbose'):
            self.config.get('verbose').write('%s   %s   %s\n' % (
                datetime.now().isoformat(), self.method, url
            ))

        # Nottin' on you.
        body = None
        content_type = None

        # Use .netrc auth if none was provided.
        if not self.auth and self.config.get('trust_env'):
            self.auth = get_netrc_auth(url)

        if self.auth:
            if isinstance(self.auth, tuple) and len(self.auth) == 2:
                # special-case basic HTTP auth
                self.auth = HTTPBasicAuth(*self.auth)

            # Allow auth to make its changes.
            r = self.auth(self)

            # Update self to reflect the auth changes.
            self.__dict__.update(r.__dict__)

        # Multi-part file uploads.
        if self.files:
            (body, content_type) = self._encode_files(self.files)
        else:
            if self.data:

                body = self._encode_params(self.data)
                if isinstance(self.data, str):
                    content_type = None
                else:
                    content_type = 'application/x-www-form-urlencoded'

        # Add content-type if it wasn't explicitly provided.
        if (content_type) and (not 'content-type' in self.headers):
            self.headers['Content-Type'] = content_type

        _p = urlparse(url)
        no_proxy = filter(lambda x:x.strip(), self.proxies.get('no', '').split(','))
        proxy = self.proxies.get(_p.scheme)

        if proxy and not any(map(_p.netloc.endswith, no_proxy)):
            conn = poolmanager.proxy_from_url(proxy)
            _proxy = urlparse(proxy)
            if '@' in _proxy.netloc:
                auth, url = _proxy.netloc.split('@', 1)
                self.proxy_auth = HTTPProxyAuth(*auth.split(':', 1))
                r = self.proxy_auth(self)
                self.__dict__.update(r.__dict__)
        else:
            # Check to see if keep_alive is allowed.
            try:
                if self.config.get('keep_alive'):
                    conn = self._poolmanager.connection_from_url(url)
                else:
                    conn = connectionpool.connection_from_url(url)
                    self.headers['Connection'] = 'close'
            except LocationParseError as e:
                raise InvalidURL(e)

        if url.startswith('https') and self.verify:

            cert_loc = None

            # Allow self-specified cert location.
            if self.verify is not True:
                cert_loc = self.verify

            # Look for configuration.
            if not cert_loc and self.config.get('trust_env'):
                cert_loc = os.environ.get('REQUESTS_CA_BUNDLE')

            # Curl compatibility.
            if not cert_loc and self.config.get('trust_env'):
                cert_loc = os.environ.get('CURL_CA_BUNDLE')

            if not cert_loc:
                cert_loc = DEFAULT_CA_BUNDLE_PATH

            if not cert_loc:
                raise Exception("Could not find a suitable SSL CA certificate bundle.")

            conn.cert_reqs = 'CERT_REQUIRED'
            conn.ca_certs = cert_loc
        else:
            conn.cert_reqs = 'CERT_NONE'
            conn.ca_certs = None

        if self.cert and self.verify:
            if len(self.cert) == 2:
                conn.cert_file = self.cert[0]
                conn.key_file = self.cert[1]
            else:
                conn.cert_file = self.cert

        if not self.sent or anyway:

            # Skip if 'cookie' header is explicitly set.
            if 'cookie' not in self.headers:
                cookie_header = get_cookie_header(self.cookies, self)
                if cookie_header is not None:
                    self.headers['Cookie'] = cookie_header

            # Pre-send hook.
            r = dispatch_hook('pre_send', self.hooks, self)
            self.__dict__.update(r.__dict__)

            # catch urllib3 exceptions and throw Requests exceptions
            try:
                # Send the request.
                r = conn.urlopen(
                    method=self.method,
                    url=self.path_url,
                    body=body,
                    headers=self.headers,
                    redirect=False,
                    assert_same_host=False,
                    preload_content=False,
                    decode_content=False,
                    retries=self.config.get('max_retries', 0),
                    timeout=self.timeout,
                )
                self.sent = True

            except MaxRetryError as e:
                raise ConnectionError(e)

            except (_SSLError, _HTTPError) as e:
                if self.verify and isinstance(e, _SSLError):
                    raise SSLError(e)

                raise Timeout('Request timed out.')

            # build_response can throw TooManyRedirects
            self._build_response(r)

            # Response manipulation hook.
            self.response = dispatch_hook('response', self.hooks, self.response)

            # Post-request hook.
            r = dispatch_hook('post_request', self.hooks, self)
            self.__dict__.update(r.__dict__)

            # If prefetch is True, mark content as consumed.
            if prefetch or self.prefetch:
                # Save the response.
                self.response.content

            if self.config.get('danger_mode'):
                self.response.raise_for_status()

            return self.sent


class Response(object):
    """The core :class:`Response <Response>` object. All
    :class:`Request <Request>` objects contain a
    :class:`response <Response>` attribute, which is an instance
    of this class.
    """

    def __init__(self):

        self._content = False
        self._content_consumed = False

        #: Integer Code of responded HTTP Status.
        self.status_code = None

        #: Case-insensitive Dictionary of Response Headers.
        #: For example, ``headers['content-encoding']`` will return the
        #: value of a ``'Content-Encoding'`` response header.
        self.headers = CaseInsensitiveDict()

        #: File-like object representation of response (for advanced usage).
        self.raw = None

        #: Final URL location of Response.
        self.url = None

        #: Resulting :class:`HTTPError` of request, if one occurred.
        self.error = None

        #: Encoding to decode with when accessing r.text.
        self.encoding = None

        #: A list of :class:`Response <Response>` objects from
        #: the history of the Request. Any redirect responses will end
        #: up here.
        self.history = []

        #: The :class:`Request <Request>` that created the Response.
        self.request = None

        #: A CookieJar of Cookies the server sent back.
        self.cookies = None

        #: Dictionary of configurations for this request.
        self.config = {}

    def __repr__(self):
        return '<Response [%s]>' % (self.status_code)

    def __bool__(self):
        """Returns true if :attr:`status_code` is 'OK'."""
        return self.ok

    def __nonzero__(self):
        """Returns true if :attr:`status_code` is 'OK'."""
        return self.ok

    @property
    def ok(self):
        try:
            self.raise_for_status()
        except RequestException:
            return False
        return True

    def iter_content(self, chunk_size=1, decode_unicode=False):
        """Iterates over the response data.  This avoids reading the content
        at once into memory for large responses.  The chunk size is the number
        of bytes it should read into memory.  This is not necessarily the
        length of each item returned as decoding can take place.
        """
        if self._content_consumed:
            raise RuntimeError(
                'The content for this response was already consumed'
            )

        def generate():
            while 1:
                chunk = self.raw.read(chunk_size)
                if not chunk:
                    break
                yield chunk
            self._content_consumed = True

        gen = stream_untransfer(generate(), self)

        if decode_unicode:
            gen = stream_decode_response_unicode(gen, self)

        return gen

    def iter_lines(self, chunk_size=10 * 1024, decode_unicode=None):
        """Iterates over the response data, one line at a time.  This
        avoids reading the content at once into memory for large
        responses.
        """

        pending = None

        for chunk in self.iter_content(
            chunk_size=chunk_size,
            decode_unicode=decode_unicode):

            if pending is not None:
                chunk = pending + chunk
            lines = chunk.splitlines()

            if lines and lines[-1] and chunk and lines[-1][-1] == chunk[-1]:
                pending = lines.pop()
            else:
                pending = None

            for line in lines:
                yield line

        if pending is not None:
            yield pending

    @property
    def content(self):
        """Content of the response, in bytes."""

        if self._content is False:
            # Read the contents.
            try:
                if self._content_consumed:
                    raise RuntimeError(
                        'The content for this response was already consumed')

                if self.status_code is 0:
                    self._content = None
                else:
                    self._content = bytes().join(self.iter_content(CONTENT_CHUNK_SIZE)) or bytes()

            except AttributeError:
                self._content = None

        self._content_consumed = True
        return self._content

    @property
    def text(self):
        """Content of the response, in unicode.

        if Response.encoding is None and chardet module is available, encoding
        will be guessed.
        """

        # Try charset from content-type
        content = None
        encoding = self.encoding

        # Fallback to auto-detected encoding.
        if self.encoding is None:
            if chardet is not None:
                encoding = chardet.detect(self.content)['encoding']

        # Decode unicode from given encoding.
        try:
            content = str(self.content, encoding, errors='replace')
        except LookupError:
            # A LookupError is raised if the encoding was not found which could
            # indicate a misspelling or similar mistake.
            #
            # So we try blindly encoding.
            content = str(self.content, errors='replace')

        return content

    @property
    def json(self):
        """Returns the json-encoded content of a request, if any."""
        try:
            return json.loads(self.text or self.content)
        except ValueError:
            return None

    def raise_for_status(self, allow_redirects=True):
        """Raises stored :class:`HTTPError` or :class:`URLError`, if one occurred."""

        if self.error:
            raise self.error

        if (self.status_code >= 300) and (self.status_code < 400) and not allow_redirects:
            http_error = HTTPError('%s Redirection' % self.status_code)
            http_error.response = self
            raise http_error

        elif (self.status_code >= 400) and (self.status_code < 500):
            http_error = HTTPError('%s Client Error' % self.status_code)
            http_error.response = self
            raise http_error

        elif (self.status_code >= 500) and (self.status_code < 600):
            http_error = HTTPError('%s Server Error' % self.status_code)
            http_error.response = self
            raise http_error
