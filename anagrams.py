import sys
import re

def sort_chars(words):
    '''
    Sorts the chars for easy comparison.
    '''
    joined = "".join(words)
    sorted_chars = sorted(joined)
    return "".join(sorted_chars)


def extract_bigrams(words):
    '''
    Gets all unique bigrams.
    (Will still have reversed duplicates)
    '''
    words = set(words)
    bigrams = set()
    stopped = set()

    for word in words:
        stopped.add(word)
        without = words - stopped
        only = [word] * len(without)
        bigrams |= set(zip(only, without))

    return bigrams


def find_matches(bigrams, minlen=2):
    '''
    Uses dict to find all matches, only displays lists of matches with len >=
    minlen.
    '''
    all_matches = {}
    picked = {}
    for bigram in bigrams:
        hashed = sort_chars(bigram)
        if hashed not in all_matches:
            all_matches[hashed] = set()
            picked[hashed] = set()

        bigram_set = set(bigram)
        if not picked[hashed].isdisjoint(bigram_set):
            continue
        picked[hashed] |= bigram_set

        all_matches[hashed].add(tuple(bigram_set))

    return [value for key, value in all_matches.items() if len(value) >= minlen]


def print_matches(matches):
    '''
    Pretty-print the matches.
    '''
    for match in matches:
        print ", ".join(sorted([" ".join(sorted(pair)) for pair in match]))


def main(text, wordlen=4, minpairlen=2):
    _text = text
    text = re.sub(r'[^a-z0-9]+', ' ',
                text.lower())
    words = sorted([word for word in set(re.split(r'\s+', text)) if len(word) >= wordlen])
    bigrams = extract_bigrams(words)
    matches = find_matches(bigrams, minlen=minpairlen)
    print_matches(matches)


if __name__ == '__main__':
    kwargs = {}
    if len(sys.argv) > 1:
        argv1 = sys.argv[1].lower()
        if argv1 == '-h' or argv1 == '--help':
            print "Reads text from stdin, and prints out anagrams.\n\n    Usage: cat text | python anagrams.py [minimum word length] [minimum pair count]"
            sys.exit(1)
        kwargs['wordlen'] = int(argv1)
    if len(sys.argv) > 2:
        kwargs['minpairlen'] = int(sys.argv[2])

    main(sys.stdin.read(), **kwargs)


