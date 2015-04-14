__author__ = 'lukestack'
import echonest.remix.audio as audio
import BeatDistance as bd
import FindBranches as fb
import random

OUTPUT_DIR = "Snippet/Samples/"

def make_song_snippet(beat1_index, beat2_index, laf1, laf2):
    beats1 = laf1.analysis.beats
    beats2 = laf2.analysis.beats
    bars1 = laf1.analysis.bars
    bars2 = laf2.analysis.bars
    md51 = laf1.analysis.pyechonest_track.md5
    md52 = laf2.analysis.pyechonest_track.md5
    distance = bd.get_beat_distance(beats1[beat1_index], beats2[beat2_index])
    bar1 = beats1[beat1_index].parent().absolute_context()[0]
    bar2 = beats2[beat2_index].parent().absolute_context()[0]
    if bar1 - 2 >= 0:
        starting_beat = bars1[bar1 - 2].children()[0].absolute_context()[0]
    else:
        starting_beat = 0
    if bar2 + 3 < len(bars2):
        last_beat = bars2[bar2 + 3].children()[0].absolute_context()[0]
    else:
        last_beat = len(beats2)
    out = audio.getpieces(beats1.get_source(), beats1[starting_beat:beat1_index])
    out += audio.getpieces(beats2.get_source(), beats2[beat2_index:last_beat])
    out.encode(OUTPUT_DIR + str(md51) + "_beat_" + str(beat1_index) + "_" + str(md52) +
               "_beat_" + str(beat2_index) + "_" + str(distance) + ".wav")


def main():
    audio_file1 = audio.LocalAudioFile("15 Sir Duke.m4a")
    branches = fb.getBranches(audio_file1)
    for i in range(10):
        beat1 = random.choice(branches.keys())
        beat2 = random.choice(branches[beat1])[0]
        make_song_snippet(beat1, beat2, audio_file1, audio_file1)


if __name__ == "__main__":
    main()