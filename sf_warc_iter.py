import warc
import json
import argparse
import socialfeedtools.utils as utils
import logging

log = logging.getLogger(__name__)


def tumblr_response_iter(record):
    json_obj = utils.extract_json_from_payload(record)
    yield "tumblr_blog", json_obj["response"]["blog"]
    for post in json_obj["response"]["posts"]:
        yield "tumblr_post", post


def flickr_response_iter(record):
    json_obj = utils.extract_json_from_payload(record)
    if "photo" in json_obj:
        yield "flickr_photo", json_obj["photo"]
    elif "person" in json_obj:
        yield "flickr_person", json_obj["person"]


def twitter_response_iter(record):
    json_obj = utils.extract_json_from_payload(record)
    if json_obj:
        for tweet in json_obj:
            yield "tweet", tweet


to_service_dict = {
    utils.is_tumblr_url: "tumblr",
    utils.is_flickr_url: "flickr",
    utils.is_twitter_url: "twitter"
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
    "twitter": twitter_response_iter

}


def iter_warc(filepath, services=(), entities=(), pretty=False):
    log.info("File %s", filepath)
    f = warc.open(filepath)
    try:
        for record in f:
            if record.type == 'response':
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
