import numpy as np
import pandas as pd

def find_similar_items(item_index, ratings):
    ratings = np.array(ratings).T
    similarity_scores = []

    for i, item in enumerate(ratings):
        if i == item_index:
            continue

        v1 = ratings[item_index]
        v2 = item
        similarity = (np.dot(v1,v2))/(np.linalg.norm(v1)*np.linalg.norm(v2))
        similarity_scores.append((i, similarity))

    similarity_scores.sort(key=lambda x: x[1], reverse=True)
    return similarity_scores

def predict_rating_by_item(user_index, item_index, ratings, k):
    similar_items = find_similar_items(item_index, ratings)
    numerator = 0
    denominator = 0

    for i in range(k):
        similar_item_index, similarity_score = similar_items[i]

        if ratings[user_index][similar_item_index] == 0:
            continue

        numerator += similarity_score * ratings[user_index][similar_item_index]
        denominator += similarity_score

    if denominator == 0:
        return 0

    return numerator / denominator

def predict_ratings_item(ratings, k):
    predicted_ratings = []

    for i, user in enumerate(ratings):
        user_ratings = []

        for j, item_rating in enumerate(user):
            if item_rating == 0:
                predicted_rating = predict_rating_by_item(i, j, ratings, k)
                user_ratings.append(predicted_rating)
            else:
                user_ratings.append(item_rating)

        predicted_ratings.append(user_ratings)

    return predicted_ratings