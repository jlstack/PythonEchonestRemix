__author__ = 'lukestack'
import echonest.remix.audio as audio
import OptimizedBeatDistance as BD
import os
import pickle
import random
from aqplayer import Player
import SegColor as sc
from Tkinter import *


PLAYLIST_DIR = "/Users/lukestack/PycharmProjects/InfiniteJukeboxReplica/InfinitePlaylistBranches/The Beatles/"
INPUT_DIR = "/Users/lukestack/PycharmProjects/InfiniteJukeboxReplica/MP3Songs/The Beatles/"

# Determines if tempo shifting will occur during playing
SHIFT_TEMP = True

# Distance threshold for branches within a song (0 to 80)
THRESHOLD = 70
# Distance threshold for branches out of a song (0 to 80)
THRESHOLD_OUT = 80

# Probability of taking a transition within a song (0 to 100)
PERCENT = 50
# Probability of taking a transition out of a song (0 to 100)
PERCENT_OUT = 80

# Number of beats that must be played before switching songs
LOOK_AHEAD = 4

# Used to change visual placement
xpad = 25
ypad = 400
height = 80


def draw(canvas, audio_file, branches):
    """
    Draws all necessary items (beats and branches) for the specified LocalAudioFile.
    """
    bounds = sc.normalizeColor(audio_file)
    beats = audio_file.analysis.beats
    width = (1440 - (xpad * 2)) / float(len(beats))
    draw_branches(canvas, audio_file, branches, bounds, width)
    draw_beats(canvas, beats, bounds, width)


def draw_beats(canvas, beats, bounds, width):
    """
    Draws all beats for a given song.
    """
    for i in range(len(beats)):
        my_color = sc.getSegmentColor(bounds, beats[i].segments[0])
        canvas.create_polygon(xpad + (i * width), ypad, xpad + (i * width) + width, ypad,
                              xpad + (i * width) + width, ypad + height, xpad + (i * width), ypad + height,
                              fill=my_color)


def draw_branches(canvas, audio_file, branches, bounds, width):
    """
    Draws all branches both within and out of a song.
    """
    beats = audio_file.analysis.beats
    md5 = audio_file.analysis.pyechonest_track.md5
    keys = branches[md5].keys()
    num_branches_in = 0
    num_branches_out = 0
    for key in keys:
        for branch in branches[md5][key]:
            if branch[0] <= THRESHOLD_OUT and branch[1] != md5:
                canvas.create_polygon(xpad + (key * width), ypad + height, xpad + (key * width) + width, ypad + height,
                                      xpad + (key * width) + width, ypad + height + 50, xpad + (key * width),
                                      ypad + height + 50, fill="green")
                num_branches_out += 1
            elif (branch[0] <= THRESHOLD and branch[1] == md5) or (branch[2] == max(keys) and branch[1] == md5):
                num_branches_in += 1
                mycolor = sc.getSegmentColor(bounds, beats[key].segments[0])
                x0 = xpad + key * width + width / 2
                x1 = xpad + branch[2] * width + width / 2
                xmid = (x0 + x1) / 2
                coord = x0, ypad, xmid, ypad - 200, x1, ypad
                canvas.create_line(coord, width=width / 2, smooth=True, fill=mycolor)
    print md5, "in:", num_branches_in, "out:", num_branches_out


def draw_current_beat(canvas, width, i):
    """
    Used to updates cursor for current beat.
    """
    # creates blue bar on current the given canvas at the specified beat's location
    return canvas.create_polygon(xpad + (i * width), ypad - 10, xpad + (i * width) + width, ypad - 10,
                                 xpad + (i * width) + width, ypad + height + 10, xpad + (i * width), ypad + height + 10,
                                 fill="blue", tag='currentBeat')


def draw_current_branch(canvas, width, start, end):
    """
    Used to draw blue highlight when a branch is taken.
    """
    # creates blue arc over current branch on the given canvas
    x0 = xpad + start * width + width / 2
    x1 = xpad + end * width + width / 2
    xmid = (x0 + x1) / 2
    coord = x0, ypad, xmid, ypad - 200, x1, ypad
    return canvas.create_line(coord, width=width / 2, smooth=True, fill="blue")


def create_all_canvases(lafs, branches, window):
    """
    Creates a canvas for each LocalAudioFile displaying all beats and transitions.
    The canvases are then stored in a dictionary using track md5s as the keys.
    """
    keys = lafs.keys()
    canvases = {}
    for key in keys:
        canvas = Canvas(window, height=900, width=1440)
        canvas.create_text(720, 100, font=("Purisa", 50), justify="center", text=lafs[key][1])
        draw(canvas, lafs[key][0], branches)
        canvases[key] = canvas
    return canvases


def create_branch_files(lafs):
    """
    Creates branch pickle file for each comparison between two LocalAudioFiles.
    """
    for i in lafs:
        for j in lafs:
            BD.get_edges(lafs[i][0], lafs[j][0], PLAYLIST_DIR)


def load_all_branches():
    """
    Combines all branch pickle files into one dictionary.
    """
    branches = {}
    for f in os.listdir(PLAYLIST_DIR):
        pkl_name = PLAYLIST_DIR + f
        pkl = open(pkl_name, 'r')
        branch_file = pickle.load(pkl)
        pkl.close()
        keys = branch_file.keys()
        for key in keys:
            if key not in branches.keys() and key != 'num_edges':
                branches[key] = branch_file[key]
            elif key != 'num_edges':
                branches[key].update(branch_file[key])
    return branches


