# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 18:00:04 2019

@author: Lum Hui Yen
"""

import pandas as pd
from datetime import date

movies = pd.read_csv("E:\Documents\mov.csv", delimiter=',',
                     header=None,
                     names=['movieID','title','genres','release','ratings','rated','language'])

#switch case to define type of genres to be stored into an array
def switchGenres(genre):
    switcher = {
            1: "Action",
            2: "Comedy",
            3: "Crime",
            4: "Thriller",
            5: "Horror",
            6: "Sci-fi",
            7: "Chilren"}
    return switcher.get(genre)


start = True
qrated = True #start the first question which is movie age demographic 
movies.index = movies.index + 1

print("Welcome! Don't know what movie to watch at home? \nThis system will decide what movie to watch for you! \nBased on the movies inside the database. Let's start the first question!")
#start the system
while start == True:
    while qrated == True:
        age = int(input("Which age demographic do you belong to? Please enter 1,2 or 3 \n 1.Below 12 years old \n 2. Between 12 to 17 \n 3. 18 and above \n"))
        if age == 1:
            rated_movie = movies[movies.rated == 'UG']
            qdated = True
            qrated = False
        elif age == 2:
            rated_movie = movies[(movies.rated == 'UG') | (movies.rated == 'PG')]
            qdated = True
            qrated = False
        elif age == 3:
            rated_movie = movies
            qdated = True
            qrated = False
        else:
            print("You have entered an invalid number, please try again.")
    #question for movie timeline
    while qdated == True:
        d = int(input("Choose a preference on movie's release year by entering the number. \n1. Latest(current year) \n2. Recent(within the past 5 years) \n3. Old\n"))
        rated_movie.release = rated_movie.release.astype(int)
        if d == 1:
            rated_year_movie = rated_movie[(rated_movie.release == date.today().year)]
            qlanguage = True
            qdated = False
        elif d == 2:
            rated_year_movie = rated_movie[(rated_movie.release < date.today().year) & (rated_movie.release >= date.today().year - 5)]
            qlanguage = True
            qdated = False
        elif d == 3:
            rated_year_movie = rated_movie[(rated_movie.release < date.today().year - 5)]
            qlanguage = True
            qdated = False
        else:
            print("You have entered an invalid number, please try again.")
    #question for preferred language movie
    while qlanguage == True:
        l = int(input("Do you prefer to watch movies in English? Please enter the number. \n1. Yes, I prefer to watch in English. \n2. No, I am fine with any language.\n"))
        if l == 1:
            rated_year_language_movie = rated_year_movie[(rated_year_movie.language == 'English')]
            qgenre = True
            qlanguage = False
        elif l == 2:
            rated_year_language_movie = rated_year_movie
            qgenre = True
            qlanguage = False
        else:
            print("You have an entered an invalid number. Please try again.")
    #question for movie genre       
    while qgenre == True:
        choose = True
        g = []
        while choose == True:
            genre = int(input("If you wish to exit this phase enter 0. \nPlease choose the type of genres you wish to watch by typing its number. \n1. Action \n2. Comedy \n3. Crime \n4. Thriller \n5. Horror \n6. Sci-fi \n7. Children\n"))
            if genre > 0:
                sg = switchGenres(genre)
                if sg not in g:
                    g.append(sg)
            elif genre == 0:
                choose = False
                qratings = True
                qgenre = False
            else:
                print("You answer is invalid, please try again")
        #remove ',' inside the csv column to read as individual words
        rated_year_language_movie.genres = rated_year_language_movie.genres.str.split(',')
        #loop through the array to find the most genres found
        genre_rated_year_movie = rated_year_language_movie[rated_year_language_movie.genres.apply(lambda a: all(b in a for b in g))]
    #question on movie ratingss
    while qratings == True:
        rq = int(input("Does ratings of the movie matters to your preference? \nEnter the number 1 if 'Yes', Enter the number 2 if 'No' "))
        if rq == 1:
            if genre_rated_year_movie.empty:
                #get mean of ratings of the movies filtered
                altr = rated_year_language_movie.ratings.mean()
                #if there is more than one movie with the same mean then the movie with the highest ratings get chosen
                if len(rated_year_language_movie.index) > 1:
                    decision = rated_year_language_movie.loc[rated_year_language_movie.ratings.idxmax()]
                #if only one movie then choose it
                elif len(rated_year_language_movie.index) == 1:
                    decision = rated_year_language_movie
                else:
                #if none then get the highest rating movie from previous filter
                    decision = rated_movie.loc[rated_movie.ratings.idxmax()]
                qratings = False
            
            else:
                #get mean of current filter and get the highest rating movie
                r = genre_rated_year_movie.ratings.mean()
                ratings_genre_rated_year_movie = genre_rated_year_movie[genre_rated_year_movie.ratings >= r]
                if len(ratings_genre_rated_year_movie.index) > 1:
                    decision = ratings_genre_rated_year_movie.loc[ratings_genre_rated_year_movie.ratings.idxmax()]
                #get movie
                elif len(ratings_genre_rated_year_movie.index) == 1:
                    decision = ratings_genre_rated_year_movie
                qratings = False
            qratings = False
            start = False
        elif rq == 2:
            #if ratings did not matter and current filter is empty then get previous filter either one of the movie
            if genre_rated_year_movie.empty:
                decision = rated_movie.sample()
                qratings = False
            else:
            #if ratings did not matter and previous previous filter is empty then get previous filter either one of the movie
                decision = genre_rated_year_movie.sample()
            qratings = False
            start = False
        else:
            print("You have entered an invalid number please try again.")

print(decision,'is the movie recommended for you to watch.')   
