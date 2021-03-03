import en_core_web_sm
nlp = en_core_web_sm.load()


DEFAULT_PRON = "candidate"
DEFAULT_PRONPOSS = "their"


class TranslatePron:
    def __init__(self, pron=None, pronposs=None):
        self.pron = pron or DEFAULT_PRON
        self.pronposs = pronposs or DEFAULT_PRONPOSS

    def translate_pron_with_token(self, token):
        if token.tag_ == 'PRP':
            return self.pron if token.text.lower() in ['he', 'she'] else token.text
        elif token.tag_ == 'PRP$':
            return self.pronposs if token.text.lower() in ['his', 'her'] else token.text


DEFAULT_WORDS = {
    "PRON": TranslatePron().translate_pron_with_token,
}


def identity_text(token):
    return token.text


def degenderify_token(token, options=None):
    merged_options = {**DEFAULT_WORDS, **(options or {})}
    method = merged_options.get(token.pos_, identity_text)
    word = method if isinstance(method, str) else method(token)
    word = word[0].upper() + word[1:] if token.text[0].isupper() else word
    return word


def degenderify(text, pron=None, poss=None):
    options = {'PRON': TranslatePron(pron, poss).translate_pron_with_token}
    doc = nlp(text)
    transformed_list = [degenderify_token(token, options) for token in doc]
    return " ".join(transformed_list)


###############################################################################
class Printer():
    text = ""

    def print(self, line):
        print(line)
        self.text += line+"\n"

    def get_text(self):
        return "<pre>"+self.text+"</pre>"


def degenderify_debug(text, pron=None, poss=None):
    options = {'PRON': TranslatePron(pron, poss).translate_pron_with_token}

    doc = nlp(text)
    p = Printer()
    p.print("======== ENTITIES ======== ")
    # Iterate over the predicted entities
    for ent in doc.ents:
        # Print the entity text and its label
        print(ent.text, ent.label_)
    p.print("======== TOKENS ======== ")
    for token in doc:
        # Get the token text, part-of-speech tag and dependency label
        token_text = token.text
        token_pos = token.pos_
        token_dep = token.dep_
        token_tag = token.tag_
        # This is for formatting only
        new_word = degenderify_token(token, options)
        word_to_pring = new_word if new_word != token_text else "="
        p.print(
            f"{token_text:<12}{word_to_pring:<12}{token_tag:<10}{token_pos:<10}{token_dep:<10}")
    return p.get_text()
