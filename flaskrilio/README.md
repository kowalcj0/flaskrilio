# Flaskrilio
-----------------------------
Flaskrilio - is a simple python project combined of two main modules:
* a [Flask](http://flask.pocoo.org/) based HTTP server that handles Twilio's requests 
* and [Behave](http://pythonhosted.org/behave/) tests


The goal of the Behave part is to verify that CallConnect & Twilio services are up and running.


## Starting Flaskrilio server
./flaskrilio_srv.py
or
python flaskrilio_srv.py


## Running tests
behave
behave -v
behave --junit
behave -v -n "name of selected scenario"
NGROK="http://3070dd9.ngrok.com" behave -v
NGROK="http://3070dd9.ngrok.com" ENV=POC behave -v --junit

# Run tests with multiple reporters
NGROK="http://janusz.ngrok.com" behave --junit -f tags -f tags.location -f steps.usage
this will generate junit like report files and few more console based reports 

## running tests locally
To run your tests locally you will need 2 things:
* a public hostname available via [ngrok](http://ngrok.com)
* running flaskrilio_srv

First start ngrok:

    ngrok 5000

copy the http hostname (we'll need it later)

Second, start flaskrilio_srv

    ./flaskrilio_srv.py

Then you can run behave tests:

    behave -v --junit --junit-directory "./reports"


## running tests on Jenkins


