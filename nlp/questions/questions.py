import math
import os
import string
import sys
from functools import cmp_to_key

import nltk

nltk.download('stopwords')

FILE_MATCHES = 1
SENTENCE_MATCHES = 1

nltk.download('stopwords')


def main():
    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    files = {}
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            with open(file_path, mode='r', encoding='utf8') as file:
                files[filename] = file.read()

    return files


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    tokens = nltk.word_tokenize(document)
    lowercased_tokens = [token.lower() for token in tokens]
    filtered_tokens = [token for token in lowercased_tokens if token not in string.punctuation and token not in nltk.corpus.stopwords.words("english")]
    return filtered_tokens


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    num_of_documents = {}
    for document in documents:
        explored_words = set()
        for word in documents[document]:
            if word not in explored_words:
                explored_words.add(word)
                num_of_documents[word] = num_of_documents[word] + 1 if word in num_of_documents else 1

    return {word: math.log(len(documents) / num_of_documents[word]) for word in num_of_documents}


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    file_ranks = {}
    for file in files:
        file_ranks[file] = 0
        for word in query:
            file_ranks[file] += files[file].count(word) * idfs[word]

    return sorted(file_ranks, key=file_ranks.get, reverse=True)[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    sentence_ranks = {}
    for sentence in sentences:
        sentence_ranks[sentence] = (0, 0)
        for word in query:
            if word in sentences[sentence]:
                sentence_ranks[sentence] = (
                    sentence_ranks[sentence][0] + idfs[word],
                    sentence_ranks[sentence][1] + sentences[sentence].count(word) / len(sentences[sentence])
                )

    sorted_sentence_ranks = sorted(sentence_ranks.items(), key=cmp_to_key(query_term_density_compare), reverse=True)
    return [sentence_rank[0] for sentence_rank in sorted_sentence_ranks][:n]


def query_term_density_compare(item1, item2):
    if item1[1][0] == item2[1][0]:
        return item1[1][1] - item2[1][1]

    return item1[1][0] - item2[1][0]


if __name__ == "__main__":
    main()
