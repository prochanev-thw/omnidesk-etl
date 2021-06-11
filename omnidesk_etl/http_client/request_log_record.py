class RequestLogRecord:

    def __init__(self, request):
        self._request = request

    def __str__(self):
        return '\nrequest\n------------\nmethod: {method}\nurl: {url}\nparams: {params}\n'.format(**self.args())

    def args(self):

        url, params = self._request.url.split('?')

        return {
            'method': self._request.method.upper(),
            'url': url,
            'params': params.split('&'),
        }


class ResponseLogRecord:

    def __init__(self, response):
        self._response = response

    def __str__(self):
        return '\nresponse\n------------\nmethod: {method}\nurl: {url}\nparams: {params}\
                \nstatus: {status}\napi_calls_left: {api_calls_left}\ntext: {text}\n'.format(**self.args())

    def args(self):

        url, params = self._response.url.split('?')

        return {
            'method': self._response.request.method.upper(),
            'url': url,
            'params': params.split('&'),
            'status': self._response.status_code,
            'api_calls_left': int(self._response.headers['api_calls_left']),
            'text': self._response.text if self._response.status_code != 200 else 'success'
        }
