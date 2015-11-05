import socialfeedtools.warc as warc
import json
import argparse
import socialfeedtools.utils as utils
import logging
from urllib3.exceptions import ProtocolError

log = logging.getLogger(__name__)


def tumblr_response_iter(record):
    json_obj = json.load(record.http_response)
    yield "tumblr_blog", json_obj["response"]["blog"]
    for post in json_obj["response"]["posts"]:
        yield "tumblr_post", post


def flickr_response_iter(record):
    json_obj = json.load(record.http_response)
    if "photo" in json_obj:
        yield "flickr_photo", json_obj["photo"]
    elif "person" in json_obj:
        yield "flickr_person", json_obj["person"]


def twitter_rest_response_iter(record):
    json_obj = json.load(record.http_response)
    for tweet in json_obj["statuses"]:
        yield "tweet", tweet


def twitter_stream_response_iter(record):
    try:
        for tweet in utils.iter_lines(record.http_response):
            try:
                yield "tweet", json.loads(tweet)
            except ValueError:
                #Bad tweet
                pass
    except ProtocolError:
        #Last chunk incomplete
        pass

to_service_dict = {
    utils.is_tumblr_url: "tumblr",
    utils.is_flickr_url: "flickr",
    utils.is_twitter_rest_url: "twitter_rest",
    utils.is_twitter_stream_url: "twitter_stream"
}


def get_service(record):
    url = record.header["WARC-Target-URI"]
    for is_func, service in to_service_dict.iteritems():
        if is_func(url):
            return service
    return None


service_to_iter_func_dict = {
    "tumblr": tumblr_response_iter,
    "flickr": flickr_response_iter,
    "twitter_rest": twitter_rest_response_iter,
    "twitter_stream": twitter_stream_response_iter

}


def iter_warc(filepath, services=(), entities=(), pretty=False):
    log.info("File %s", filepath)
    f = warc.WARCResponseFile(filepath)
    try:
        for count, record in enumerate(f):
            #Determine the service
            service = get_service(record)
            #Iterate over the iter for the service
            if service and (not services or service in services):
                for entity_type, entity_obj in service_to_iter_func_dict[service](record):
                    if not entities or entity_type in entities:
                        print json.dumps(entity_obj, indent=4 if pretty else None)

    finally:
        f.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--services",
                        help="A comma separated list of services to limit the results to. "
                             "Services are: twitter, tumblr, flickr, other.")
    parser.add_argument("--entities",
                        help="A comma separated list of entities to limit the results to. "
                             "Entities are: tweet, tumblr_blog, tumblr_post, flickr_photo, flickr_person.")
    parser.add_argument("--pretty", action="store_true", help="Format the json for viewing.")
    parser.add_argument("filepath", nargs="+", help="Filepath of the warc.")

    args = parser.parse_args()
    scvs = args.services.split(",") if args.services else ()
    ents = args.entities.split(",") if args.entities else ()

    for fp in args.filepath:
        iter_warc(fp, services=scvs, pretty=args.pretty, entities=ents)
