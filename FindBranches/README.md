##FindBranches

FindBranches is static and is used to find and store all branches in a given song. After the brancehs are found they are stored in the Branch directory as a pickle file. If the Branch directory does not exist, it is created. The file is named using the md5 for from the LocalAudioFile.

**Problem**

When creating the InfiniteJukebox replica, I could already find branches, but I would have to sit and wait for it to do all of the comparisons every time. This got old after a while, so I decided to store them. In Python, pickle is used to store objects. This seemed to fit my needs. I named the files using their md5 since that is what Echo Nest uses.
 
**Example**

```python
import echonest.remix.audio as audio
import FindBranches as fb

filename = "15 Sir Duke.m4a"
audio_file = audio.LocalAudioFile(filename)
branches = fb.getBranches(audio_file) #a dictionary is returned containing the branches for the given audio_file
if branches.has_key(4):
    print branches[4] #list of tuples containing all branchable beats with their appropriate distance

```

After running this code, a pickle file should be created and stored in the Branches(which will be located in your local directory) if it did not already exist. You will see that the code will run incredibly fast after the branches have already been stored. 

FindBranches has only two methods. The method that does most of the work is findBranches. FindBranches loops through all of the beats comparing them to every other beat in the song. If the distance between two beats is less than or equal to 80, the the branch is added to the branches dictionary. Keep in mind, findBranches is a void method. It just creates and stores the branches. However, GetBranches loads the pickle file if it is available and returns the dictionary of branches. If the pickle file does not exist, it first calls findBranches to create them.

Below is the code for findBranches. As you can see, it makes use of nested for loops to do all of the (n * (n-1))/2 comparisons. To calculate distance, it uses my BeatDistance class.

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
        pickle.dump(branches, outfile)
```

In the dictionary the key is equal to the first beat being compared. The value for each key is a list of tuples holding the branchable beat and the distance between the key and that beat. 

