import en_core_web_sm
nlp = en_core_web_sm.load()

DEFAULT_PRON = "candidate"
DEFAULT_PRONPOSS = "their"
DEFAULT_WORDS = {
    "PRON": lambda t: DEFAULT_PRON,
    "DET": lambda t: DEFAULT_PRONPOSS if t.tag_ == "PRP$" else t.text
}


def identity_text(token):
  return token.text


def degenderify_token(token, options=None):
  merged_options = {**DEFAULT_WORDS, **(options or {})}
  word = merged_options.get(token.pos_, identity_text)(token)
  word = word[0].upper() + word[1:] if token.text[0].isupper() else word
  return word


def degenderify(text):
    doc = nlp(text)
    text_transformed_list = [degenderify_token(token) for token in doc]
    return " ".join(text_transformed_list)
