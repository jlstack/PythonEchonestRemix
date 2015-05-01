__author__ = 'lukestack'

from echonest.remix import audio
from aqplayer import Player


def main():
    file1 = "Mp3Songs/15 Sir Duke.m4a"
    audiofile = audio.LocalAudioFile(file1)
    player = Player()
    beats = audiofile.analysis.beats
    for beat in beats:
        ratio = 1.25 - ((float(beat.absolute_context()[0]) / float(len(beats))) * .5)
        player.shift_tempo_and_play(beat, ratio)
    player.close_stream()


if __name__ == '__main__':
    main()
