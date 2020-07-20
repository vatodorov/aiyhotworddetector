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

import time
import queue
import miasnowboydecoder

import aiy._drivers._recorder

# Global variables. They are lazily initialized.
_voicehat_recorder = None

class miaAudio(object):
    """A processor that queues up sound from the voicehat."""

    def __init__(self):
        self._audio_queue = queue.Queue()

    def add_data(self, data):
        self._audio_queue.put(data)

    def is_done(self):
        return
        
    def __enter__(self):
        return self

    def __exit__(self, *args):
        return
        
    def getAudio(self):
        data = self._audio_queue.get()
        return data

class miaHotword:
    def __init__(self):
      ############# MODIFY THE FOLLOWING #############
      model_file='./resources/ok_kick.pmdl' # put your hotword file here. if you want to just try out use ./resources/snowboy.umdl
      sensitivity = 0.5
      ############### END OF MODIFY ##################
      self.detection = miasnowboydecoder.HotwordDetector(model_file, sensitivity=sensitivity)
      
    def waitForHotword(self,recorder, voice_only, seconds):
      if voice_only:
        print('waiting for voice')
        if seconds  > 0:
          revert2hotword=time.time() + seconds  
      else:
        print('waiting for hotword')
      sleep_time=0.03
      audio=miaAudio()
      recorder.add_processor(audio)
      while True:  
          data=audio.getAudio()
          if len(data) == 0:
            time.sleep(sleep_time)
            continue
          ans = self.detection.detector.RunDetection(data)
          if ans > 0:
            print('Hotword Detected!')
            break
          elif ans==0:
            if voice_only:
              break
          if voice_only and seconds > 0 and time.time() > revert2hotword:
            print('sleeping')
            voice_only=False
      recorder.remove_processor(audio)
       
def get_recorder():
    """Returns a driver to control the VoiceHat microphones.

    The aiy modules automatically use this recorder. So usually you do not need to
    use this.
    """
    global _voicehat_recorder
    if _voicehat_recorder is None:
        _voicehat_recorder = aiy._drivers._recorder.Recorder()
    return _voicehat_recorder

if __name__ == '__main__':
    MiaHot=miaHotword()
    recorder=get_recorder()
    recorder.start()
    MiaHot.waitForHotword(recorder,True, 4)
    MiaHot.waitForHotword(recorder,False,0)
    MiaHot.waitForHotword(recorder,True, 0)
    
    
