# social-feed-tools

Proof-of-concept tools for working with social media harvests recorded in WARCs.

## sf_warc_lister

Lists the social media platform API calls that are contained in the WARC.

    usage: sf_warc_lister.py [-h] [--services SERVICES] filepath [filepath ...]

    positional arguments:
      filepath             Filepath of the warc.

    optional arguments:
      -h, --help           show this help message and exit
      --services SERVICES  A comma separated list of services to limit the results
                           to. Services are: twitter, tumblr, flickr, other.

## sfm_warc_iter

Iterates the individual JSON results that are contained in the WARC.

    usage: sf_warc_iter.py [-h] [--services SERVICES] [--entities ENTITIES]
                           [--pretty]
                           filepath [filepath ...]

    positional arguments:
      filepath             Filepath of the warc.

    optional arguments:
      -h, --help           show this help message and exit
      --services SERVICES  A comma separated list of services to limit the results
                           to. Services are: twitter_rest, twitter_stream, tumblr, flickr, other.
      --entities ENTITIES  A comma separated list of entities to limit the results
                           to. Entities are: tweet, tumblr_blog, tumblr_post,
                           flickr_photo, flickr_person.
      --pretty             Format the json for viewing.
