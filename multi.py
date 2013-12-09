from multiprocessing import Process, Pipe
import logging
import os
import sys
from time import sleep

# Set Path
pwd = os.path.abspath(os.path.dirname(__file__))
project = os.path.basename(pwd)
new_path = pwd.strip(project)
activate_this = os.path.join(new_path, 'flaskr')
sys.path.append(activate_this)

from flaskrilio import app


def run_app():
    while True:
        print "started the app"
        sleep(5)
        print "I slept for 5 secs :) "

def run_server(conn):
    conn.send([42, None, 'hello'])
    conn.close()
    app.run(host='127.0.0.1', port=8088, debug=True)

def main():
    parent_conn, child_conn = Pipe()

    client = Process(target=run_app)
    client.start()

    server = Process(target=run_server, args=(child_conn,))
    server.start()

    print parent_conn.recv()

    client.join()
    server.terminate()

if __name__ == "__main__":
    main()
