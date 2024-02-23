import numpy as np
import networkx as nx
from nltk.cluster.util import cosine_distance

class Summarizer():
    def __init__(self):
        # import stop words from file
        self.stop_words = []
        with open("util/stop_words_polish.txt", "r") as stop_words_file:
            for line in stop_words_file:
                self.stop_words.append(line.strip())

    # calculate two sentences similarity based on cosine distance
    def _calculate_sentences_similarity(self, sentence_1, sentence_2):
        sentence_1 = [word.lower() for word in sentence_1]
        sentence_2 = [word.lower() for word in sentence_2]

        all_words = list(set(sentence_1 + sentence_2))

        vector_1 = np.zeros(len(all_words))
        vector_2 = np.zeros(len(all_words))

        for word in sentence_1:
            if word not in self.stop_words:
                vector_1[all_words.index(word)] += 1
        
        for word in sentence_2:
            if word not in self.stop_words:
                vector_2[all_words.index(word)] += 1

        return 1 - cosine_distance(vector_1, vector_2)

    # calculate similarity matrix
    def _calculate_similarity_matrix(self, sentences):
        matrix = np.zeros((len(sentences), len(sentences)))
        for i in range(len(sentences)):
            for j in range(len(sentences)):
                if i != j:
                    matrix[i][j] = self._calculate_sentences_similarity(sentences[i], sentences[j])
        return matrix

    def summarize(self, text, summarize_factor):
        # split text into sentences
        sentences = []
        for sentence in text.split("."):
            sentences.append(sentence.replace("[^a-zA-Z]", " ").split(" "))
        sentences.pop()
        
        # calculate similarity matrix
        similarity_matrix = self._calculate_similarity_matrix(sentences)
        # calculate sentences scores based on pagerank algorithm
        similarity_graph = nx.from_numpy_array(similarity_matrix)
        scores = nx.pagerank(similarity_graph)

        # selection of sentence indexes for summary
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        num_sentences_to_keep = int(summarize_factor * len(sentences))
        important_sentence_indices = [index for index, _ in sorted_scores[:num_sentences_to_keep]]
        important_sentence_indices.sort()

        # merging sentences
        summarized_text = [" ".join(sentences[i]) for i in important_sentence_indices]
        output_text = ".".join(summarized_text)
        output_text_length = len(output_text.split(" "))

        return output_text, output_text_length
