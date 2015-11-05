from tests import TestCase
import socialfeedtools.utils as utils


class TestUtils(TestCase):
    def test_is_tumblr_url(self):
        self.assertTrue(utils.is_tumblr_url("http://api.tumblr.com/v2/blog/justinlittman-dev.tumblr.com/posts?oauth_body_hash=2jmj7l5rSw0yVb%2FvlWAYkK%2FYBwk%3D&oauth_nonce=98846162&oauth_timestamp=1426651697&oauth_consumer_key=Fki0Q9w9QcW95yy66RtFCni14QpM0pjuHbDWMrZ9aPXcsthVQq&oauth_signature_method=HMAC-SHA1&oauth_version=1.0&limit=20&offset=0&oauth_token=&api_key=Fki0Q9w9QcW95yy66RtFCni14QpM0pjuHbDWMrZ9aPXcsthVQq&oauth_signature=iQ5hsKPkOFUVQQhmkvTLS4rHZ10%3D"))
        self.assertFalse(utils.is_tumblr_url("https://farm9.staticflickr.com/8710/16609036938_6ed7e2331e_b.jpg"))

    def test_is_flickr_url(self):
        self.assertTrue(utils.is_flickr_url("https://api.flickr.com/services/rest/?nojsoncallback=1&user_id=131866249%40N02&method=flickr.people.getInfo&format=json"))
        self.assertFalse(utils.is_flickr_url("https://farm9.staticflickr.com/8710/16609036938_6ed7e2331e_b.jpg"))

    def test_is_twitter_rest_url(self):
        self.assertTrue(utils.is_twitter_rest_url("https://api.twitter.com/1.1/statuses/user_timeline.json?page=1&screen_name=justin_littman"))
        self.assertFalse(utils.is_twitter_rest_url("https://farm9.staticflickr.com/8710/16609036938_6ed7e2331e_b.jpg"))
        self.assertFalse(utils.is_twitter_stream_url("https://stream.twitter.com/1.1/statuses/sample.json"))

    def test_is_twitter_stream_url(self):
        self.assertTrue(utils.is_twitter_stream_url("https://stream.twitter.com/1.1/statuses/sample.json"))
        self.assertFalse(utils.is_twitter_rest_url("https://api.twitter.com/1.1/statuses/user_timeline.json?page=1&screen_name=justin_littman"))
        self.assertFalse(utils.is_twitter_rest_url("https://farm9.staticflickr.com/8710/16609036938_6ed7e2331e_b.jpg"))
