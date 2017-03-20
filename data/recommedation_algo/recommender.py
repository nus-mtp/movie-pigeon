"""
    Main class for recommendation operations

    # calculate raw score

    # get relevant movies pool (crude criteria) (waiting to be classified)

    # for every movie in pool
        # calculate multiplier : classification (logistic regression)
        # obtain final score (expected output)
        # sort and rank
        # store in database

"""
import logging
from db_handler import DatabaseHandler
from public_data.controller import ETLController
from sklearn import linear_model
from datetime import datetime
from gensim import corpora, models, similarities
from collections import defaultdict


import warnings


class Recommender:

    def __init__(self, user_id):
        self.controller = ETLController()
        self.db = DatabaseHandler()
        self.user_id = user_id

    def run(self):
        # for every user update scale
        # for every user generate recommendation if not enough
        pass

    def update_user_scale(self):
        """
        update the user scale in the database
        :return:
        """
        regressors = []
        responses = []

        # calculate raw score
        user_rating_records = self.db.get_user_ratings(self.user_id)  # join public rating remove None

        # TODO: No rating?

        for record in user_rating_records:
            current_id = record[0]

            # regressors
            public_rating_records = self.db.get_public_rating(current_id)
            if not public_rating_records:
                self.controller.update_single_movie_rating(current_id)  # update rating
                public_rating_records = self.db.get_public_rating(current_id)

            public_rating_records = sorted(public_rating_records, key=lambda x: x[1])  # sort records -> replace by sql
            current_set = []
            for regressor in public_rating_records:
                current_set.append(regressor[3])
            regressors.append(current_set)

            # response
            user_rating = record[1]
            responses.append(user_rating)

        regression = linear_model.LinearRegression()
        regression.fit(regressors, responses)
        weights = regression.coef_

        self.db.load_weights(weights, self.user_id)

    def update_user_recommendation(self):
        """
        update the recommendations in database,
        each user will be generated up to 10 recommended movies
        upon executing this function

        Consider at least 8.0 to be recommended
        :return:
        """
        result_list = []
        current_year = datetime.now().strftime("%Y")

        while True:
            if len(result_list) == 10:
                break

            user_ratings = self.db.get_user_ratings(self.user_id)

            # labelling responses
            label = []
            attributes = []
            for user_rating in user_ratings:
                movie_id, score = user_rating
                attributes.append([movie_id])
                if score >= 8.0:  # consider as favorable movie
                    label.append([movie_id, 1])
                else:
                    label.append([movie_id, 0])

            # TODO: quantify available data fields, make logistic regression model
            # genre, actors, runtime
            for attribute in attributes:
                movie_id = attribute[0]
                public = self.db.get_movie_data_by_id(movie_id)
                print(public)

            # TODO: after classification, iterate through movie pools by year and store recommendation

            break

def test():
    # Tokenize Corpus and filter out anything that is a
    # stop word or has a frequency <1

    documents = [
        'Car Insurance',  # doc_id 0
        'Car Insurance Coverage',  # doc_id 1
        'Auto Insurance',  # doc_id 2
        'Best Insurance',  # doc_id 3
        'How much is car insurance',  # doc_id 4
        'Best auto coverage',  # doc_id 5
        'Auto policy',  # doc_id 6
        'Car Policy Insurance',  # doc_id 7
    ]

    stoplist = set(['is', 'how'])

    texts = [[word.lower() for word in document.split()
              if word.lower() not in stoplist]
             for document in documents]

    frequency = defaultdict(int)
    for text in texts:
        for token in text:
            frequency[token] += 1
    texts = [[token for token in text if frequency[token] > 1]
             for text in texts]

    dictionary = corpora.Dictionary(texts)
    # doc2bow counts the number of occurences of each distinct word,
    # converts the word to its integer word id and returns the result
    # as a sparse vector

    corpus = [dictionary.doc2bow(text) for text in texts]
    lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=2)

    doc = "giraffe poop car murderer"
    vec_bow = dictionary.doc2bow(doc.lower().split())

    # convert the query to LSI space
    vec_lsi = lsi[vec_bow]
    index = similarities.MatrixSimilarity(lsi[corpus])

    # perform a similarity query against the corpus
    sims = index[vec_lsi]
    sims = sorted(enumerate(sims), key=lambda item: -item[1])


if __name__ == '__main__':
    warnings.filterwarnings(action="ignore", module="scipy", message="^internal gelsd")  # ignore lapack related warning
    test()
    # recommender = Recommender('8')
    # recommender.update_user_recommendation()
