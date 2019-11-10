# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 18:00:04 2019

@author: Lum Hui Yen
"""

import pandas as pd
from datetime import date

movies = pd.read_csv("E:\Documents\mov.csv", delimiter=',',
                     header=None,
                     names=['movieID','title','genres','release','ratings','rated'])

gen = ['Comedy','Action']
ge = movies[movies.genres.isin(gen)]



#mov = movies[movies.genres.str.contains('Comedy') & movies.genres.str.contains('Action')]
mov1 = movies[movies.genres.apply(lambda x: all(gg in x for gg in gen))]
#print(mov1)

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
qrated = True
qgenre = True
qdated = True
qratings = True
movies.index = movies.index + 1
while start == True:
    while qrated == True:
        age = int(input("Which age demographic do you belong to? Please enter 1,2 or 3 \n 1.Below 12 years old \n 2. Between 12 to 17 \n 3. 18 and above \n"))
        if age == 1:
            rated_movie = movies[movies.rated == 'UG']
            qrated = False
        elif age == 2:
            rated_movie = movies[(movies.rated == 'UG') | (movies.rated == 'PG')]
            qrated = False
        elif age == 3:
            rated_movie = movies
            qrated = False
        else:
            print("You have entered an invalid number, please try again.")
            
    while qdated == True:
        d = int(input("Choose a preference on movie's release year by entering the number. \n1. Latest(current year) \n2. Recent(within the past 5 years) \n3. Old\n"))
        rated_movie.release = rated_movie.release.astype(int)
        if d == 1:
            rated_year_movie = rated_movie[(movies.release == date.today().year)]
            qdated = False
        elif d == 2:
            rated_year_movie = rated_movie[(movies.release < date.today().year) & (movies.release >= date.today().year - 5)]
            qdated = False
        elif d == 3:
            rated_year_movie = rated_movie[(movies.release < date.today().year - 5)]
            qdated = False
        else:
            print("You have entered an invalid number, please try again.")
            
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
                qgenre = False
            else:
                print("You answer is invalid, please try again")
        rated_year_movie.genres = rated_year_movie.genres.str.split(',')
        genre_rated_year_movie = rated_year_movie[rated_year_movie.genres.apply(lambda a: all(b in a for b in g))]
    
    while qratings == True:
        print(genre_rated_year_movie,'a')
        
        if genre_rated_year_movie.empty:
            altr = rated_year_movie.ratings.mean()
            if len(rated_year_movie.index) > 1:
                decision = rated_year_movie.loc[rated_year_movie.ratings.idxmax()]
            elif len(rated_year_movie.index) == 1:
                decision = rated_year_movie
            else:
                decision = rated_movie.loc[rated_movie.ratings.idxmax()]
            print("We could not find a movie that suits most of your preference so this is one that we would recommend ")
            qratings = False
            break
        
        r = genre_rated_year_movie.ratings.mean()
        ratings_genre_rated_year_movie = genre_rated_year_movie[genre_rated_year_movie.ratings >= r]
        if len(ratings_genre_rated_year_movie.index) > 1:
            decision = ratings_genre_rated_year_movie.loc[ratings_genre_rated_year_movie.ratings.idxmax()]
        elif len(ratings_genre_rated_year_movie.index) == 1:
            decision = ratings_genre_rated_year_movie
        else:
            decision = rated_year_movie.loc[genre_rated_year_movie.ratings.idxmax()]
            print("We could not find a movie that suits most of your preference so this is one that we would recommend ")
        qratings = False
    break

print(decision)   
