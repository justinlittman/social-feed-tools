def is_tumblr_url(url):
    return url.startswith("http://api.tumblr.com/v2")


def is_flickr_url(url):
    return url.startswith("https://api.flickr.com/services/rest/")


def is_twitter_rest_url(url):
    return url.startswith("https://api.twitter.com/1.1")


def is_twitter_stream_url(url):
    return url.startswith("https://stream.twitter.com/1.1")


def iter_lines(http_response):
    """
    Iterates over the response data, one line at a time.

    Borrowed from https://github.com/kennethreitz/requests/blob/master/requests/models.py.
    """

    pending = None

    for chunk in http_response.stream(decode_content=True):

        if pending is not None:
            chunk = pending + chunk

        lines = chunk.splitlines()

        if lines and lines[-1] and chunk and lines[-1][-1] == chunk[-1]:
            pending = lines.pop()
        else:
            pending = None

        for line in lines:
            yield line

    if pending is not None:
        yield pending