from flask import Flask
from flask import request
#from flask import session
#from flask import g
#from flask import redirect
#from flask import url_for
from flask import send_from_directory
#from flask import abort
#from flask import render_template
#from flask import flash

# Flask app Configuration
app = Flask(__name__)
app.config.from_object(__name__)
app.debug = True


@app.route('/')
def show_entries():
    #return render_template('show_entries.html', entries=entries)
    return "Welcome"


@app.route('/callback', methods=['POST'])
def twilio_callback():
    #return redirect(url_for('show_entries'))
    if request.method == 'POST':
        print "Req.: %s" % request.data
        return "Req.: %s" % request.data


@app.route('/callback/<twiml>', methods=['POST', 'GET'])
def return_callback_twilml(twiml):
    if request.method == 'POST':
        print "POST CallSid: %s" % request.args.get("CallSid")
        print "All POST Req. data: %s" % request.data
        print "All POST params: %s" % request.args
        print "All POST Hdrs.: \n\n%s\n\n" % request.headers
        return send_from_directory('twimls', filename=twiml)
    if request.method == 'GET':
        print "GET CallSid: %s" % request.args.get("CallSid")
        print "All GET params: %s" % request.args
        print "All GET Hdrs.: \n\n%s\n\n" % request.headers
        return send_from_directory('twimls', filename=twiml)


if __name__ == '__main__':
    app.run()
    # run as root to listen on port 80
    #app.run(host='0.0.0.0', port=80)
