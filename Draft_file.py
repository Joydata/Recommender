from math import isnan
import pandas as pd
import numpy as np

reviews=pd.read_csv('imdb datasets/reviews_light.csv',sep=',',index_col=0)
reviews_array = np.array(reviews)


#Useful variables
n_movies = reviews.shape[1] 
n_users = reviews.shape[0]

#Useful indexes
movies_idx = reviews.columns 
users_idx = reviews.index

#Cosine similarity between movies
#https://learning.oreilly.com/library/view/practical-recommender-systems/9781617292705/kindle_split_018.html

# Calculating user's average rating : user_mean
user_mean=np.array(reviews.mean(axis=1,skipna=True)).reshape(n_users,1)

#Normalized review matrix (user_rating - user_mean)
reviews_norm = reviews - (user_mean * np.ones((n_users,n_movies)))
reviews_norm.fillna(0,inplace=True)
A=np.array(reviews_norm)

#Calculation of the Movies Cosine-similarity matrix

sim_num = (np.transpose(A)).dot(A)
sim_den = np.sqrt((A*A).sum(axis=0).reshape(n_movies,1)).dot(np.transpose(np.sqrt((A*A).sum(axis=0).reshape(n_movies,1))))
similarity_matrix = np.divide(sim_num,sim_den)
pd.DataFrame(similarity_matrix)

#What is the max similarity between different movies ?
(similarity_matrix-np.eye(n_movies)).max()
#0.59 

#Let's see what are the movies that have more than 0.35 cosine similarity to test the calculation
for i in range(n_movies):
    j=0
    while j<i:
        if similarity_matrix[i,j] > 0.4:
            print(reviews.columns[i],' / ',reviews.columns[j],'-->',similarity_matrix[i,j])
        j +=1

#Gully Boy  /  OMG: Oh My God! --> 0.4502837979921495
#Airlift  /  OMG: Oh My God! --> 0.5202753744614524
#Barfi!  /  OMG: Oh My God! --> 0.5949185829206567
#Barfi!  /  Airlift --> 0.5316172207519916
#Le Seigneur des anneaux : La Communauté de l'anneau  /  Le Seigneur des anneaux : Les Deux Tours --> 0.44828877425077673
#Veer-Zaara  /  Bhaag Milkha Bhaag --> 0.4084653690395161
#Le Seigneur des anneaux : Le Retour du roi  /  Le Seigneur des anneaux : Les Deux Tours --> 0.4680401872656044
#Trois couleurs: Bleu  /  Trois couleurs: Rouge --> 0.41553132664574016
# Seems to make sense :)


#Let's recommend some movies using this cosine similarity method

#import dataframe with my own reviews for a few movies and normalize it
own_reviews=pd.read_csv('own_reviews2.csv',sep=',',index_col=0)
own_reviews_array=np.array(own_reviews)

#Boolean vector with TRUE for the movies I rated:
own_rated = own_reviews_array==own_reviews_array

# Usefull variables : count and mean of the movies I rated 
n_rated = own_rated.sum()
own_mean=own_reviews.mean(axis=1,skipna=True)[0]
n_rated
own_mean
#My own Normalized ratings
own_reviews_norm = np.nan_to_num(own_reviews - (own_mean * np.ones((1,n_movies))))
# For movie j, the rating prediction will be SUM_i€S_(rating_movie_i*similarity(i,j)) /  SUM_i€S_(|similarity(i,j)|)
# where S is the set of movies rated by me
#SUM_i€S_(|similarity(i,j)|) = Sum_sim
#SUM_i€S_(rating_movie_i*similarity(i,j)) = Sum_rat_sim

Sum_sim = own_rated.dot(abs(similarity_matrix))
Sum_rat_sim = own_reviews_norm.dot(similarity_matrix)
Predictions = Sum_rat_sim / Sum_sim

i=1
Sum_rat_sim[0][i]
Sum_sim[0][i]
Predictions[0][i]


