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
To find the start of the wav frames to be fed to the stream, aqplayer multiplies the starting time of the 'echonest.remix.audio.AudioQuantum' by the wav framerate. To calculate the number of frames, aqplayer multiplies the duration of the 'echonest.remix.audio.AudioQuantum' by the wav framerate. After these values are found, the position of the wave is set, and the frames read using wave's readframes method. These frames are written to the stream.
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

**Information About Waves**

The things you need to know about waves are:

	-wave files store file data in an array
	-a wave framesrate is the number of frames per second for a file
	-to find the frames associated with a given time, multiply the sime by the framerate
