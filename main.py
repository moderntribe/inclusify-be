from degenderify import degenderify, degenderify_debug
from inclusify import inclusify, inclusify_debug


def parse_param(request, key):
    request_json = request.get_json()
    value = ''
    if request.args and key in request.args:
        value = request.args.get(key)
    elif request_json and key in request_json:
        value = request_json[key]
    return value


def old_degenderify_request(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    text = parse_param(request, "text")

    pron = parse_param(request, "pron") or None
    poss = parse_param(request, "poss") or None

    debug = parse_param(request, "debug") or None

    if not text:
        return f'No text found'

    if debug:
        return degenderify_debug(text, pron, poss)

    return degenderify(text, pron, poss)


def degenderify_request(request):
    # Set CORS headers for the preflight request
    if request.method == 'OPTIONS':
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }

        return ('', 204, headers)

    post_dict = request.get_json()
    if post_dict is not None:
        params = post_dict["params"]
        text = params.get("text")
        options = params.get("options", [])
        replace = params.get("replace", {})
        debug = params.get("debug", None)
    else:
        text = parse_param(request, "text")
        options = parse_param(request, "options") or []
        replace = parse_param(request, "replace") or {}
        debug = parse_param(request, "debug") or None

    if not text:
        res_text = f'No text found'

    if debug:
        res_text = inclusify_debug(text, options, replace)

    res_text = inclusify(text, options, replace)

    return (res_text, 200, {'Access-Control-Allow-Origin': '*'})
