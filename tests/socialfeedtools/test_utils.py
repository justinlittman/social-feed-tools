from tests import TestCase
import socialfeedtools.utils as utils
from warc.warc import WARCRecord
from warc.utils import FilePart
import StringIO


class TestUtils(TestCase):
    def test_is_tumblr_url(self):
        self.assertTrue(utils.is_tumblr_url("http://api.tumblr.com/v2/blog/justinlittman-dev.tumblr.com/posts?oauth_body_hash=2jmj7l5rSw0yVb%2FvlWAYkK%2FYBwk%3D&oauth_nonce=98846162&oauth_timestamp=1426651697&oauth_consumer_key=Fki0Q9w9QcW95yy66RtFCni14QpM0pjuHbDWMrZ9aPXcsthVQq&oauth_signature_method=HMAC-SHA1&oauth_version=1.0&limit=20&offset=0&oauth_token=&api_key=Fki0Q9w9QcW95yy66RtFCni14QpM0pjuHbDWMrZ9aPXcsthVQq&oauth_signature=iQ5hsKPkOFUVQQhmkvTLS4rHZ10%3D"))
        self.assertFalse(utils.is_tumblr_url("https://farm9.staticflickr.com/8710/16609036938_6ed7e2331e_b.jpg"))

    def test_is_flickr_url(self):
        self.assertTrue(utils.is_flickr_url("https://api.flickr.com/services/rest/?nojsoncallback=1&user_id=131866249%40N02&method=flickr.people.getInfo&format=json"))
        self.assertFalse(utils.is_flickr_url("https://farm9.staticflickr.com/8710/16609036938_6ed7e2331e_b.jpg"))

    def test_is_twitter_url(self):
        self.assertTrue(utils.is_twitter_url("https://api.twitter.com/1.1/statuses/user_timeline.json?page=1&screen_name=justin_littman"))
        self.assertFalse(utils.is_twitter_url("https://farm9.staticflickr.com/8710/16609036938_6ed7e2331e_b.jpg"))

    def test_extract_json_from_payload(self):
        message_body = """HTTP/1.1 200 OK
cache-control: no-cache, no-store, must-revalidate, pre-check=0, post-check=0
content-disposition: attachment; filename=json.json
content-length: 49212
content-type: application/json;charset=utf-8
date: Thu, 30 Apr 2015 17:46:34 GMT
expires: Tue, 31 Mar 1981 05:00:00 GMT
last-modified: Thu, 30 Apr 2015 17:46:34 GMT
pragma: no-cache
\r\n[{"foo1": "bar1"}, {"foo2": "bar2"}]"""
        record = WARCRecord(defaults=False, payload=FilePart(StringIO.StringIO(message_body), len(message_body)))
        json_obj = utils.extract_json_from_payload(record)
        self.assertIsNotNone(json_obj)
        self.assertTrue(2, len(json_obj))
        self.assertEqual("bar1", json_obj[0]["foo1"])

    def test_extract_json_from_payload_not_200(self):
        message_body = """HTTP/1.1 404 Not Found
cache-control: no-cache, no-store, must-revalidate, pre-check=0, post-check=0
content-disposition: attachment; filename=json.json
content-length: 49212
content-type: application/json;charset=utf-8
date: Thu, 30 Apr 2015 17:46:34 GMT
expires: Tue, 31 Mar 1981 05:00:00 GMT
last-modified: Thu, 30 Apr 2015 17:46:34 GMT
pragma: no-cache
\r\n[{"foo1": "bar1"}, {"foo2": "bar2"}]"""
        record = WARCRecord(defaults=False, payload=FilePart(StringIO.StringIO(message_body), len(message_body)))
        json_obj = utils.extract_json_from_payload(record)
        self.assertIsNone(json_obj)

    def test_extract_json_from_payload_no_body(self):
        message_body = """HTTP/1.1 200 OK
cache-control: no-cache, no-store, must-revalidate, pre-check=0, post-check=0
content-disposition: attachment; filename=json.json
content-length: 49212
content-type: application/json;charset=utf-8
date: Thu, 30 Apr 2015 17:46:34 GMT
expires: Tue, 31 Mar 1981 05:00:00 GMT
last-modified: Thu, 30 Apr 2015 17:46:34 GMT
pragma: no-cache
\r\n"""
        record = WARCRecord(defaults=False, payload=FilePart(StringIO.StringIO(message_body), len(message_body)))
        json_obj = utils.extract_json_from_payload(record)
        self.assertIsNone(json_obj)

    def test_extract_json_from_payload_invalid_json(self):
        message_body = """HTTP/1.1 200 OK
cache-control: no-cache, no-store, must-revalidate, pre-check=0, post-check=0
content-disposition: attachment; filename=json.json
content-length: 49212
content-type: application/json;charset=utf-8
date: Thu, 30 Apr 2015 17:46:34 GMT
expires: Tue, 31 Mar 1981 05:00:00 GMT
last-modified: Thu, 30 Apr 2015 17:46:34 GMT
pragma: no-cache
\r\n[{"foo1": "bar1"}, {"foo2": "bar2"}"""
        record = WARCRecord(defaults=False, payload=FilePart(StringIO.StringIO(message_body), len(message_body)))
        json_obj = utils.extract_json_from_payload(record)
        self.assertIsNone(json_obj)
