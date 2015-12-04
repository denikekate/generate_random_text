import cPickle as pickle
import numpy as np
from time import time
from collections import defaultdict


#some globals for beautiful sentence construction
ends_of_sentence = ['.','?','!']
non_alpha = [',','-']
name_patterns = set(['mrs', 'ms', 'mr'])
#number of sentences
N = 1000


def normalize_freq(freq_after_phrases):
    prob_after_phrases = defaultdict(dict)
    for phrase, freq_after_phrase in freq_after_phrases.items():
        norm = float(sum(freq_after_phrase.values()))
        for next_word, freq in freq_after_phrase.items():
            prob_after_phrases[phrase][next_word] = freq_after_phrase[next_word] / norm
    return prob_after_phrases


def generate_sentence(prob_start_words, prob_after_words, prob_after_phrases, prob_after_long_phrases):
    sentence = []
    word = None
    while not (word in ends_of_sentence and
                   all([name_part not in sentence[-1] for name_part in name_patterns])):
        if len(sentence) == 0:
            word = np.random.choice(prob_start_words.keys(), 1, p=prob_start_words.values())[0]
        elif len(sentence) == 1:
            word = np.random.choice(prob_after_words[word].keys(), 1, p=prob_after_words[word].values())[0]
        elif len(sentence) == 2:
            phrase = ' '.join(sentence[-2:])
            word = np.random.choice(prob_after_phrases[phrase].keys(), 1, p=prob_after_phrases[phrase].values())[0]
        else:
            phrase = ' '.join(sentence[-3:])
            word = np.random.choice(prob_after_long_phrases[phrase].keys(), 1, p=prob_after_long_phrases[phrase].values())[0]
        sentence.append(word)
    return sentence


def gimme_beautiful_sentence(sentence):
    try:
        parts = ['ll', 's', 'd', 't', 'm', 're']
        beauty = []
        sentence = filter(lambda x: x != "'", sentence)
        sentence = map(lambda x: x if x.strip() != 'i' else 'I', sentence)
        while (sentence != '') and (sentence[0] in parts or sentence[0] in ends_of_sentence or sentence[0] == ','):
            print ("wrong sentence")
            sentence = sentence[1:]
        sentence[0] = sentence[0].capitalize()
        for curr, word in enumerate(sentence):
            if word in parts:
                beauty[-1] = "{}'{}".format(beauty[-1],word)
            elif word == ',' or word in ends_of_sentence:
                beauty[-1] = ''.join([beauty[-1], word])
            else:
                beauty.append(word)
    except IndexError:
        print ('IndexError{}'.format(sentence))
        return ''
    return ' '.join(beauty).strip()


def generate_text(n_sentences, prob_start_words, prob_after_words, prob_after_phrases, prob_after_long_phrases):
    random_text = []
    for i in range(n_sentences):
        sentence =  generate_sentence(prob_start_words, prob_after_words, prob_after_phrases, prob_after_long_phrases)
        if sentence != []:
            random_text.append(gimme_beautiful_sentence(sentence))
    return ' '.join(random_text)


def main():
    start = time()
    freq_start_words = pickle.load(open('freq_start_words.txt'))
    prob_start_words = {}
    norm = sum(freq_start_words.values())
    for key, val in freq_start_words.items():
        prob_start_words[key] = float(val)/float(norm)
    print 'Got probability of start words. Time: {}'.format(time()-start)
    prob_after_words = normalize_freq(pickle.load(open('freq_after_words.txt')))
    print 'Got probability (window = 1). Time: {}'.format(time()-start)
    prob_after_phrases = normalize_freq(pickle.load(open('freq_after_phrases.txt')))
    print 'Got probability (window = 2). Time: {}'.format(time()-start)
    prob_after_long_phrases = normalize_freq(pickle.load(open('freq_after_long_phrases.txt')))
    print 'Got probability (window = 3). Time: {}'.format(time()-start)
    random_text = generate_text(N, prob_start_words, prob_after_words, prob_after_phrases, prob_after_long_phrases)
    with open('random_text.txt','w') as f:
        f.write(random_text)
    print 'Generated random text. Time: {}'.format(time()-start)


if __name__ == '__main__':
    main()
