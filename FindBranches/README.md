##FindBranches

FindBranches is static and is used to find and store all branches in a given song. After the brancehs are found they are stored in the Branch directory as a pickle file. If the Branch directory does not exist, it is created. The file is named using the md5 for from the LocalAudioFile.

**Example**

```python
import echonest.remix.audio as audio
import FindBranches as fb

audio_file = audio.LocalAudioFile(filename)
fb.findBranches(audio_file)
```

After running this code, a pickle file should be created and stored in the Branch directory located in your local directory.


