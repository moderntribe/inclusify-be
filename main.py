from degenderify import degenderify


def parse_param(request, key):
    request_json = request.get_json()
    value = ''
    if request.args and key in request.args:
        value = request.args.get(key)
    elif request_json and key in request_json:
        value = request_json[key]
    return value


def degenderify_request(request):
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

    if not text:
        return f'No text found'

    return degenderify(text, pron)
