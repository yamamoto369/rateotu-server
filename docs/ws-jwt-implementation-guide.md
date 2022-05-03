Authentication with JWT over Websockets (from personal experience)
===========

**Cliff Notes and How it Works?**
JWT token is only validated once by the server when the initial websocket message
(WebSocket handshake) containing a token is sent by the client, after that the server is unaware of the token.

The websocket connection is kept alive as long as we keep the server running and a browser/tab
is not refreshed on the client side.

The server will not close the connection when a token expires because its unaware of the token
after the intial handshake is done.

From client perspective, the server will close a connection when a user closes his browser/tab, power outage or anything
that terminates a connection from the client side. If this happens, the client has to reconnect, and the whole process from above repeats.

**Issue regarding JWT websocket authentication**
The Javascript WebSocket API implemented in the browsers doesn't support sending anything through the headers (altough the WebSockets protocol itself supports), [see](https://stackoverflow.com/questions/4361173/http-headers-in-websockets-client-api). All they have control over is the URL and the websocket subprotocols sent [see](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket) There aren't really a lot of options when it comes to connecting to a WebSocket via a browser. Firstly, the request has to be done via HTTP GET request, which then gets upgraded to a WebSocket protocol. There is no option to do this via a POST request. When using HTTP/HTTPS, query params in URLs can get stored in places such as proxy server logs, browser history,etc. However, neither of those concerns apply to websockets (a browser won't keep history of the connections made by a HTML page) as the connection itself is initiated by the JS client, nor is possible to open ws connection manually from the browser. However, probably there are 3rd party tools that can inspect a page connections/headers to get access to all network calls on the page, that's why the SSL is the only real solution in this case along with the lower token expiration time. **The best long-term options are: switching to the session auth, or an another  more complex token authentican methods (JWT FUCKING SUCKS).**

Possible Options Overview

1. Between these tradoffs, I opted for attaching a token in the URL as a query string. With SSL encryption, this theoretically isn't unsafe since the URL is encrypted along with the rest of the request. Ideally, secrets like API keys or authentication Tokens would be sent though the request header or even the request body.

2. Second option is using the "Sec-WebSocket-Protocol" header to attach the JWT token in the sub-protocol selected list. Also unrecommended and unsual way of doing things, but possible option.

3. Also, another option is to perform the authentication once the websocket connection is established. The JWT token can be sent as the first message to the server and if it is invalid, the server can terminate the connection. Basically, anyone can connect, but then the client needs to validate itself afterwards in order to recieve a data. But this comes with a overhead of completing the websocket handshake for each request which is sorta expensive operation, and we would be on the mercy of the client to respect the rules.

The Chosen WebSocket Auth Solution:

1. Attach the JWT token as a query parameter on the client side when connecting to the ws endpoint
2. Check the token on the server and act appropriately
3. Add SSL in production (REST/https and WebSockets/wss)
4. Set JWT expire time to reasonable amount; to add another layer of security
5. Add CORS
6. **Since JWTs are managed at the client application level, each client application (web/desktop/mobile) must
implement storage, expiry and renewal of JWTs. This is a significant, security-sensitive responsibility.
Therefore, in order to bypass issues mentioned above regarding the JWT token expiration using the WebSocket communication, the client
is required to check for the token expiration and redirect a user to a desired page when the token is about to expire;this will close all active ws connections on that page.**

!!! info
    **CONCLUSION:** JWT SUCKS and it's pain in the ass to implement correctly (if even possible)!
