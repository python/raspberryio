import unittest

from raspberryio.project.utils import YOUTUBE_DOMAINS, get_youtube_video_id


class GetYoutubeVideoIdTestCase(unittest.TestCase):
    "Test the utility that extracts a video id from a YouTube URL"

    def test_valid_domains(self):
        vid = 'dummy'
        for domain in YOUTUBE_DOMAINS[:3]:
            url = 'http://%s/watch?v=%s' % (domain, vid)
            video_id = get_youtube_video_id(url)
            self.assertEqual(vid, video_id)
        short_url = 'http://%s/%s' % (YOUTUBE_DOMAINS[3], vid)
        video_id = get_youtube_video_id(short_url)
        self.assertEqual(vid, video_id)

    def test_invalidvalid_domains(self):
        vid = 'dummy'
        url = 'http://notyoutube.com/watch?v=%s' % vid
        video_id = get_youtube_video_id(url)
        self.assertEqual('', video_id)
