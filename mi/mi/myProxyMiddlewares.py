import base64

# Start your middleware class
class MyProxyMiddleware(object):

    # overwrite process request
    def process_request(self, request, spider):

        # Set the location of the proxy
        request.meta['proxy'] = "http://124.88.67.10:843"
        # Use the following lines if your proxy requires authentication
        proxy_user_pass = "USERNAME:PASSWORD"
        # setup basic authentication for the proxy
        encoded_user_pass = base64.encodestring(proxy_user_pass)
        request.head0ers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass