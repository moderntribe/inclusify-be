import en_core_web_sm
nlp = en_core_web_sm.load()

DEFAULT_PRON = "candidte"
DEFAULT_PRONPOSS = "their"
DEFAULT_WORDS = {
    "PRON": lambda _: DEFAULT_PRON,
    "DET": lambda t: DEFAULT_PRONPOSS if t.tag_ == "PRP$" else t.text
}


def identity_text(token):
  return token.text


def degenderify_token(token, options=None):
  merged_options = {**DEFAULT_WORDS, **(options or {})}
  method = merged_options.get(token.pos_, identity_text)
  word = method if isinstance(method, str) else method(token)
  word = word[0].upper() + word[1:] if token.text[0].isupper() else word
  return word


def degenderify(text, pron=None):
    options = None
    if pron:
        options = {'PRON': pron}
    doc = nlp(text)
    transformed_list = [degenderify_token(token, options) for token in doc]
    return " ".join(transformed_list)
