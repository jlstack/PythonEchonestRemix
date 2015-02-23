__author__ = 'lukestack'
import echonest.remix.audio as audio
import os
from aqplayer import Player
import FindBranches as fb
import SegColor as sc
import random
import hashlib
import pickle
from Tkinter import *

usage = """
        Usage:
            python InfiniteJukebox.py <input_filename> <threshold>

        Example:
            python one.py EverythingIsOnTheOne.mp3 65
        """
xpad = 25
ypad = 400
height = 80

def draw(C, audio_file, branches, threshold):
    bounds = sc.normalizeColor(audio_file)
    beats = audio_file.analysis.beats
    width = (1440 - (xpad * 2)) / float(len(beats))
    drawBranches(C, beats, branches, threshold, bounds, width)
    drawBeats(C, beats, bounds, width)

def drawBeats(C, beats, bounds, width):
    for i in range(len(beats)):
        mycolor = sc.getSegmentColor(bounds, beats[i].segments[0])
        C.create_polygon(xpad + (i * width), ypad,                   xpad + (i * width) + width, ypad,
                         xpad + (i * width) + width, ypad + height,  xpad + (i * width), ypad + height, fill=mycolor)

def drawBranches(C, beats, branches, threshold, bounds, width):
    keys = branches.keys()
    lastBranch = max(keys)
    for key in keys:
        for branch in branches[key]:
            if branch[1] <= threshold or key == lastBranch:
                mycolor = sc.getSegmentColor(bounds, beats[key].segments[0])
                x0 = xpad + key * width + width / 2
                x1 = xpad + branch[0] * width + width / 2
                xmid = (x0 + x1) / 2
                coord = x0, ypad, xmid, ypad - 200, x1, ypad
                C.create_line(coord, width=width / 2, smooth=True, fill=mycolor)

def drawCurrentBeat(canvas, width, i):
    return canvas.create_polygon(xpad + (i * width), ypad - 10,                  xpad + (i * width) + width, ypad - 10,
                                 xpad + (i * width) + width, ypad + height + 10, xpad + (i * width), ypad + height + 10,
                                 fill="blue", tag='currentBeat')

def drawCurrentBranch(canvas, width, start, end):
    x0 = xpad + start * width + width / 2
    x1 = xpad + end * width + width / 2
    xmid = (x0 + x1) / 2
    coord = x0, ypad, xmid, ypad - 200, x1, ypad
    return canvas.create_line(coord, width = width / 2, smooth = True, fill="blue")

def play(canvas, audio_file, branches, threshold):
    player = Player(audio_file)
    beats = audio_file.analysis.beats
    lastBranch = max(branches.keys())
    width = (1440 - (xpad * 2)) / float(len(beats))
    cur = drawCurrentBeat(canvas, width, 0)
    canvas.update()
    player.play(beats[0], True) #play the first beat with extra frames for intro
    bran = None
    i = 1
    while i < len(beats):
        randomInt = random.randint(0,1)
        if bran != None:
            canvas.delete(bran)
        if cur != None:
            canvas.delete(cur)
        if i == lastBranch or (branches.has_key(i) and randomInt == 1):
            branchTo = random.choice(branches[i])
            if i == lastBranch or (branchTo[0] < lastBranch and branchTo[1] <= threshold):
                bran = drawCurrentBranch(canvas, width, i, branchTo[0])
                i = branchTo[0]
        cur = drawCurrentBeat(canvas, width, i)
        canvas.update()
        player.play(beats[i])
        i+=1

def main(filename, threshold):
    audio_file = audio.LocalAudioFile(filename)
    pklname = os.path.dirname(os.path.realpath(__file__)) + "/Branches/" + \
              hashlib.md5(file(filename, 'rb').read()).hexdigest() + ".pkl"
    if not os.path.isfile(pklname):
        fb.findBranches(audio_file)
    pkl = open(pklname, 'r')
    branches = pickle.load(pkl)[0]
    window = Tk()
    canvas = Canvas(window, height=900, width=1440)
    song = os.path.split(filename)[1]
    canvas.create_text(720, 100, font=("Purisa", 50), justify="center", text=song)
    draw(canvas, audio_file, branches, threshold)
    canvas.pack()
    canvas.update()
    play(canvas, audio_file, branches, threshold)

if __name__ == '__main__':
    import sys
    try:
        input_filename = sys.argv[1]
        threshold = sys.argv[2]
        main(input_filename, threshold)
    except:
        print usage
        sys.exit(-1)
