from degenderify import degenderify


TEXT_KEY = "text"


def degenderify_request(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    request_json = request.get_json()
    if request.args and TEXT_KEY in request.args:
        text = request.args.get(TEXT_KEY)
    elif request_json and TEXT_KEY in request_json:
        text = request_json[TEXT_KEY]

    if not text:
        return f'No text found'

    return degenderify(text)
