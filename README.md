# PythonEchonestRemix

Files that may help you interact with echonest\n\n


## aqplayer
**Dependencies**

To use aqplayer.py, you will need:

      - pyaudio
      - wave 

**Example**

Simply initialize the aqplayer with a wav file.
Then you can feed it any type of AudioQuantum to be played.
```python
__author__ = 'lukestack'

import echonest.remix.audio as audio
from aqplayer import player

"""
If you do not have the wav file, you can create one using pydub.AudioSegment(see code below)
    from pydub import AudioSegment
    audio_segment = AudioSegment.from_file(inuput_file)
    audio_segment.export(output_file, format="wav")
"""

wav_file = "WAVSongs/15 Sir Duke.wav"
audio_file = audio.LocalAudioFile("MP3Songs/15 Sir Duke.m4a") #you want to give echonest the compressed audiofile to analyze
bars = audio_file.analysis.bars

aqplayer = player(wav_file) #file must be wav

aqplayer.play(bars.__getitem__(5)) #give play() any AudioQuantum to be played (section, bar, beat, etc...)

aqplayer.closeStream() #close the audiostream when done
```

