__author__ = 'lukestack'

import echonest.remix.audio as audio
import matplotlib.pyplot as plt
import SegColor
import aqplayer
import threading


audio_file = audio.LocalAudioFile("MP3Songs/15 Sir Duke.m4a")
audio_data = audio_file.render().data
audio_data = (audio_data[:, 0] + audio_data[:, 1]) / 2
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

for sect in sections:
    ax.plot([sect.start, sect.start], [-30, -60], linewidth=4, color='black')

for bar in bars:
    ax.plot([bar.start, bar.start], [-37.5, -60], linewidth=3.5, color='blue')

for beat in beats:
    ax.plot([beat.start, beat.start], [-45, -60], linewidth=3, color='green')

for tat in tatums:
    ax.plot([tat.start, tat.start], [-52.5, -60], linewidth=2.5, color='red')

ax.plot([sections[0].start, sections[0].start], [-30, -60], linewidth=4, color='black', label="Section")
ax.plot([bars[0].start, bars[0].start], [-37.5, -60], linewidth=3.5, color='blue', label="Bar")
ax.plot([beats[0].start, beats[0].start], [-45, -60], linewidth=3, color='green', label="Beat")
ax.plot([tatums[0].start, tatums[0].start], [-52.5, -60], linewidth=2.5, color='red', label="Tatum")

ax.set_xlim([0, 10])
ax.set_ylim(-60, 0)
ax.legend()
plt.show(block=True)


# need help making it run


def update_cursor(cursor, x):
    cursor.set_xdata(x)
    fig.canvas.draw()


def play_music():
    player = aqplayer.Player()
    beat = beats[0]
    cursor, = ax.plot(0, -55, color='green', markersize=10, marker='s')
    dt = 0.001
    timer = fig.canvas.new_timer(interval=dt*1000.0)
    timer.add_callback(update_cursor, cursor, beat.start)
    timer.start()
    for b in beats:
        beat = b
        player.play(beat)
    player.close_stream()


# play_music()
# thread1 = threading.Thread(target=play_music)
# thread2 = threading.Thread(target=run_cursor)
# thread2.start()
# thread1.start()
