#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect
import os
import re
from subprocess import Popen, PIPE
import logging
import alsaaudio

logger = ''
process = None
mixer = alsaaudio.Mixer(control='Speaker')
app = Flask(__name__)

@app.route('/')
def index():
    volume = mixer.getvolume()[0]
    # getmute: 0 means not muted, 1 means muted.
    muted = not mixer.getmute()[0]

    #amixer = Popen("/usr/bin/amixer sget Speaker".split(' '), stdout=PIPE)
    #amixer.wait()
    #stdout = str(amixer.stdout.read())
    #volume_re = re.search("\[([0-9]+)\%\]", stdout)
    #if len(volume_re.groups()) > 0:
    #    volume = volume_re.group(1)
    #else:
    #    volume = '50'
    #muted_re = re.search("\[(on)\]", stdout)
    #if muted_re and len(muted_re.groups()) > 0:
    #    muted = False 
    #else:
    #    muted = True
    return render_template('index.html', volume=volume, muted=muted)

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

@app.route('/setvolume')
def setvolume():
    volume = request.args.get("volume")
    mixer.setvolume(int(volume))
    return f'Set volume to {volume}'
    #command = f'amixer set Speaker {volume}% unmute'
    #amixer = Popen(command.split(' '), stdout=PIPE)
    #retcode = amixer.wait()
    #if retcode == 0:
    #  return f'Set value to {volume}'
    #else:
    #  return f'Could not set volume'

@app.route('/unmute')
def unmute_volume():
    mixer.setmute(0)
    return 'Unmuted'
    #command = "amixer set Speaker unmute"
    #amixer = Popen(command.split(' '), stdout=PIPE)
    #retcode = amixer.wait()
    #if retcode == 0:
    #  return f'Unmuted'
    #else:
    #  return f'Could not unmute'

@app.route('/mute')
def mute_volume():
    mixer.setmute(1)
    return 'Muted'
    #command = "amixer set Speaker mute"
    #amixer = Popen(command.split(' '), stdout=PIPE)
    #retcode = amixer.wait()
    #if retcode == 0:
    #  return f'Muted'
    #else:
    #  return f'Could not mute'
    #return ""

loglevel = os.getenv('LOGLEVEL', 'DEBUG').upper()
logging.basicConfig(format='%(asctime)s-%(name)s-%(levelname)s-%(message)s', level=loglevel)
logger = logging.getLogger('noisemachine')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
