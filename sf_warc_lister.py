import warc
import urlparse
import argparse
import socialfeedtools.utils as utils


class ResponseRecord():
    def __init__(self, record_id, record_url, date):
        self.record_id = record_id
        self.record_url = record_url
        self.date = date


class ApiResponseRecord(ResponseRecord):
    def __init__(self, record_id, record_url, date, service, api_method, api_args):
        ResponseRecord.__init__(self, record_id, record_url, date)
        self.service = service
        self.api_method = api_method
        self.api_args = api_args


def parse_tumblr_url(url):
    #Parse the url
    #http://api.tumblr.com/v2/blog/justinlittman-dev.tumblr.com/posts?oauth_body_hash=2jmj7l5rSw0yVb%2FvlWAYkK%2FYBwk%3D&oauth_nonce=98846162&oauth_timestamp=1426651697&oauth_consumer_key=Fki0Q9w9QcW95yy66RtFCni14QpM0pjuHbDWMrZ9aPXcsthVQq&oauth_signature_method=HMAC-SHA1&oauth_version=1.0&limit=20&offset=0&oauth_token=&api_key=Fki0Q9w9QcW95yy66RtFCni14QpM0pjuHbDWMrZ9aPXcsthVQq&oauth_signature=iQ5hsKPkOFUVQQhmkvTLS4rHZ10%3D
    (scheme, netloc, path, query, fragment) = urlparse.urlsplit(url)
    path_parts = path.split("/")
    assert len(path_parts) == 5
    assert path_parts[1] == "v2"
    api_method = "%s.%s" % (path_parts[2], path_parts[4])
    api_args = urlparse.parse_qs(query)
    #Addd blog to args
    api_args["base-hostname"] = [path_parts[3]]
    #Remove oauth keys
    del_keys = []
    for key in api_args:
        if key.startswith("oauth_"):
            del_keys.append(key)
    for key in del_keys:
        del api_args[key]
    #Remove api_key
    if "api_key" in api_args:
        del api_args["api_key"]
    return "tumblr", api_method, api_args


def parse_flickr_url(url):
    #https://api.flickr.com/services/rest/?nojsoncallback=1&user_id=131866249%40N02&method=flickr.people.getInfo&format=json
    (scheme, netloc, path, query, fragment) = urlparse.urlsplit(url)
    api_args = urlparse.parse_qs(query)
    assert "method" in api_args
    assert len(api_args["method"]) == 1
    api_method = api_args["method"][0]
    if api_method.startswith("flickr."):
        api_method=api_method[7:]
    #Remove method from api_args
    del api_args["method"]
    if "nojsoncallback" in api_args:
        del api_args["nojsoncallback"]
    if "format" in api_args:
        del api_args["format"]
    if "secret" in api_args:
        del api_args["secret"]

    return "flickr", api_method, api_args


def parse_twitter_url(url):
    #https://api.twitter.com/1.1/statuses/user_timeline.json?page=1&screen_name=justin_littman
    (scheme, netloc, path, query, fragment) = urlparse.urlsplit(url)
    path_parts = path.split("/")
    assert len(path_parts) == 4
    assert path_parts[1] == "1.1"
    api_method = "%s.%s" % (path_parts[2], path_parts[3][0:-5])
    api_args = urlparse.parse_qs(query)
    return "twitter", api_method, api_args

api_func_dict = {
    utils.is_tumblr_url: parse_tumblr_url,
    utils.is_flickr_url: parse_flickr_url,
    utils.is_twitter_url: parse_twitter_url
}


def to_response_record(record):
    url = record.header["WARC-Target-URI"]
    for is_func in api_func_dict:
        if is_func(url):
            service, api_method, api_args = api_func_dict[is_func](url)
            return ApiResponseRecord(record.header.record_id, url, record.header.date, service, api_method, api_args)
    return ResponseRecord(record.header.record_id, url, record.header.date)


def list_records(filepath, services=()):
    print "File %s" % filepath
    f = warc.open(filepath)
    try:
        for record in f:
            if record.type == 'response':
                resp_record = to_response_record(record)
                if (not services
                    or (isinstance(resp_record, ApiResponseRecord) and resp_record.service in services)
                        or (not isinstance(resp_record, ApiResponseRecord) and "other" in services)):
                    print "Record %s" % resp_record.record_id
                    print "Url: %s" % resp_record.record_url
                    print "Date: %s" % resp_record.date
                    if isinstance(resp_record, ApiResponseRecord):
                        print "Service: %s" % resp_record.service
                        print "API method: %s (%s)" % (resp_record.api_method, resp_record.api_args)
    finally:
        f.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--services",
                        help="A comma separated list of services to limit the results to. "
                             "Services are: twitter, tumblr, flickr, other.")
    parser.add_argument("filepath", nargs="+", help="Filepath of the warc.")

    args = parser.parse_args()
    svcs = args.services.split(",") if args.services else ()

    for fp in args.filepath:
        list_records(fp, services=svcs)
