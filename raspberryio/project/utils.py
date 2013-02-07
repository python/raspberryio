import urlparse

YOUTUBE_SHORT_URL = "youtu.be"

YOUTUBE_DOMAINS = ("www.youtube.com",
                   "youtube.com",
                   "m.youtube.com",
                   YOUTUBE_SHORT_URL
                   )


def get_youtube_video_id(url):
    "Consumes a URL and extracts the video id"
    video_id = ''
    data = urlparse.urlparse(url)
    if data.netloc.lower() in YOUTUBE_DOMAINS:
        if data.netloc.lower() != YOUTUBE_SHORT_URL:
            query = urlparse.parse_qs(data.query)
            video_id = query.get('v', '')[0]
        else:
            video_id = data.path.split('/')[1]
    return video_id
