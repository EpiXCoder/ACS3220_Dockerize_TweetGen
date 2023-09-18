
import re
import random
source = 'Kiyosaki.txt'

class Markov():
    def __init__(self, source_text, order):
        self.order = order
        self.words_list = self.read_text(source_text)
        self.start_wordgroup = self.start_words_gen()
        self.end_words = self.end_words_gen()
        self.distribution = self.distribution_gen()
        

    def read_text(self, source_text):
        text = open(source_text,"r").read().replace('"', '' )
        words_list = text.split()
        # print(len(words_list))
        return words_list

    def start_words_gen(self):
        order = self.order
        words_list = self.words_list
        start_wordgroup = []
        for i in range(len(words_list) - order):
            if words_list[i][0].isupper() and words_list[i+ order -1][-1] not in [".", "?", "!"]:
                start_wordgroup.append(tuple(words_list[i:i+order]))
        # print(start_words)
        return start_wordgroup

    def end_words_gen(self):
        words_list = self.words_list
        end_words = []
        for word in words_list:
            if word[-1] in [".", "?", "!"]:
                end_words.append(word)
        # print(end_words)
        return end_words

    def sample_start_word(self):
        choice = random.choice(self.start_wordgroup)
        # print(f"Starter choice {choice}")
        return choice
    
    def distribution_gen(self):
        words_list = self.words_list
        order = self.order
        word_distribution = dict()
        for i in range(len(words_list) - order):
            key_n_order = tuple(words_list[i:i+order])
            if key_n_order not in word_distribution:
                word_distribution[key_n_order] = {}

        for i in range(len(words_list)-order):
            key_n_order = tuple(words_list[i:i+order])
            next_wordgroup = tuple(words_list[(i+(order-1)):(i+(order-1)+order)])
            if next_wordgroup in  word_distribution[key_n_order]:
                word_distribution[key_n_order][next_wordgroup] += 1
            else: 
                word_distribution[key_n_order][next_wordgroup] = 1
        # print(word_distribution)
        return word_distribution

    def weighted_selection(self, choices):
        weighted_list = [(key, 1) for key in choices.keys()]
        selected_tuple = random.choices(weighted_list, weights=[w for _, w in weighted_list])[0][0]
        return selected_tuple
    
    def join_tuples(self, list):
        # Create a list of all but the last elements of the tuples
        partial_sentences = [t[:-1] for t in list]

        # Join the partial sentences to form the complete sentence
        sentence = ' '.join([word for partial_sentence in partial_sentences for word in partial_sentence])

        # Add the last element of the last tuple to the sentence
        sentence += (' ' + list[-1][-1])
        split_string = re.split(r'([.?!])', sentence)
        new_string = split_string[0] + split_string[1]
        return new_string

    def endword_checker(self, tuple):
        end_words = self.end_words
        for word in tuple:
            if word in end_words:
                return True
            else:
                return False

    def generate_sentence(self):
        word_distribution = self.distribution
        # print(word_distribution)
        next_wordgroup =  self.sample_start_word()
        # print(f"Starter choice {next_wordgroup}")
        sentence_list = [next_wordgroup]
        # print(f"Start SL {sentence_list}")

        while True:
            try:
                next_wordgroup = self.weighted_selection(word_distribution[next_wordgroup])
            except:
                return self.join_tuples(sentence_list)
            sentence_list.append(next_wordgroup)
            # print(f"sentence list append: {sentence_list}")
            if self.endword_checker(next_wordgroup):
                return self.join_tuples(sentence_list)

if __name__ == '__main__':
    # markov = Markov('yoga.txt')
    # markov = Markov('Kiyosaki.txt',2) 
    markov = Markov('fishsample.txt', 2)
    # print(markov.start_wordgroup)
    print(markov.generate_sentence())
    print(markov.distribution_gen())
    markov.read_text('yoga.txt')
