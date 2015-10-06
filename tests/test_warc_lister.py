from unittest import TestCase
import sf_warc_lister as lister


class TestReader(TestCase):
    def test_parse_tumblr_url(self):
        service, api_method, api_args = lister.parse_tumblr_url("http://api.tumblr.com/v2/blog/justinlittman-dev.tumblr.com/posts?oauth_body_hash=2jmj7l5rSw0yVb%2FvlWAYkK%2FYBwk%3D&oauth_nonce=98846162&oauth_timestamp=1426651697&oauth_consumer_key=Fki0Q9w9QcW95yy66RtFCni14QpM0pjuHbDWMrZ9aPXcsthVQq&oauth_signature_method=HMAC-SHA1&oauth_version=1.0&limit=20&offset=0&oauth_token=&api_key=Fki0Q9w9QcW95yy66RtFCni14QpM0pjuHbDWMrZ9aPXcsthVQq&oauth_signature=iQ5hsKPkOFUVQQhmkvTLS4rHZ10%3D")
        self.assertEqual("tumblr", service)
        self.assertEqual("blog.posts", api_method)
        self.assertEqual(api_args["base-hostname"], ["justinlittman-dev.tumblr.com"])
        self.assertEqual(api_args["limit"], ["20"])
        self.assertEqual(api_args["offset"], ["0"])

    def test_parse_flickr_url(self):
        service, api_method, api_args = lister.parse_flickr_url("https://api.flickr.com/services/rest/?nojsoncallback=1&user_id=131866249%40N02&method=flickr.people.getInfo&format=json")
        self.assertEqual("flickr", service)
        self.assertEqual("people.getInfo", api_method)
        self.assertEqual(api_args["user_id"], ["131866249@N02"])

    def test_parse_twitter_url(self):
        service, api_method, api_args = lister.parse_twitter_url("https://api.twitter.com/1.1/statuses/user_timeline.json?page=1&screen_name=justin_littman")
        self.assertEqual("twitter", service)
        self.assertEqual("statuses.user_timeline", api_method)
        self.assertEqual(api_args["screen_name"], ["justin_littman"])
        self.assertEqual(api_args["page"], ["1"])