# If the movie was already rated, we don't want a prediction, therefore we will empty the predictions vector on columns 
# of the movies already rated.
Predictions = Predictions * (~own_rated)

# Now we fill the prediction vector with the movies already rated and then we add own_mean to get the unnormalized ratings.
Predictions=Predictions + own_reviews_norm + own_mean

Predictions.max()
Predictions.min()
Predictions.mean()
def recommend(how_many):
    Predictions_df=pd.DataFrame(Predictions*~own_rated,columns=reviews.columns,index=['Preds']).transpose()
    return(Predictions_df.sort_values(by='Preds',ascending=False)[:how_many])

recommend(20)



for i in range(n_movies):
    if own_rated[0][i] == False and Predictions[0][i] < 7:
        print(reviews.columns[i],'-->',Predictions[0][i])






##############################
itemID_to_title = {}
title_to_itemID = {}
for i in range(len(reviews.columns)):
    itemID_to_title[i]=reviews.columns[i]
    title_to_itemID[reviews.columns[i]]=i


def matrix_to_dataframe(reviews_matrix):
    dataset_dict={'itemID':[],'rating':[],'userID':[]}
    for user in reviews_matrix.index:
        ratings=reviews_matrix.loc[user][reviews_matrix.loc[user]==reviews_matrix.loc[user]]
        for i in range(len(ratings.index)):
            itemID=title_to_itemID[ratings.index[i]]
            rating=ratings[i]
            dataset_dict['itemID'].append(itemID)
            dataset_dict['rating'].append(rating)
            dataset_dict['userID'].append(user)
    return dataset_dict



dataset_dict = matrix_to_dataframe(reviews)
dataset=pd.DataFrame(dataset_dict)
dataset.to_csv('dataset.csv')

#Function to feed my own reviews
own_reviews2 = pd.DataFrame(columns=reviews.columns,index=['Johann'])
own_reviews2

def add_note(df):
    import random
    movie_list=list(df.columns)
    movie = movie_list.pop(random.randint(0,len(movie_list)-1))
    while df[movie][0] == df[movie][0]: #check if not NaN
        movie = movie_list.pop(random.randint(0,len(movie_list)-1))
    note = 0
    while note == 0:
        note = int(input('What is your Note for movie '+ movie + " (1-10, 0 if you didn't see it) ?"))
        if note == 0:
            movie = movie_list.pop(random.randint(0,len(movie_list)-1))
            while df[movie][0] == df[movie][0]: #check if not NaN
                movie = movie_list.pop(random.randint(0,len(movie_list)-1))
        else:
            df[movie][0] = note
    return df

def fill_reviews(df,target):
    while df.count(axis=1)[0] < target:
        df = add_note(df)

fill_reviews(own_reviews,76)

print(own_reviews.count(axis=1)[0])
print(own_reviews.head())

own_reviews.to_csv('own_reviews2.csv')

#Normalisation matrices
movie_mean=reviews.mean(axis=0,skipna=True)
user_mean=reviews.mean(axis=1,skipna=True)
user_mean
Norm=reviews.copy()

for i in range(len(user_mean)):
    if i%100 == 0:
        print(i)
    for j in range(len(movie_mean)):
        if Norm.iloc[i,j] == Norm.iloc[i,j]:
            Norm.iloc[i,j] = -0.5*(user_mean[i]+movie_mean[j])

Norm

normalized_reviews = reviews + Norm
normalized_reviews

#######

own_reviews=pd.read_csv('own_reviews.csv',sep=',',index_col='Unnamed: 0')
own_reviews_dataset_dict=matrix_to_dataframe(own_reviews)
own_reviews_dataset=pd.DataFrame(own_reviews_dataset_dict)

full_reviews=pd.concat([dataset,own_reviews_dataset])
full_reviews.to_csv('full_reviews.csv')


dataset=pd.read_csv('full_reviews.csv',sep=',',index_col='Unnamed: 0')


