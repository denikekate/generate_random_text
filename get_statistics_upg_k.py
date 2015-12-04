import os
import cPickle as pickle
from collections import Counter, defaultdict
from time import time

path_to_books = './corpus/'
non_alpha_legal_symbols = set('.,!?')
ends_of_sentence = set('.?!')
name_patterns = set(['mrs', 'ms', 'mr'])

def sym_is_alpha(sym):
    legal_in_word = set(["'"])
    return sym.isalpha() or sym.isdigit() or (sym in legal_in_word)


def alpha(word):
    return all([sym_is_alpha(sym) for sym in word])


def read_text(path_to_books):
    text = []
    for path, dirs, file_names in os.walk(path_to_books):
        for file_name in file_names:
            if '.txt' in file_name:
                with open(os.path.join(path, file_name)) as f:
                    text.append(f.read())
                    break
    return '/n'.join(text)


def tokenize_text(text):
    words = text.split()
    tokens = []
    for word in words:
        sub_words = []
        start = 0
        chunk_type_isalpha = alpha(word[0])
        for ind, sym in enumerate(word):
            if alpha(sym) != chunk_type_isalpha:
                if chunk_type_isalpha or word[start:ind] in non_alpha_legal_symbols:
                    sub_words.append(word[start:ind].lower())
                start = ind
                chunk_type_isalpha = alpha(sym)
        if start < len(word):
            if chunk_type_isalpha or word[start:] in non_alpha_legal_symbols:
                sub_words.append(word[start:].lower())
        tokens.extend(sub_words)
    return map(lambda token: token.strip("'"), tokens)


def get_start_words(tokens):

    freq_start_words = Counter()

    for curr in xrange(1, len(tokens) - 1):
        if tokens[curr] in ends_of_sentence and tokens[curr - 1] not in name_patterns:
            freq_start_words[tokens[curr + 1]] += 1

    return freq_start_words


def get_all_freq(corpus, length):
    all_freq = defaultdict(Counter)
    for i in xrange(0, len(corpus) - length):
        if i % 500000 == 0:
            print ('{}/{} corpus {}'.format(i, len(corpus) - length - 1, length))
        all_freq[' '.join(corpus[i:i+length])][corpus[i+length]] += 1
    return all_freq


def main():
    start = time()
    text = read_text(path_to_books)
    tokens = tokenize_text(text)
    freq_start_words = get_start_words(tokens)
    pickle.dump(freq_start_words, open('freq_start_words.txt', "w"))
    print 'Got frequency of start words. Time: {}'.format(time()-start)
    freq_after_words = get_all_freq(tokens, 1)
    pickle.dump(freq_after_words, open('freq_after_words.txt', "w"))
    print 'Got frequency (window = 1). Time: {}'.format(time()-start)
    freq_after_phrases = get_all_freq(tokens, 2)
    pickle.dump(freq_after_phrases, open('freq_after_phrases.txt', "w"))
    print 'Got frequency (window = 2). Time: {}'.format(time()-start)
    print ('Time: {}'.format(time() - start))
    freq_after_long_phrases = get_all_freq(tokens, 3)
    pickle.dump(freq_after_long_phrases, open('freq_after_long_phrases.txt', "w"))
    print 'Got frequency (window = 3). Time: {}'.format(time()-start)
    print ('Pickling finished in {}'.format(time() - start))

if __name__ == '__main__':
    main()
