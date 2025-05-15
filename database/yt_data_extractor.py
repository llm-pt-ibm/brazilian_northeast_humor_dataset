import os

from pydub import AudioSegment
from pytubefix import YouTube
from pytubefix.cli import on_progress

class YouTubeDataExtractor:

    def __init__(self):
        pass

    def extract_length_from_youtube_video(self, youtube_url):
        yt = YouTube(youtube_url, on_progress_callback = on_progress)
        return yt.length

    def extract_title_from_youtube_video(self, youtube_url):
        yt = YouTube(youtube_url, on_progress_callback = on_progress)
        return yt.title

    def extract_publish_date_from_youtube_video(self, youtube_url):
        yt = YouTube(youtube_url, on_progress_callback = on_progress)
        details = yt.vid_details

        keys_path = ["engagementPanels", "2", "engagementPanelSectionListRenderer", "content",
           "structuredDescriptionContentRenderer", "items", "0",
           "videoDescriptionHeaderRenderer", "publishDate", "simpleText"]
        
        try:
            for key in keys_path:
                if isinstance(details, list):
                    key = int(key)
                details = details[key]
            return details
        except (KeyError, IndexError, TypeError, ValueError):
            return None

    def extract_audio_from_youtube_video(self, youtube_url: str, output_path: str):
        yt_title = self.extract_title_from_youtube_video(youtube_url)
        yt = YouTube(youtube_url, on_progress_callback = on_progress, use_oauth=True, client = 'MWEB', allow_oauth_cache=True)
        ys = yt.streams.get_audio_only()

        filename = f'{yt_title}'
        audio_path = ys.download(output_path = output_path, filename = filename)

        mp3_path = os.path.splitext(audio_path)[0] + ".mp3"
        audio = AudioSegment.from_file(audio_path)
        audio.export(mp3_path, format="mp3")
        
        os.remove(audio_path)

        audio_path = os.path.join(output_path, f'{filename}.mp3')

        return audio_path