import csv
import json
import en_core_web_sm
nlp = en_core_web_sm.load()


def clean_terms(terms_line):
  return [a.strip() for a in terms_line.lower().split(',')]


def is_slur(word):
    hate_dict = list(csv.DictReader(open("hate.csv")))
    for row in hate_dict:
        if word.lower() in clean_terms(row["Term"]):
            return row


def deracify(text):
    """ Search coincidences in words.
    """
    # Process the text
    doc = nlp(text)

    result = []

    for token in doc:
        # Get the token text, part-of-speech tag and dependency label
        token_text = token.text
        token_pos = token.pos_
        token_dep = token.dep_
        # This is for formatting only
        #print(f"{token_text:<12}{token_pos:<10}{token_dep:<10}")
        if token_pos == 'PUNCT':
            result.append(token_text)
        else:
            slur_result = is_slur(token_text)
            if slur_result:
                result.append({
                    'symbol': token_text,
                    'synonyms': [slur_result['Targeted Demographic']],
                    'info': slur_result,
                    'flags': {
                        'gender': False,
                        'race': True
                    }
                })
            else:
                result.append(token_text)
    return result


# json.dumps(deracify(text))
