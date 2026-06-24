import http.server

#count how many reqwuests made in total
count = 0

# defines custom class for responding to requests
class R(http.server.BaseHTTPRequestHandler):
    
    def do_GET(self):
        global count
        count+=1
        print(f"Request #{count}")
        
        if count % 2 == 1:
            self.send_reponse(200)
            self.end_headers()
            self.wfile.write(b"Hello World!")
        else:
            self.send(301)
            self.send_header('Location', 'http://127.0.0.1:1337/secret')
            self.end_headers()
        
    def log_message(self, *args):
        pass

http.server.HTTPServer(('0.0.0.0', 8000), R).serve_forever()
# 0.0.0.0 = listen on all interfaces
# 8000 = port to listen on
# R = use our custom class to handle requests
# serve_forever() = keep running until ctrl+c
            
