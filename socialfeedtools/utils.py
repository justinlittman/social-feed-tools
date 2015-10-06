import json
import logging

log = logging.getLogger(__name__)

def is_tumblr_url(url):
    return url.startswith("http://api.tumblr.com/v2")


def is_flickr_url(url):
    return url.startswith("https://api.flickr.com/services/rest/")


def is_twitter_url(url):
    return url.startswith("https://api.twitter.com/1.1")


def extract_json_from_payload(record):
    """
    Extract json from a warc response record.

    Assumes that json is a single line that appears after the http headers.
    :param record:  the warc response record.
    :return: a json object or None
    """
    next_line = False
    first_line = True
    for l in record.payload:
        if first_line:
            if not l.startswith("HTTP/1.1 200 OK"):
                return None
            first_line = False
        if next_line:
            try:
                return json.loads(l)
            except:
                log.warning("Error parsing json in record %s (%s)", record.header.record_id, record.url)
                return None
        if l == "\r\n":
            next_line = True

    return None