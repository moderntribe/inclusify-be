import html
import en_core_web_sm
nlp = en_core_web_sm.load()

DEFAULT_PERSON = "Person"
DEFAULT_PRON = "candidate"
DEFAULT_POSS = "their"
DEFAULT_LOCATION = "location"
DEFAULT_GPE = "place"


TAGS = {
    'PERSON': 'PERSON',
    'PRON': 'PRON_GENDER',
    'POSS': 'PRON_POSS',
    'LOCATION': 'LOCATION',
    'GPE': 'GPE',
}

REPLACE_TAGS = {
    'PERSON': DEFAULT_PERSON,
    'PRON_GENDER': DEFAULT_PRON,
    'PRON_POSS': DEFAULT_POSS,
    'LOCATION': DEFAULT_LOCATION,
    'GPE': DEFAULT_GPE,
}

CSS_TAGS = {
    'PERSON': 'bg-green-100 text-green-700',
    'PRON_GENDER': 'bg-purple-100 text-purple-700',
    'PRON_POSS': 'bg-indigo-100 text-indigo-700',
    'LOCATION': 'bg-red-100 text-red-700',
    'GPE': 'bg-red-100 text-red-700',
}

TYPE_TAGS = {
    'PERSON': 'tag-person',
    'PRON_GENDER': 'tag-pron_gender',
    'PRON_POSS': 'tag-pron_poss',
    'LOCATION': 'tag-location',
    'GPE': 'tag-gpe',
}


class Placeholders:
    i = 0
    values = {}

    def get_key(self):
        self.i = self.i + 1
        return f'tag_{self.i}'

    def add(self, text):
        key = self.get_key()
        self.values[key] = text
        return key


def generate_html_tag(tag, original):
    return f'<span class="{CSS_TAGS[tag]}" data-type={TYPE_TAGS[tag]} data-original="{html.escape(original)}" title="{html.escape(original)}">{REPLACE_TAGS[tag]}</span>'


def replace_ner(p, text, ner_label='PERSON', tag=TAGS['PERSON']):
    clean_text = text
    doc = nlp(text)
    ents_list = []
    for ent in reversed(doc.ents):
        if ent.label_ == ner_label:
            key = p.add(generate_html_tag(tag, ent.text))
            clean_text = clean_text[:ent.start_char] + \
                'HH_'+key+'_HH' + clean_text[ent.end_char:]
            ents_list.append(ent)
    return clean_text, list(reversed(ents_list))


def replace_gneric(p, text, target_list=[], tag='PERSON'):
    clean_text = ''
    doc = nlp(text)
    for token in doc:
        replace_word = token.text
        # Get the token text, part-of-speech tag and dependency label
        token_text = token.text
        token_pos = token.pos_
        token_dep = token.dep_
        token_tag = token.tag_

        if token_text.lower() in target_list:
            key = p.add(generate_html_tag(tag, token_text))
            replace_word = 'HH_'+key+'_HH'

        clean_text += ' ' + replace_word
    return clean_text


def replace_pron(p, text, target_list=['he', 'she'], tag=TAGS['PRON']):
    return replace_gneric(p, text, target_list, tag)


def replace_poss(p, text, target_list=['his', 'her'], tag=TAGS['POSS']):
    return replace_gneric(p, text, target_list, tag)


def inclusify(text, options, replace={}):

    options = options or ['name', 'gender', 'address']
    global REPLACE_TAGS
    REPLACE_TAGS[TAGS['PERSON']] = replace.get('pron', DEFAULT_PRON)
    REPLACE_TAGS[TAGS['PRON']] = replace.get('poss', DEFAULT_POSS)
    REPLACE_TAGS[TAGS['POSS']] = replace.get('person', DEFAULT_PERSON)
    REPLACE_TAGS[TAGS['LOCATION']] = replace.get('location', DEFAULT_LOCATION)
    REPLACE_TAGS[TAGS['GPE']] = replace.get('gpe', DEFAULT_GPE)

    # print('REPLACE_TAGS', REPLACE_TAGS)

    p = Placeholders()
    clean_text = html.escape(text)

    # Replace names
    if 'name' in options:
        clean_text, names_list = replace_ner(p, clean_text)
    
    # Replace locations and gpe
    if 'location' in options:
        clean_text, names_list = replace_ner(p, clean_text, 'GPE', TAGS['GPE'])
        clean_text, names_list = replace_ner(p, clean_text, 'LOCATION', TAGS['LOCATION'])

    # Replace gender
    if 'gender' in options:
        clean_text = replace_pron(p, clean_text)
        clean_text = replace_poss(p, clean_text)

    # print(names_list)
    return clean_text.replace("HH_", "{").replace("_HH", "}").format(**p.values)


def inclusify_debug(text, options, replace={}):
    return inclusify(text, options, replace)
