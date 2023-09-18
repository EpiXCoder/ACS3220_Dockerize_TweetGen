
import re
import random
source = 'Kiyosaki.txt'

class Markov():
    def __init__(self, source_text):
        self.words_list = self.read_text(source_text)
        self.start_words = self.start_words_gen()
        self.end_words = self.end_words_gen()
        self.distribution = self.distribution_gen()

    def read_text(self, source_text):
        text = open(source_text,"r").read().replace('"', '' )
        words_list = text.split()
        return words_list

    def start_words_gen(self):
        words_list = self.words_list
        start_words = []
        for word in words_list:
            if word[0].isupper() and word[-1] not in [".", "?", "!"]:
                start_words.append(word)
        # print(start_words)
        return start_words

    def end_words_gen(self):
        words_list = self.words_list
        end_words = []
        for word in words_list:
            if word[-1] in [".", "?", "!"]:
                end_words.append(word)
        # print(end_words)
        return end_words

    def sample_start_word(self):
        choice = random.choice(self.start_words)
        # print(f"Starter choice {choice}")
        return choice

    def distribution_gen(self):
        words_list = self.words_list
        word_distribution = dict()
        for word in words_list:
            if word not in word_distribution:
                word_distribution[word] = {}

        for i in range(len(words_list)-1):
            next_word = words_list[i + 1]
            if next_word in  word_distribution[words_list[i]]:
                word_distribution[words_list[i]][next_word] += 1
            else: 
                word_distribution[words_list[i]][next_word] = 1
        # print(word_distribution)
        return word_distribution

    def weighted_selection(self, distribution):
        start_words = self.start_words
        # print(start_words)
        starter = True
        words, weights = zip(*list(distribution.items()))
        while starter == True:
            selected_word = random.choices(words, weights=weights)[0]
            if selected_word not in start_words:
                starter == False 
                # print(f"selected_word: {selected_word}")
                return selected_word

    def generate_sentence(self):
        word_distribution = self.distribution
        next_word =  self.sample_start_word()
        end_words = self.end_words
        sentence_list = [next_word]
        while True:
            try:
                next_word = self.weighted_selection(word_distribution[next_word])
            except:
                return " ".join(sentence_list)
            sentence_list.append(next_word)
            if next_word in end_words:
                return " ".join(sentence_list)

if __name__ == '__main__':
    markov = Markov('yoga.txt')
    # markov = Markov('fishsample.txt')
    print(markov.generate_sentence())
