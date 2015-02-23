##FindBranches

FindBranches is static and is used to find and store all branches in a given song. After the brancehs are found they are stored in the Branch directory as a pickle file. If the Branch directory does not exist, it is created. The file is named using the md5 for from the LocalAudioFile.

**Example**

```python
import echonest.remix.audio as audio
import FindBranches as fb

audio_file = audio.LocalAudioFile(filename)
fb.findBranches(audio_file)
```

After running this code, a pickle file should be created and stored in the Branches which will be located in your local directory.

FindBranches has only one method. This method checks to see if the distance between two beats is less than or equal to 80. If it is, the the branch is added to the branches dictionary.

```python
def findBranches(audio_file):
    print "Finding branches. Be patient, this could take a while..."
    if ".remix-db/audio" in audio_file.filename:
        filename = os.path.splitext(os.path.split(audio_file.filename)[1])[0]
    else:
        filename = hashlib.md5(file(audio_file.filename, 'rb').read()).hexdigest()
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
```

In the dictionary the key is equal to the first beat being compared. The value for each key is a list of tuples holding the branchable beat and the distance between the key and that beat. Below is an example of how you might use these branches.

```python
filename = "15 Sir Duke.m4a"
audio_file = audio.LocalAudioFile(filename)
pklname = os.path.dirname(os.path.realpath(__file__)) + "/Branches/" + \
          hashlib.md5(file(filename, 'rb').read()).hexdigest() + ".pkl"
if not os.path.isfile(pklname):
    fb.findBranches(audio_file)
pkl = open(pklname, 'r')
branches = pickle.load(pkl)[0]
if branches.has_key(4):
    print branches[4] #will print a list of tuples containing all branchable beats with the appropriate distance

```
