__author__ = 'lukestack'

import echonest.remix.audio as audio
import matplotlib.pyplot as plt
import SegColor
import aqplayer

SONG_DIR = "MP3Songs/"
SONG = "15 Sir Duke.m4a"

audio_file = audio.LocalAudioFile(SONG_DIR + SONG)
bounds = SegColor.normalizeColor(audio_file)

segments = audio_file.analysis.segments
tatums = audio_file.analysis.tatums
beats = audio_file.analysis.beats
bars = audio_file.analysis.bars
sections = audio_file.analysis.sections

fig = plt.figure()
ax = fig.add_subplot(111)

for i in range(0, len(segments)):
    start = segments[i].start
    loudest_point = start + segments[i].time_loudness_max
    end = start + segments[i].duration
    color = SegColor.getSegmentColor(bounds, segments[i])
    if i + 1 < len(segments):
        next_seg_loudness = segments[i + 1].loudness_begin
    else:
        next_seg_loudness = 0
    ax.plot([start, loudest_point], [segments[i].loudness_begin, segments[i].loudness_max], linewidth=2, color=color)
    ax.fill_between([start, loudest_point], [segments[i].loudness_begin, segments[i].loudness_max], -60, color=color)
    ax.plot([loudest_point, end], [segments[i].loudness_max, next_seg_loudness], linewidth=2, color=color)
    ax.fill_between([loudest_point, end], [segments[i].loudness_max, next_seg_loudness], -60, color=color)

# plots for legend
ax.plot([sections[0].start, sections[0].start], [-30, -60], linewidth=4, color='black', label="Section")
ax.plot([bars[0].start, bars[0].start], [-37.5, -60], linewidth=3.5, color='blue', label="Bar")
ax.plot([beats[0].start, beats[0].start], [-45, -60], linewidth=3, color='green', label="Beat")
ax.plot([tatums[0].start, tatums[0].start], [-52.5, -60], linewidth=2.5, color='red', label="Tatum")

# plots every tatum, beat, bar and section
for sect in sections:
    ax.plot([sect.start, sect.start], [-30, -60], linewidth=4, color='black')

for bar in bars:
    ax.plot([bar.start, bar.start], [-37.5, -60], linewidth=3.5, color='blue')

for beat in beats:
    ax.plot([beat.start, beat.start], [-45, -60], linewidth=3, color='green')

for tat in tatums:
    ax.plot([tat.start, tat.start], [-52.5, -60], linewidth=2.5, color='red')


ax.set_xlim([0, 10])
ax.set_ylim(-60, 0)
ax.legend()

fig.suptitle(SONG, fontsize=20)
plt.xlabel('Seconds', fontsize=16)
plt.ylabel('Decibels (dB)', fontsize=16)
plt.savefig("SirDukeAnalysisVisual.png")
plt.show(block=True)


# Still needs work
"""
curr_beat = beats[0]
# cursor, = ax.plot(curr_beat.start, -55, color='green', markersize=10, marker='s')
playing = True


def update_cursor():
    global curr_beat
    last_beat = curr_beat
    while playing:
        if last_beat != curr_beat:
            # cursor.set_xdata(curr_beat.start)
            # fig.canvas.draw(blit=True)
            last_beat = curr_beat


def play_music():
    global curr_beat
    global playing
    player = aqplayer.Player()
    for beat in beats:
        print beat.start
        curr_beat = beat
        player.play(curr_beat)
    playing = False
    player.close_stream()

#thread1 = threading.Thread(target=play_music)
#thread2 = threading.Thread(target=update_cursor)

#thread1.start()
#thread2.start()
"""