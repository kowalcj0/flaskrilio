# -*- coding: utf-8 -*-
import os
from flask import Flask
from flask import request
#from flask import session
#from flask import g
#from flask import redirect
#from flask import url_for
from flask import send_from_directory
#from flask import abort
from flask import render_template
#from flask import flash

# Flask app Configuration
app = Flask(__name__)
app.config.from_object(__name__)
app.debug = True


def get_twiml(twiml):
    """Will safely check if requested twiml file exists!"""
    try:
        with open("twimls/%s" % twiml):
            print "responding with %s" % twiml
            return send_from_directory('twimls', filename=twiml)
    except IOError:
        return render_template('404.xml'), 404


def print_request_details(request):
    if request.method == 'POST':
        print "All POST Req. data: %s" % request.data
        print "All POST params: %s" % request.args
        print "All POST Hdrs.: \n\n%s\n\n" % request.headers
    if request.method == 'GET':
        print "GET CallSid: %s" % request.args.get("CallSid")
        print "All GET params: %s" % request.args
        print "All GET Hdrs.: \n\n%s\n\n" % request.headers


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@app.route('/', methods=['POST', 'GET'])
def show_entries():
    return ("Welcome to Flaskrilio! A simple http server for handling Twilio "
            "requests")


@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'


@app.route('/vru', methods=['POST', 'GET'])
@app.route('/vfu', methods=['POST', 'GET'])
@app.route('/scu', methods=['POST', 'GET'])
@app.route('/mru', methods=['POST', 'GET'])
def respond_with_default_twiml():
    """Will respond with a default twiml message"""
    print_request_details(request)
    ctx = str(request.url_rule).replace("/", "")
    return get_twiml("%s-default.xml" % ctx)


@app.route('/vru/<twiml>', methods=['POST', 'GET'])
@app.route('/vfu/<twiml>', methods=['POST', 'GET'])
@app.route('/scu/<twiml>', methods=['POST', 'GET'])
@app.route('/mru/<twiml>', methods=['POST', 'GET'])
def respond_with_twiml(twiml):
    """Will respond with a specified twiml file"""
    print_request_details(request)
    return get_twiml(twiml)


if __name__ == '__main__':
    if os.environ.get('ENV') is not None:
        if os.environ['ENV'] == 'EC2':
            from helpers import get_public_ip
            ip = get_public_ip()
            print "My public IP address is: %s" % ip
            app.run(host='0.0.0.0', port=80)
    else:
        app.run()
