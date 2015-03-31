__author__ = 'lukestack'

import dirac
from echonest.remix import audio
from aqplayer import Player

file1 = "15 Sir Duke.m4a"

def main():
    audiofile = audio.LocalAudioFile(file1)
    player = Player(audiofile)
    beats = audiofile.analysis.beats
    for beat in beats:
        ratio = 1.25 - ((float(beat.absolute_context()[0]) / float(len(beats))) * .5)
        print ratio
        beat_audio = beat.render()
        scaled_beat = dirac.timeScale(beat_audio.data, ratio)
        ts = audio.AudioData(ndarray=scaled_beat, shape=scaled_beat.shape,
                                     sampleRate=audiofile.sampleRate, numChannels=scaled_beat.shape[1])
        player.play_from_AudioData(ts)
    player.close_stream()
if __name__ == '__main__':
    main()

