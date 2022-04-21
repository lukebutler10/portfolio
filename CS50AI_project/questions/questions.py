import sys
import os
import string
import nltk
import math


FILE_MATCHES = 1
SENTENCE_MATCHES = 1


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

    os.chdir(directory) #may need some more work on if the directories don't match up
    cd = os.getcwd()
    files = os.listdir()

    file_dict = dict()

    for file in files:
        with open(file, encoding = "utf8") as f:
            text = f.read()
        f.close()
        file_dict[file] = text

    return file_dict
        
punct = string.punctuation
stopwords = nltk.corpus.stopwords.words("english")

def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    tkn = nltk.word_tokenize(document)
    tkn = [word.lower() for word in tkn]
    for word in tkn[:]:
        for char in word:
            if char in punct:
                try:
                    while True:
                        tkn.remove(word)
                except ValueError:
                    pass
        if word in stopwords:
            try:
                while True:
                    tkn.remove(word)
            except ValueError:
                pass
            
    return tkn

def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    total_docs = len(documents)
    idf_dict = dict()
    for doc_name in documents.keys():
        for word in documents[doc_name]:
            if word in idf_dict.keys():
                pass
            else:
                counter = 0
                for word_list in documents.values():
                    if word in word_list:
                        counter += 1
                    else:
                        pass
                idf_value = math.log(total_docs/counter)
                idf_dict[word] = idf_value
    return idf_dict


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    tfidf_dict = dict()
    for filename in files.keys():
        sum_tfidf = 0
        for word in query:
            tf = files[filename].count(word)
            tfidf = tf*idfs[word]
            sum_tfidf += tfidf
            
        tfidf_dict[filename] = sum_tfidf
    
    sorted_files = sorted(tfidf_dict.items(), key = lambda x:x[1], reverse=True)
    sorted_files = [x[0] for x in sorted_files]
    top_n = sorted_files[:n]
    
    return top_n


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    idf_dict = dict()
    for sentence in sentences.keys():
        sum = 0
        for word in query:
            if word not in sentences[sentence]:
                pass
            else:
                sum += idfs[word]
            
        idf_dict[sentence] = sum
        
    def density(sentence_x,query_x): #sentence_x should be the "sentence name", query_x should be the query given in top_sentences
        counter = 0
        for word in sentences[sentence_x]:
            if word in query_x: 
                counter +=1
            else:
                pass
        
        return counter / len(sentences[sentence_x])
    
    sorted_sentences = sorted(idf_dict.items(), key = lambda x:(x[1],density(x[0],query)),reverse=True)
    sorted_sentences = [x[0] for x in sorted_sentences]
    top_n = sorted_sentences[:n]
    
    return top_n


if __name__ == "__main__":
    main()
