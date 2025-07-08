import requests


class RequestHandler:
    def __init__(self, base_url):
        self.url = base_url

    def post_request(self, json_content:object, post_url:str):
        """
        json_content : Any | object to be sent through the request

        post_url : str | self.url + post_url -> intended destination
        """
        req = requests.post(
            url=post_url,json=json_content
        )
        
        return req
    
    def get_request(self, get_url:str):
        """
        get_url : str | self.url + get_url -> intended destination
        """
        req = requests.get(
            url = self.url + get_url
        )
        
        return req
    
