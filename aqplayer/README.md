## aqplayer

Play an audio.AudioQuantum using PyAudio

**Problem**
Before creating Aqplayer I could not play audio in Python directly. You had to output a whole new audio file, but I needed to play music in real time in order to replicate the InfiniteJukebox for an S-STEM research project. After Dr.Parry helped us figuring out how to index wav files and how to feed frames to a Pyaudio stream, I wanted to package it up into its own class. I did this so I would not have to repeat code and in hopes that others could use it.


**Process**

Aqplayer first creates a Pyaudio object. It then opens a Pyaudio stream with the wav file associated with the 'echonest.remix.audio.LocalAudioFile'. Aqplayer then calculates the frames associated with the given quantum and feeds them to the stream to be played.


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

**Code Explanation**

In the initializer, aqplayer first creates a pyaudio object. It then retrieves the wave file associated with the 'echonest.remix.audio.LocalAudioFile' and opens it using the built in wave module. After opening the wave, a stream is opened using the pyaudio object. The parameters used to open the stream are retrieved from the wave file.
```python
    def __init__(self, audio_file):
        self.p = pyaudio.PyAudio()
        self.af = audio_file
        self.wf = wave.open(self.get_wav(), 'rb')
        self.stream = self.p.open(format=self.p.get_format_from_width(self.wf.getsampwidth()),
                                channels=self.af.numChannels, rate=self.af.sampleRate, output=True)
```
To find the start of the wave frames to be fed to the stream, aqplayer multiplies the starting time of the 'echonest.remix.audio.AudioQuantum' by the wave framerate. To calculate the number of frames, aqplayer multiplies the duration of the 'echonest.remix.audio.AudioQuantum' by the wave framerate. After these values are found, the position of the wave is set, and the frames read using wave's readframes method. These frames are written to the stream to be played.
```python
    def play(self, AudioQuantum, intro=True):
        """
        Accepts any echonest.remix.audio.AudioQuantum and audibly plays it for you.
        If the AudioQuantum is the first one present, it will play any frames before
        it's start time. To turn this off, set intro=False.
        """
        index = AudioQuantum.absolute_context()[0]
        if index == 0 and intro== True:
            numframes = int((AudioQuantum.duration + AudioQuantum.start) * self.wf.getframerate())
            startframe = 0
        else:
            numframes = int(AudioQuantum.duration * self.wf.getframerate())
            startframe = int(AudioQuantum.start * self.wf.getframerate())
        self.wf.setpos(startframe)
        self.stream.write(self.wf.readframes(numframes))
```
Make sure to close the pyaudio stream when you are done by calling the closeStream() method.
