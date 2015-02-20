__author__ = 'lukestack'

import BeatDistance
import pickle
import os
import echonest.remix.audio as audio

def findBranches(audio_file):
    print "Finding branches. Be patient, this could take a while..."
    filename= os.path.splitext(os.path.split(audio_file.filename)[1])[0]
    print "finding branches for",filename
    beats = audio_file.analysis.beats
    branches = {}
    for i in range(len(beats)):
        beat1 = beats[i]
        for j in range(i+1,len(beats)):
            beat2 = beats[j]
            if beat1.local_context()[0] == beat2.local_context()[0]:
                dist = BeatDistance.get_beat_distance(beat1, beat2)
                if dist <= 80:
                    if branches.has_key(i):
                        branches[i].append((j, dist))
                    else:
                        branches[i] = [(j, dist)]
                    if branches.has_key(j):
                        branches[j].append((i, dist))
                    else:
                        branches[j] = [(i, dist)]
    if not os.path.exists(os.path.dirname(os.path.realpath(__file__)) + "/Branches"):
        os.makedirs(os.path.dirname(os.path.realpath(__file__)) + "/Branches")
    with open(os.path.dirname(os.path.realpath(__file__)) + "/Branches/" + filename + ".pkl", 'w') as outfile:
        pickle.dump([branches, branches], outfile)
