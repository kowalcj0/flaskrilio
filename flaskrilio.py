#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
from flask import Flask
from flask import request
#from flask import session
from flask import g
#from flask import redirect
#from flask import url_for
from flask import send_from_directory
#from flask import abort
from flask import render_template
from flask import flash
from flask import jsonify
from contextlib import closing
import sqlite3

# Flask app Configuration
DATABASE = 'twilio.db'
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()


def dict_from_row(cur):
    """Transforms sqlite3 result cursor into dictionary"""
    colname = [ d[0] for d in cur.description ]
    result_dict = [ dict(zip(colname, r)) for r in cur.fetchall() ]
    return result_dict


def get_twiml(twiml):
    """Will safely check if requested twiml file exists!"""
    try:
        with open("twimls/%s" % twiml):
            print "responding with %s" % twiml
            return send_from_directory('twimls', filename=twiml)
    except IOError:
        return render_template('404.xml'), 404


def print_request_details(request):
    print "All REQ Cookies: %s" % request.cookies
    if request.method in ['POST', 'PUT']:
        print "All POST Values: %s" % request.values
        print "All POST Form: %s" % request.form
        print "All POST Req. data: %s" % request.data
        print "All POST params: %s" % request.args
        print "All POST Hdrs.: \n%s\n" % request.headers
    if request.method == 'GET':
        print "GET CallSid: %s" % request.args.get("CallSid")
        print "All GET Values: %s" % request.values
        print "All GET params: %s" % request.args
        print "All GET Hdrs.: \n%s\n" % request.headers


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    g.db.close()


@app.route('/', methods=['POST', 'GET'])
def get_gome():
    payload = {
        "msg" : "Welcome to Flaskrilio! A simple http server for handling Twilio requests"
    }
    return jsonify(payload)


@app.route('/shutdown', methods=['POST', 'GET'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'


@app.route('/vru', methods=['POST', 'GET'])
@app.route('/vfu', methods=['POST', 'GET'])
@app.route('/scu', methods=['GET'])
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


# handle Twilio's Status Callback requests separetely
@app.route('/scu', methods=['POST'])
def handle_scu():
    if request.form.get('CallStatus') is not None:
        print "adding to DB"
        duration = int(request.form.get('CallDuration')) if request.form.get('CallDuration') is not None else 0
        print duration
        g.db.execute('insert into calls \
                     (FromNo, \
                     ToNo, \
                     Caller, \
                     Called, \
                     AccountSid, \
                     CallSid, \
                     Direction, \
                     CallStatus, \
                     CallDuration) \
                     values (?, ?, ?, ?, ?, ?, ?, ?, ?)', \
                    [request.form.get('From'), \
                     request.form.get('To'), \
                     request.form.get('Caller'), \
                     request.form.get('Called'), \
                     request.form.get('AccountSid'), \
                     request.form.get('CallSid'), \
                     request.form.get('Direction'), \
                     request.form.get('CallStatus'), \
                     duration])
        g.db.commit()
        print 'New call status record was successfully added to db'
    return "", 204


@app.route('/calls', methods=['GET'])
def show_calls():
    cur = g.db.execute('select * from calls order by id desc')
    calls = dict_from_row(cur)
    for c in calls:
        print c
    return jsonify({ 'calls' : calls })


if __name__ == '__main__':
    if os.environ.get('ENV') is not None:
        if os.environ['ENV'] == 'EC2':
            from helpers import get_public_ip
            ip = get_public_ip()
            init_db()
            print "My public IP address is: %s" % ip
            app.run(host='0.0.0.0', port=80)
    else:
        init_db()
        app.run(debug=True)

