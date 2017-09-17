import usocket
import ussl
import time
import ujson
import tools

def request(method, url, json=None, headers={}, retry_num=5, retry_min_msec=500):
    try:
        proto, dummy, host, path = url.split("/", 3)
    except ValueError:
        proto, dummy, host = url.split("/", 2)
        path = ""

    if proto == "http:":
        port = 80
    elif proto == "https:":
        port = 443
    else:
        raise ValueError("Unsupported protocol: " + proto)

    if ":" in host:
        host, port = host.split(":", 1)
        port = int(port)

    # open socket connection (try 5 times exponentially)
    retry = 0
    con_status, s = connect_socket(proto, host, port)
    while retry < retry_num and not con_status:
        time.sleep(pow(2, retry)*retry_min_msec/1000)
        #Debug
        #print("{} - retry: {}".format(tools.datetime_toIso(time.localtime()), retry) )
        con_status, s = connect_socket(proto, host, port)
        retry+=1
    if retry >= retry_num and not con_status:
        raise Exception("Socker Connection Error")

    # Send headers and body
    try:
        s.write(b"%s /%s HTTP/1.0\r\n" % (method, path))
        if not "Host" in headers:
            s.write(b"Host: %s\r\n" % host)
        # Iterate over keys to avoid tuple alloc
        for k in headers:
            s.write(k)
            s.write(b": ")
            s.write(headers[k])
            s.write(b"\r\n")
        if json:
            data = ujson.dumps(json)
            s.write(b"Content-Length: %d\r\n" % len(data))

        s.write(b"\r\n")
        if data:
            s.write(data)
    except Exception:
        raise Exception("enable to send data")
    else:
        l = s.readline()
        protover, status, msg = l.split(None, 2)
        status = int(status)
        #print("###########",protover, status, msg )

        #Read all headers fields
        while True:
            l = s.readline()
            if not l or l == b"\r\n":
                break
            if l.startswith(b"Transfer-Encoding:"):
                if b"chunked" in l:
                    raise ValueError("Unsupported " + l)
            elif l.startswith(b"Location:") and not 200 <= status <= 299:
                raise NotImplementedError("Redirects not yet supported")
        resp = {
        'body': s.read(),
        'status_code':  status,
        'reason': str(msg.rstrip())
        }
        #print("RESP: ", resp)
        return resp
    finally:
        s.close()

def connect_socket(proto, host, port):
    try:
        s = usocket.socket()
        if proto == "https:":
            s = ussl.wrap_socket(s, server_hostname=host)
        s.connect(usocket.getaddrinfo(host, port)[0][-1])
    except Exception as e:
        s.close()
        #Debug
        #print(e)
        return [False, s]
    else:
        return [True, s]
