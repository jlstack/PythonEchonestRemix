__author__ = 'lukestack'

import pyaudio
import wave

"""
This class' purpose is to play an echonest.remix.audio.AudioQuantum given the quantum and the wave file.
It opens a pyaudio stream and feeds it the wave frames to be played.
"""
class player:

    def __init__(self, wave_file):
        p = pyaudio.PyAudio()
        self.wf = wave.open(wave_file, 'rb')
        self.stream = p.open(format=self.p.get_format_from_width(self.wf.getsampwidth()),
                                channels=self.wf.getnchannels(), rate=self.wf.getframerate(), output=True)

    def play(self, AudioQuantum):
        index = AudioQuantum.absolute_context()[0]
        if index == 0:
            numframes = int((AudioQuantum.duration + AudioQuantum.start) * self.wf.getframerate())
            startframe = 0
        else:
            numframes = int(AudioQuantum.duration * self.wf.getframerate())
            startframe = int(AudioQuantum.start * self.wf.getframerate())
        self.wf.setpos(startframe)
        self.stream.write(self.wf.readframes(numframes))

    def closeStream(self):
        self.stream.close()