def get_all_laf():
    """
    Retrieves LocalAudioFile from Echonest for each song in the input directory.
    """
    lafs = {}
    for song in os.listdir(INPUT_DIR):
        if song.endswith(".m4a") or song.endswith(".mp3"):
            try:
                laf = audio.LocalAudioFile(INPUT_DIR + song)
                md5 = laf.analysis.pyechonest_track.md5
                if md5 not in lafs.keys():
                    lafs[md5] = (laf, os.path.splitext(song)[0])
            except:
                print "Failed to retrieve analysis from Echonest"
    return lafs


def should_branch(new_song, curr_song, local_context, distance):
    """
    Determines if a branch should be taken.
    """
    rand = random.randint(1, 100)
    if new_song != curr_song and rand <= PERCENT_OUT and distance <= THRESHOLD_OUT and local_context == 0:
        return True
    if new_song == curr_song and rand <= PERCENT and distance <= THRESHOLD:
        return True
    return False


def play(lafs, branches, canvases):
    """
    Determines the path the music takes by choosing songs, branches and beats.
    Most of the code is just updating variables:
        curr_song - current song being played (md5)
        curr_laf - current LocalAudioFile being used
        curr_beat - current beat being played
        curr_canvas - current canvas for the current song
        curr_width - current width of blue cursor
        next_branch - beat index for next transition to take place
        new_song - next song to be played (determined by the next branch to be taken)
        new_beat - where the next transition goes to in the next song
        cursor - blue bar that is updated on the canvas to show the song's current position
        bran - blue arc that is drawn on canvas to indicate a branch being taken
    These variables must be updated every time a transition is taken. Some must be updated with every beat.
    One day I may consolidate multiple dictionaries into one, using tuples to make the code neater.
    """
    player = Player()
    curr_song = random.choice(branches.keys())
    curr_canvas = canvases[curr_song]
    curr_canvas.pack()
    curr_canvas.update()
    curr_laf = lafs[curr_song][0]
    curr_width = (1440 - (xpad * 2)) / float(len(curr_laf.analysis.beats))
    curr_beat = 0
    next_branch = -1
    new_song = -1
    new_beat = -1
    cursor = None
    bran = None
    while True:
        try:
            # deletes last cursor / branch if necessary
            if cursor is not None:
                curr_canvas.delete(cursor)
            if bran is not None:
                curr_canvas.delete(bran)

            # looks for next branch if one hasn't been chosen
            if (curr_beat + LOOK_AHEAD) in branches[curr_song].keys() and next_branch < 0:
                distance, new_song, new_beat = random.choice(branches[curr_song][curr_beat + LOOK_AHEAD])
                if should_branch(new_song, curr_song,
                                 curr_laf.analysis.beats[curr_beat + LOOK_AHEAD].local_context()[0], distance):
                    next_branch = curr_beat + LOOK_AHEAD

            # branches either within or out of the current song
            if curr_beat == next_branch:
                if new_song == curr_song:
                    bran = draw_current_branch(curr_canvas, curr_width, curr_beat, new_beat)
                    curr_beat = new_beat
                else:
                    curr_song = new_song
                    curr_beat = new_beat
                    curr_laf = lafs[curr_song][0]
                    curr_width = (1440 - (xpad * 2)) / float(len(curr_laf.analysis.beats))
                    curr_canvas.forget()
                    curr_canvas = canvases[curr_song]
                    curr_canvas.pack()
                    curr_canvas.update()
                next_branch = -1
            cursor = draw_current_beat(curr_canvas, curr_width, curr_beat)
            curr_canvas.update()

            # plays current beat and shifts tempo first if desired
            if SHIFT_TEMP and next_branch > -1 and new_song != curr_song:
                curr_tempo = curr_laf.analysis.tempo
                new_tempo = lafs[new_song][0].analysis.tempo
                tempo_diff = (curr_tempo['value'] - new_tempo['value'])
                if tempo_diff > 20:
                    tempo_diff = 20  # anything more seems to speed up/slow down too much
                if tempo_diff < -20:
                    tempo_diff = -20  # anything more seems to speed up/slow down too much
                adjusted_diff = (tempo_diff / LOOK_AHEAD) * (LOOK_AHEAD - (next_branch - curr_beat) + 1)
                adjusted_diff *= new_tempo['confidence']  # I did this because transitions were too extreme
                ratio = curr_tempo['value'] / (curr_tempo['value'] - adjusted_diff)
                player.shift_tempo_and_play(curr_laf.analysis.beats[curr_beat], ratio)
            else:
                player.play(curr_laf.analysis.beats[curr_beat])
            curr_beat += 1

        # used for when a song reaches it's end and a new song must be chosen
        except IndexError:
            curr_song = random.choice(lafs.keys())
            curr_beat = 0
            curr_laf = lafs[curr_song][0]
            curr_width = (1440 - (xpad * 2)) / float(len(curr_laf.analysis.beats))
            if cursor is not None:
                curr_canvas.delete(cursor)
            curr_canvas.forget()
            curr_canvas = canvases[curr_song]
            curr_canvas.pack()
            curr_canvas.update()


def main():
    lafs = get_all_laf()
    window = Tk()
    if not os.path.isdir(PLAYLIST_DIR):
        os.makedirs(PLAYLIST_DIR)
        create_branch_files(lafs)
    branches = load_all_branches()
    canvases = create_all_canvases(lafs, branches, window)
    play(lafs, branches, canvases)


if __name__ == "__main__":
    main()