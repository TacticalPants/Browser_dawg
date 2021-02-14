
def request(url):
    #connects to url with 'socket' feature, parses header
    #and parses the body of the url
    import socket
    import ssl

    if url[4]=='s':
        scheme='https'
    else:
        scheme='http'

    url = url[len("http://"):] 

    if ":" in url:
        url, port = url.split(":", 1)

    burl = url.encode()
    s = socket.socket(
        family=socket.AF_INET,
        type=socket.SOCK_STREAM,
        proto=socket.IPPROTO_TCP,
    )
    if scheme == "https":
        ctx = ssl.create_default_context()
        s = ctx.wrap_socket(s, server_hostname=path)
    s.connect((url, 80))

    s.send(b"GET /index.html HTTP/1.0\r\n" + 
        b"Host: " +
        burl +
        b"\r\n\r\n")

    response = s.makefile("r", encoding="utf8", newline="\r\n")
    statusline = response.readline()
    version, status, explanation = statusline.split(" ", 2)
    assert status == "200", "{}: {}".format(status, explanation)  

    headers = {}
    while True:
        line = response.readline()
        if line == "\r\n": break
        header, value = line.split(":", 1)
        headers[header.lower()] = value.strip()

    body = response.read()
    s.close()
    return headers, body

def show(body):
    #prints the body of the html and strips the tags
    #there is probably a much more elegant way to do this
    web_body=[]
    str1=""
    in_angle = False
    for c in body:
        if c == "<":
            in_angle = True
        elif c == ">":
            in_angle = False
        elif not in_angle:
            web_body.append(c)
            return str1.join(web_body)



if __name__ == "__main__":
    import sys
    headers, body = request(sys.argv[1])
    show(body)
