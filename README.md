# PythonEchonestRemix

Files that may help you interact with echonest


## aqplayer

Play an audio.AudioQuantum using PyAudio

**Process**

Aqplayer first creates a pyaudio object. It then opens a pyaudio stream with the wav file associated with the 'echonest.remix.audio.LocalAudioFile'. Aqplayer then calculates the frames associated with the given quantum and feeds them to the stream to be played. For more detail, refer to the DESCRIPTION.md.


**Dependencies**

To use aqplayer.py, you will need:

      - pyaudio
      - ffmpeg 

**Example**

Simply initialize the aqplayer with an 'echonest.remix.audio.LocalAudioFile'.
Then you can feed it any type of AudioQuantum to be played.
```python
import echonest.remix.audio as audio
from aqplayer import Player

audio_file = audio.LocalAudioFile("15 Sir Duke.m4a")
bars = audio_file.analysis.bars

aqplayer = Player(audio_file) #creates a Player given an 'echonest.remix.audio.LocalAudioFile'

for bar in bars:
    aqplayer.play(bar) #give play() any 'echonest.remix.audio.AudioQuantum' to be played (section, bar, beat, etc...)

aqplayer.closeStream() #close the audiostream when done
```

##BeatDistance

Beat Distance is static and used to compare two 'echonest.remix.audio.AudioQuantum' of kind 'beat'.
The only method that should ever be called is get_beat_distance()

**Example**

```python
import echonest.remix.audio as audio
import BeatDistance

audio_file = audio.LocalAudioFile("MP3Songs/15 Sir Duke.m4a")
beats = audio_file.analysis.beats

beat1 = beats.__getitem__(0)
beat2 = beats.__getitem__(1)

print BeatDistance.get_beat_distance(beat1, beat2)
```

