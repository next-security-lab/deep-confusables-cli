from .utils.unicode import to_hex, to_unicode, to_decimal
import random
from itertools import islice, product
import requests
import time
import whois

latin_characters = [format(i + 32, '05x') for i in range(96)]


def similar_domain(domain, confusables):
    new_domain = ''
    for character in domain:
        character_hex = to_hex(character)
        if(character_hex not in latin_characters):
            new_domain = new_domain + character
        else:
            confusables_characters = confusables['characters'][character_hex]
            choice = random.choice(confusables_characters)
            new_domain = new_domain + to_unicode(choice)

    return new_domain

def similar_domains(domain, confusables, max_domains=100000,):
    try:
        d = domain.split('.')
        domain = d[0]
        tld = d[1]

        characters_lists = [list(map(to_unicode,
                                     confusables['characters'][to_hex(x)]
                                     )) for x in domain]

        cartesian_product = product(*characters_lists)

        return [''.join(new_domain) + '.{}'.format(tld)
                for new_domain in islice(cartesian_product, max_domains)]

    except IndexError:
        print('The domain must contain a dot.')
        return []


def check_domain(domain, t=5, verbose=False, whois=False):
    try:
        requests.get('http://{}'.format(domain))
        if verbose:
            print('The domain {} exists'.format(domain))
        if whois:
            w = who_is(domain)
            if(w is not None):
                print(w)
    except Exception:
        if verbose:
            print('The domain {} does not exist'.format(domain))
    time.sleep(t)


def check_domains(domains, t=5, verbose=False, whois=False):
    for domain in domains:
        check_domain(domain, t, verbose, whois)

def who_is(domain):
    try:
        return whois.whois(domain)
    except whois.parser.PywhoisError:
        print('Whois not found!')
