import requests


class HttpClient:

    def __init__(self, server, headers=None, proxies=None):
        self.__server = server
        self.__session = requests.Session()
        self.__session.headers = headers
        self.__session.proxies = proxies

    def get(self, uri):
        return self.__send_request('GET', uri)

    def post(self, uri, json=None, data=None):
        return self.__send_request('GET', uri, data=data, json=json)

    def authorize_bearer(self, uri, login, password):
        body = 'grant_type=password&username={0}&password={1}'.format(login,password)
        response = self.post(uri, data=body)
        self.__update_header('Authorization', 'Bearer ' + response['access_token'])

    def __update_header(self, key, value):
        self.__session.headers[key] = value

    def __send_request(self, method, uri, data=None, json=None):
        server_uri = '{0}/{1}'.format(self.__server, uri)
        response = self.__session.request(method, url=server_uri, data=data, json=json)

        if response.status_code > 300:
            raise Exception('An error occured: {0}'.format(response.content))

        return response.json()


