import numpy as np
import pandas as pd


def find_similar_users(user_index, ratings):
    similarity_scores = []

    for i, user in enumerate(ratings):
        if i == user_index:
            continue

        v1 = ratings[user_index]
        v2 = user
        similarity = (np.dot(v1,v2))/(np.linalg.norm(v1)*np.linalg.norm(v2))
        similarity_scores.append((i, similarity))

    similarity_scores.sort(key=lambda x: x[1], reverse=True)
    return similarity_scores


def average_rating(user_index, ratings):
  s, k = 0, 0
  for elem in ratings[user_index]:
    if elem != 0:
      s += elem
      k += 1
  return s / k


def predict_rating(user_index, movie_index, ratings, k):
    similar_users = find_similar_users(user_index, ratings)
    numerator = 0
    denominator = 0
    user_av_rat = average_rating(user_index, ratings)

    for i in range(k):
        similar_user_index, similarity_score = similar_users[i]

        if ratings[similar_user_index][movie_index] == 0:
            continue

        rat_av = average_rating(similar_user_index, ratings)
        numerator += similarity_score * (ratings[similar_user_index][movie_index]-rat_av)
        denominator += similarity_score

    if denominator == 0:
        return 0

    return user_av_rat + numerator / denominator



def predict_ratings(ratings, k):
    predicted_ratings = []

    for i, user in enumerate(ratings):
        user_ratings = []

        for j, movie_rating in enumerate(user):
            if movie_rating == 0:
                predicted_rating = predict_rating(i, j, ratings, k)
                user_ratings.append(predicted_rating)
            else:
                user_ratings.append(movie_rating)

        predicted_ratings.append(user_ratings)

    return predicted_ratings

