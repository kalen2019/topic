#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""A demo of the Google CloudSpeech recognizer."""
import locale
import logging
import sys
import os
import time

from google.assistant.library.event import EventType
from aiy.assistant import auth_helpers
from aiy.assistant.library import Assistant

from aiy.board import Board, Led
from aiy.voice import audio
from gtts import gTTS
from pydub import AudioSegment
rc = ""
e = 0
def locale_language():
    language, _ = locale.getdefaultlocale()
    return language

def say(text):
    tts = gTTS(text, lang='zh-TW')
    tts.save('output.mp3')
    sound = AudioSegment.from_mp3('output.mp3')
    sound.export('output.wav', format='wav')
    audio.play_wav('output.wav')

def main():

    logging.basicConfig(level=logging.INFO)

    credentials = auth_helpers.get_assistant_credentials()
    with Board() as board, Assistant(credentials) as assistant:
        for event in assistant.start():
            process_event(board.led, assistant, event)
 
def process_event(led, assistant, event):
    logging.info(event)
    remote_name = ['mbot', 'temp']
    mbot = ['前進','後退','左轉','右轉','紅外線','超聲波','循線','轉圈圈']
    mbot_r = ['前進中','後退中','左轉','右轉','紅外線模式','超聲波模式','循線模式','轉圈圈']
    mbot_m = ['FORWARD','BACK','LEFT','RIGHT','A','B','C']
    temp = ['開冷氣','關冷氣','上升溫度','下降溫度']
    temp_r = ['開機','關機','上升了','下降了']
    temp_m = ['POWER','CLOSE','UP','DOWN']
    if event.type == EventType.ON_START_FINISHED:
        led.state = Led.BEACON_DARK  # Ready.
        logging.info('Say "OK, Google" then speak, or press Ctrl+C to quit...')

    elif event.type == EventType.ON_CONVERSATION_TURN_STARTED:
        led.state = Led.ON  # Listening.

    elif event.type == EventType.ON_END_OF_UTTERANCE:
        led.state = Led.PULSE_QUICK  # Thinking.

    elif event.type == EventType.ON_RECOGNIZING_SPEECH_FINISHED:
        text = event.args['text']
        time.sleep(1)
        assistant.stop_conversation()
        time.sleep(1)
        if text in mbot:
            assistant.stop_conversation()
            s = mbot.index(text)
            RmN = remote_name.index('mbot')
            if text == "轉圈圈":
                lirc_command = "irsend send_start " + remote_name[RmN] + " KEY_" + mbot_m[2]
                print(lirc_command)
                say(mbot_r[s])
                print("Assistant : " + mbot_r[s])
                os.system(lirc_command)
                time.sleep(4)
                lirc_command = "irsend send_stop " + remote_name[RmN] + " KEY_" + mbot_m[2]
                print(lirc_command)
                os.system(lirc_command)
                lirc_command = "irsend send_start " + remote_name[RmN] + " KEY_" + mbot_m[3]
                print(lirc_command)
                #say(mbot_r[s])
                print("Assistant : " + mbot_r[s])
                os.system(lirc_command)
                time.sleep(4)
                lirc_command = "irsend send_stop " + remote_name[RmN] + " KEY_" + mbot_m[3]
                print(lirc_command)
                os.system(lirc_command)
            else:
                lirc_command = "irsend send_start " + remote_name[RmN] + " KEY_" + mbot_m[s]
                print(lirc_command)
                say(mbot_r[s])
                print("Assistant : " + mbot_r[s])
                os.system(lirc_command)
                time.sleep(1)
                lirc_command = "irsend send_stop " + remote_name[RmN] + " KEY_" + mbot_m[s]
                print(lirc_command)
                os.system(lirc_command)
            assistant.start_conversation()
        elif text in temp:
            #assistant.stop_conversation()
            t = temp.index(text)
            RmN = remote_name.index('temp')
            lirc_command = "irsend send_once " + remote_name[RmN] + " KEY_" + temp_m[t]
            print(lirc_command)
            say(temp_r[t])
            print("Assistant : " + temp_r[t])
            os.system(lirc_command)
            time.sleep(1)
            assistant.start_conversation()
        elif '再見' in text:
            global rc 
            rc = text
    elif event.type == EventType.ON_RENDER_RESPONSE:
        text = rc
        if '再見' in text:
            global e
            e = 1
    elif event.type == EventType.ON_RESPONDING_FINISHED:
        if e == 1 :
            sys.exit(1)
    elif (event.type == EventType.ON_CONVERSATION_TURN_FINISHED 
          or event.type == EventType.ON_CONVERSATION_TURN_TIMEOUT
          or event.type == EventType.ON_NO_RESPONSE):
        led.state = Led.BEACON_DARK
    elif event.type == EventType.ON_ASSISTANT_ERROR and event.args and event.args['is_fatal']:
        print(event.args)
        sys.exit(1)
        



if __name__ == '__main__':
    main()