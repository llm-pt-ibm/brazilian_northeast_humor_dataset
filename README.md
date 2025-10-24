# Brazilian Northeast Humor Dataset

Code used to collect transcriptions of texts by Northeastern comedians from YouTube Shorts.

# Data

1. The file ```youtube_videos.csv``` in the ```/data/videos``` folder contains the URLs manually extracted from YouTube Shorts videos of Northeastern Brazilian comedians.
2. The data in the ```/data/transcriptions``` folder come from the automatic collection performed by the code in this repository.
3. The data in the ```/data/annotated``` folder come from the <b>manual</b> annotations and revisions described in this [Zenodo repository](https://zenodo.org/records/15473224).
4. The data in the ```/data/completed``` folder come from the automatic polishing process performed by the code in this repository.

# Requirements

- Python [3.12](https://www.python.org/downloads/release/python-3120/) and [pip](https://pip.pypa.io/en/stable/installation/)
- ``pip install -r requirements.txt``
- ``sudo apt-get update && apt-get install -y ffmpeg``

# Execution
- ``python main.py``




