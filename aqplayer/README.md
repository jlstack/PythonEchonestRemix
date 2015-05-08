## aqplayer

Play an audio.AudioQuantum using PyAudio

**Problem**

Before creating Aqplayer I could not play audio in Python directly. You had to output a whole new audio file, but I needed to play music in real time in order to replicate the InfiniteJukebox for an S-STEM research project. After Dr.Parry helped us figuring out how to index wav files and how to feed frames to a Pyaudio stream, I wanted to package it up into its own class. I did this so I would not have to repeat code and in hopes that others could use it.


**Process**

Aqplayer first creates a Pyaudio object. It then opens a Pyaudio stream with some default values that are typical for most songs. When the player later receives an 'echonest.remix.audio.AudioQuantum', it retrieves an 'echonest.remix.audio.AudioData' for the given 'echonest.remix.audio.AudioQuantum' by means of the 'render' function. This AudioData object contains the data for the section. You simply call '.data' to retrieve the data and write it directly to the audio stream.  


**Dependencies**

To use aqplayer.py, you will need:

      - pyaudio
      - ffmpeg
      - pypitch
      - dirac

**Example**

Simply initialize the aqplayer.
Then you can feed it any type of AudioQuantum to be played.
```python
import echonest.remix.audio as audio
from aqplayer import Player

audio_file = audio.LocalAudioFile("15 Sir Duke.m4a")
bars = audio_file.analysis.bars

aqplayer = Player()  # creates a Player 

for bar in bars:
    aqplayer.play(bar)  # give play() any 'echonest.remix.audio.AudioQuantum' to be played (section, bar, beat, etc...)

aqplayer.closeStream()  # close the audiostream when done
```

**Code Explanation**

In the initializer, aqplayer first creates a pyaudio object. It then creates a stream using the pyaudio object. The parameters used to open the stream are set to default values.
```python
def __init__(self):
        """
        Creates a Player object
        Special thanks to Dr.Parry for adding linux compatibility
        """
        if sys.platform == 'linux2':
            import ossaudiodev

            self.stream = ossaudiodev.open('w')
            self.stream.setparameters(ossaudiodev.AFMT_S16_LE, 2, 44100)
        else:
            import pyaudio

            self.p = pyaudio.PyAudio()
            self.stream = self.p.open(format=self.p.get_format_from_width(2), channels=2, rate=44100, output=True)
```
When it comes time to play an AudioQuantum, it just renders it into an AudioData object and feeds the data directly to the stream.
```python
def play(self, audio_quantum):
        """
        Accepts any echonest.remix.audio.AudioQuantum and audibly plays it for you using pyaudio.
        """
        ad = audio_quantum.render()  # gets AudioData object for AudioQuantum
        self.stream.write(ad.data.tostring())  # writes data to stream
```
Make sure to close the pyaudio stream when you are done by calling the closeStream() method.

**Tempo Shifting**

A recent improvement to aqplayer allows for real time tempo shifting using dirac. Best results are found when shifting beats. If you try to shift anything larger, it creates blips in the music. Also, keep the ratio in the limits that dirac specifies. When you begin to reach the outer limits, blips may also occur. Otherwise shifting is seamless.

```python
def shift_tempo_and_play(self, audio_quantum, ratio):
        """
        Takes an echonest.remix.audio.AudioQuantum and a ratio.
        It first shifts the tempo of the AudioQuantum using dirac
        and then writes the modified data to the stream.
        """
        import dirac
        import numpy as np
        ad = audio_quantum.render()  # gets AudioData object for AudioQuantum
        scaled_beat = dirac.timeScale(ad.data, ratio)  # modifies tempo using dirac
        self.stream.write(scaled_beat.astype(np.int16).tostring())  # writes data to stream
```

**Pitch Shifting**

The most recent improvement to aqplayer allows users to shift pitch in real time. There are two methods to do so. One can shift by semitones or by octaves. Shifting by semitones is generally the more useful option, but as Jesse Sykes said "sometimes you just want to hear chipmunks." Again, best results occur when shifting beats. Anything larger may result in blips. Also, shifting by octaves seems to be a little more intensive, so blips may also occur.

```python
def shift_semitones_and_play(self, audio_quantum, semitones):
        """
        Takes an echonest.remix.audio.AudioQuantum and a number from -6 to 6.
        It first shifts the AudioQuantum's semitones by the specified input using pypitch
        and then writes the modified data to the stream.
        """
        import numpy as np
        from pypitch import PyPitch

        ad = audio_quantum.render()  # gets AudioData object for AudioQuantum
        new_data = PyPitch.shiftPitchSemiTones(ad.data, semitones)  # shifts semitones using pypitch
        self.stream.write(new_data.astype(np.int16).tostring())  # writes data to stream


    def shift_octaves_and_play(self, audio_quantum, octaves):
        """
        Takes an echonest.remix.audio.AudioQuantum and a number of octaves to shift by.
        It first shifts the AudioQuantum's semitones by the specified input using pypitch
        and then writes the modified data to the stream.
        """
        import numpy as np
        from pypitch import PyPitch

        ad = audio_quantum.render()  # gets AudioData object for AudioQuantum
        new_data = PyPitch.shiftPitchOctaves(ad.data, octaves)  # shifts octaves using pypitch
        self.stream.write(new_data.astype(np.int16).tostring())  # writes data to stream
```
