__author__ = 'lukestack'
import sys


class Player:
    """
    Plays an echonest.remix.audio.AudioQuantum given an echonest.remix.audio.LocalAudioFile.
    It opens a pyaudio stream and feeds it the wave frames to be played.
    """

    def __init__(self):
        if sys.platform == 'linux2':
            # make sure you've started this with $ padsp python infinite_playlist [...]
            import ossaudiodev

            self.stream = ossaudiodev.open('w')
            self.stream.setparameters(ossaudiodev.AFMT_S16_LE, 2, 44100)
        else:
            import pyaudio

            self.p = pyaudio.PyAudio()
            self.stream = self.p.open(format=self.p.get_format_from_width(2), channels=2, rate=44100, output=True)


    def shift_tempo_and_play(self, audio_quantum, ratio):
        """
        Takes an echonest.remix.audio.AudioQuantum and a ratio.
        It first shifts the tempo of the AudioQuantum using dirac
        and then writes the modified data to the stream.
        """
        import dirac
        import numpy as np

        ad = audio_quantum.render()
        scaled_beat = dirac.timeScale(ad.data, ratio)
        self.stream.write(scaled_beat.astype(np.int16).tostring())


    def shift_semitones_and_play(self, audio_quantum, semitones):
        import numpy as np
        from pypitch import PyPitch

        ad = audio_quantum.render()
        new_data = PyPitch.shiftPitchSemiTones(ad.data, semitones)
        self.stream.write(new_data.astype(np.int16).tostring())


    def shift_octaves_and_play(self, audio_quantum, octaves):
        import numpy as np
        from pypitch import PyPitch

        ad = audio_quantum.render()
        new_data = PyPitch.shiftPitchOctaves(ad.data, octaves)
        self.stream.write(new_data.astype(np.int16).tostring())


    def play(self, audio_quantum):
        """
        Accepts any echonest.remix.audio.AudioQuantum and audibly plays it for you using pyaudio.
        """
        ad = audio_quantum.render()
        self.stream.write(ad.data.tostring())


    def close_stream(self):
        """
        closes pyaudio stream
        """
        self.stream.close()
        if self.p is not None:
            self.p.terminate()
