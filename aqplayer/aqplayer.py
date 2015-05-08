__author__ = 'lukestack'
import sys


class Player:
    """
    Plays an echonest.remix.audio.AudioQuantum given an echonest.remix.audio.LocalAudioFile.
    It opens a pyaudio stream and feeds it the wave frames to be played.
    """
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


    def play(self, audio_quantum):
        """
        Accepts any echonest.remix.audio.AudioQuantum and audibly plays it for you using pyaudio.
        """
        ad = audio_quantum.render()  # gets AudioData object for AudioQuantum
        self.stream.write(ad.data.tostring())  # writes data to stream


    def close_stream(self):
        """
        closes pyaudio stream and pyaudio object if necessary
        """
        self.stream.close()
        if self.p is not None:
            self.p.terminate()
