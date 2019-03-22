#!/usr/bin/env python
# -*- coding: utf-8 -*-


import json
import pdb
import requests
import sys
import traceback


def get_movies_from_tastedive(movie):
    params = {"q": movie, "type": "movies", "limit": 5}
    response = requests.get("https://tastedive.com/api/similar", params=params)
    return response.json()


def extract_movie_titles(movies):
    titles = []
    for result in movies["Similar"]["Results"]:
        titles.append(result["Name"])
    return titles


def get_related_titles(movies):
    all_related_titles = []
    for movie in movies:
        related_movies = get_movies_from_tastedive(movie)
        related_titles = extract_movie_titles(related_movies)
        for related_title in related_titles:
            if related_title not in all_related_titles:
                all_related_titles.append(related_title)
    return all_related_titles


def get_omdb_api_key():
    with open("omdb_api_key.json", "r") as inf:
        payload = json.load(inf)
    return payload


def get_movie_data(title):
    url = "http://www.omdbapi.com/"
    params = {"r": "json", "t": title}
    params = {**params, **get_omdb_api_key()}
    response = requests.get(url, params=params)
    return response.json()


def get_movie_rating(movie_data):
    ratings = movie_data["Ratings"]
    for rating in ratings:
        if rating["Source"] == "Rotten Tomatoes":
            value = rating["Value"]
            if value[-1] == "%":
                value = value[:-1]
            return int(value)
    return 0


def get_sorted_recommendations(movies):
    recommendations = []
    related_titles = get_related_titles(movies)
    for title in related_titles:
        data = get_movie_data(title)
        rating = get_movie_rating(data)
        recommendations.append((title, rating))
    recommendations.sort(key=lambda t: t[1], reverse=True)
    return [recommendation[0] for recommendation in recommendations]


if __name__ == "__main__":
    try:
        movies = ["Bridesmaids", "Sherlock Holmes"]
        if len(sys.argv) > 1:
            movies = sys.argv[1:]
        recommendations = get_sorted_recommendations(movies)
        print("\n".join(recommendations))
    except:
        traceback.print_exc()
        pdb.post_mortem()
