#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect
import os
from subprocess import Popen
import logging

logger = ''
process = None
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def run_command(command):
    logger.debug("Starting a process")
    global process
    if type(process) == Popen:
        stop_process()
    process = Popen(command.split(' '))
    pid = process.pid
    logger.info(f'Started process: {command} with pid: {pid}')

def stop_process():
    logger.debug("Stopping a process")
    global process
    try:
        pid = process.pid
        process.kill()
        ret = process.returncode
        process = None
        logger.info(f'Killing process {pid}, exited with {ret}')
    except:
        logger.warning(f'Could not kill process')
        pass

@app.route('/rain', methods = ['POST'])
def rain():
    command = "play -q -n synth brownnoise synth pinknoise mix synth sine amod 0.1 20"
    run_command(command)
    return redirect('/')

@app.route('/waves', methods = ['POST'])	
def waves():
    command = "play -q -n synth brownnoise synth pinknoise mix synth sine amod 0.6 20"
    run_command(command)
    return redirect('/')

@app.route('/whitenoise', methods = ['POST'])	
def whitenoise():
    command = "play -q -n synth brownnoise synth pinknoise mix"
    run_command(command)
    return redirect('/')

@app.route('/stop', methods = ['POST'])	
def stop():
    stop_process()
    return redirect('/')


loglevel = os.getenv('LOGLEVEL', 'DEBUG').upper()
logging.basicConfig(format='%(asctime)s-%(name)s-%(levelname)s-%(message)s', level=loglevel)
logger = logging.getLogger('noisemachine')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
