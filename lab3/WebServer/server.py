import socket
import os.path
import threading


class WebServer:
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 8080
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            while True:
                conn, addr = s.accept()
                request = MyHttpRequest(conn)
                thread = threading.Thread(target=request.process_request)
                thread.start()


class MyHttpRequest:
    def __init__(self, connection):
        self.connection = connection
        self.CRLF = "\r\n"

    def process_request(self):
        data = self.connection.recv(1024).decode("utf-8")
        filename = data.split()[1][1:]
        file_exists = os.path.isfile(filename)

        result_str = self.create_response(filename, file_exists)
        result_bytes = bytes(result_str, "utf-8")
        self.connection.sendall(result_bytes)
        self.connection.close()

    def create_response(self, filename, file_exists):
        if file_exists:
            status_line = "HTTP/1.0 200 OK" + self.CRLF
            content_type_line = "Content-Type: " + \
                                self.content_type(filename) + self.CRLF
            entity_body = ""
        else:
            status_line = "HTTP/1.0 404 Not Found" + self.CRLF
            content_type_line = "Content-Type: text/html" + self.CRLF
            entity_body = "<HTML>" + \
                          "<HEAD><TITLE>Not Found</TITLE></HEAD>" + \
                          "<BODY>Not Found</BODY></HTML>"
        result_str = status_line + content_type_line + self.CRLF

        if file_exists:
            with open(filename, 'r') as file:
                result_str += file.read()
        else:
            result_str += entity_body

        return result_str

    @staticmethod
    def content_type(filename):
        ext = filename.split('.')[-1]
        if ext == "htm" or ext == "html":
            return "text/html"

        if ext == "ram" or ext == "ra":
            return "audio/x-pn-realaudio"

        return "application/octet-stream"


if __name__ == '__main__':
    WebServer()

