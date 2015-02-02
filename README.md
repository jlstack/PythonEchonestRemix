# PythonEchonestRemix

Files that may help you interact with echonest


## aqplayer
**Process**

aqplayer first creates a pyaudio object. It then opens a pyaudio stream with the wav file associated with the 'echonest.remix.audio.LocalAudioFile'. aqplayer then calculates the frames associated with the given quantum and feeds them to the stream to be played.


**Dependencies**

To use aqplayer.py, you will need:

      - pyaudio
      - ffmpeg 

**Example**

Simply initialize the aqplayer with an 'echonest.remix.audio.LocalAudioFile'.
Then you can feed it any type of AudioQuantum to be played.
```python
__author__ = 'lukestack'

import echonest.remix.audio as audio
from aqplayer import player

audio_file = audio.LocalAudioFile("15 Sir Duke.m4a")
bars = audio_file.analysis.bars

aqplayer = player(audio_file) #creates a player given an 'echonest.remix.audio.LocalAudioFile'

for bar in bars:
    aqplayer.play(bar) #give play() any 'echonest.remix.audio.AudioQuantum' to be played (section, bar, beat, etc...)

aqplayer.closeStream() #close the audiostream when done
```

