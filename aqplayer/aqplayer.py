__author__ = 'lukestack'

import pyaudio
import wave
import tempfile
from echonest.remix.support.ffmpeg import ffmpeg

class Player:
    """
    Plays an echonest.remix.audio.AudioQuantum given an echonest.remix.audio.LocalAudioFile.
    It opens a pyaudio stream and feeds it the wave frames to be played.
    """
    def __init__(self, audio_file):
        self.p = pyaudio.PyAudio()
        self.af = audio_file
        self.wf = wave.open(self.get_wav(), 'rb')
        self.stream = self.p.open(format=self.p.get_format_from_width(self.wf.getsampwidth()),
                                channels=self.af.numChannels, rate=self.af.sampleRate, output=True)

    def get_wav(self): #borrowed some code from the AudioData class to get wavfile
        """
        Helper method for __init__
        :return .wav file from the LocalAudioFile
        """
        if self.af.filename.lower().endswith(".wav") and (self.af.sampleRate, self.af.numChannels) == (44100, 2):
            file_to_read = self.af.filename
        elif self.af.convertedfile:
            file_to_read = self.af.convertedfile
        else:
            temp_file_handle, self.af.convertedfile = tempfile.mkstemp(".wav")
            self.af.sampleRate, self.af.numChannels = ffmpeg(self.af.filename, self.af.convertedfile, overwrite=True,
                    numChannels=self.af.numChannels, sampleRate=self.af.sampleRate, verbose=self.af.verbose)
            file_to_read = self.af.convertedfile
        return file_to_read

    def play(self, AudioQuantum, intro=False):
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

    def closeStream(self):
        """
        closes pyaudio stream
        """
        self.stream.close()
