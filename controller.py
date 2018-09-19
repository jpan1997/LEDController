from multiprocessing import Process, Pipe
import SimpleHTTPServer
import SocketServer
import sys
import time

# Server parameters
PORT = 8000

# Default controller settings
DEFAULT_SETTINGS = {
    'mode': 'mood',

    'color': 0.5,
    'brightness': 1,
    'speed': 1,
    'type': 'single',
    'flash': 'none',

    'threshold': 1.5,
    'moving average': 20,
    'pulsing': True,

    'smoothness': 0.5,
    'sensitivity': 1
}

# Each process has own copy of settings
settings = DEFAULT_SETTINGS.copy()


# Custom handler built on top of SimpleHTTPRequestHandler class
class Handler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    # Service GET Request
    def do_GET(self):
        if 'init' in self.path:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(settings))
        else:
            SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

    # Service POST Request
    def do_POST(self):
        try:
            # Load message
            body = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
        except:
            print 'WARNING: Invalid POST message received:', body
            return

        # Send response
        self.send_response(200)
        self.end_headers()

        # Update server settings
        update_settings(body, settings)

        # Send new settings to controller
        server_pipe.send(body)

    # Log each request
    # def log_message(self, format, *args):
    #    return


# Controller process
def controller(ctrl_pipe):

    # Control loop
    while True:

        changed_setting = None

        # Read messages from pipe
        if ctrl_pipe.poll():
            msg = ctrl_pipe.recv()
            update_settings(msg, settings)
            changed_setting = msg.keys()[0]    # Only one setting changed at a time

        # Mood mode
        if settings['mode'] == 'mood':
            # Single type
            if settings['type'] == 'single':
                if changed_setting == 'color' or changed_setting == 'brightness':
                    # Set all LEDS to settings['color'], settings['brightness']
                    print('MODE: MOOD, TYPE: SINGLE; color: ' + str(settings['color']) + ', brightness: ' + str(settings['brightness']))

            # Fade type
            elif settings['type'] == 'fade':
                

            # Gradient type
            elif settings['type'] == 'gradient':



        # Beat mode
        elif settings['mode'] == 'beat':

        # Frequency mode
        elif settings['mode'] == 'freq':



        # print 'controller running...'
        time.sleep(1)


def update_settings(src, dest):
    for key in src:
        if key in dest:
            dest[key] = src[key]
        else:
            print "WARNING: Invalid setting:", key


# Main method
if __name__ == '__main__':
    # Create Pipe
    server_pipe, ctrl_pipe = Pipe()

    # Spawn child controller process
    p = Process(target=controller, args=(ctrl_pipe,))
    p.start()

    # Run server
    httpd = SocketServer.TCPServer(("", PORT), Handler)
    print "serving at port", PORT

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        # Exit cleanly on CTRL-C
        httpd.shutdown()
        p.terminate()
        sys.exit()
