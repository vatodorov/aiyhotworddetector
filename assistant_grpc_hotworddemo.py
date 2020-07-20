"""A demo of the Google Assistant GRPC recognizer with hotword activation."""
#!/usr/bin/env python3
# Copyright 2017 Cyber-Renegade.
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

import logging
import miaHotword

import aiy.assistant.grpc
import aiy.audio
import aiy.voicehat

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
)

def main():
    voice_only=False
    seconds=0
    status_ui = aiy.voicehat.get_status_ui()
    status_ui.status('starting')
    assistant = aiy.assistant.grpc.get_assistant()
    miaHot=miaHotword.miaHotword()
    with aiy.audio.get_recorder() as recorder:
        while True:
            status_ui.status('ready')
            miaHot.waitForHotword(recorder,voice_only,seconds)
            status_ui.status('listening')
            print('Listening...')
            text, audio = assistant.recognize()
            if text is not None:
                if text == 'goodbye':
                    status_ui.status('stopping')
                    print('Bye!')
                    break
                print('You said "', text, '"')
            if audio is not None:
                aiy.audio.play_audio(audio)
            # if you don't want to repeat the hotward after the first time set the voice only to True
            # the seconds value means that the after waiting that amount of time the box will go back
            # to sleep and the hotword will be required again
            # voice_only=True
            # seconds = 3 

if __name__ == '__main__':
    main()
