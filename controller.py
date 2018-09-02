from multiprocessing import Process, Pipe
import SimpleHTTPServer
import SocketServer
import sys


# Server parameters
PORT = 8000


# Custom handler built on top of SimpleHTTPRequestHandler class
class Handler(SimpleHTTPServer.SimpleHTTPRequestHandler):
   # Service GET Request
   def do_GET(self):
      SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

   # Service POST Request
   def do_POST(self):
      print 'POST Received'
      content_length = int(self.headers['Content-Length'])
      body = self.rfile.read(content_length)
      print 'Body: ' + body
      self.send_response(200)
      self.end_headers()

   # Log each request
   # def log_message(self, format, *args):
   #    return







def f(conn):
   conn.send([42, None, 'hello'])
   conn.close()

# Main method
if __name__ == '__main__':
   parent_conn, child_conn = Pipe()
   p = Process(target=f, args=(child_conn,))
   p.start()
   print parent_conn.recv()   # prints "[42, None, 'hello']"
   p.join()
   
   try:
      # Run server
      httpd = SocketServer.TCPServer(("", PORT), Handler)
      print "serving at port", PORT                                                                                                                                  
      httpd.serve_forever()
   except KeyboardInterrupt:
      # Exit cleanly on CTRL-C
      httpd.shutdown()
      sys.exit()