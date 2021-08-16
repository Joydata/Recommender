import pandas as pd
import numpy as np
import random

def predict(reviews,own_reviews):
    """Predicts a key-user ratings of items by cosine similarity method.

    Parameters
    ----------
    reviews : pandas.DataFrame
        The DataFrame containing several user's ratings of some items.
        Must be of shape (n_users,n_items)
    own_reviews : pandas.DataFrame
        The DataFrame containing the key user's ratings of some items.
        Must be of shape (1,n_items)

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing the key user's ratings predictions of all the items.
        Shape (n_items,1)
        Items already rated by the key user in own_reviews parameter are not predicted
        but kept from the original DataFrame.
    """
    
    own_reviews_array = np.array(own_reviews)
    own_rated = own_reviews_array == own_reviews_array # Boolean array with TRUE for rated movies in own_reviews
    
    # Calculating user's reviews average ratings and max ratings : user_mean, user_max
    user_mean = reviews.mean(axis=1,skipna=True)
    user_max = reviews.max(axis=1,skipna=True)
    
    # Filtering users having always the same rating
    bad_raters = (user_mean==user_max)[(user_mean==user_max)].index
    filtered_reviews = reviews[~reviews.index.isin(bad_raters)]

    #Useful variables
    n_movies = filtered_reviews.shape[1] 
    n_users = filtered_reviews.shape[0]
    own_mean = own_reviews.mean(axis=1,skipna=True)[0]

    # Recomputing user's reviews average ratings with the reduced dataset
    user_mean = np.array(filtered_reviews.mean(axis=1,skipna=True)).reshape(n_users,1)

    # Computing normalized review matrix (user_rating - user_mean)
    reviews_norm = filtered_reviews - (user_mean * np.ones((n_users,n_movies)))
    reviews_norm.fillna(0,inplace = True)
    A = np.array(reviews_norm)

    #Calculating the Movies Cosine-similarity matrix
    sim_num = (np.transpose(A)).dot(A)
    sim_den = np.sqrt((A*A).sum(axis=0).reshape(n_movies,1)).dot(np.transpose(np.sqrt((A*A).sum(axis=0).reshape(n_movies,1))))
    similarity_matrix = np.divide(sim_num,sim_den)
    np.nan_to_num(similarity_matrix, copy=False)

    #Computing own Normalized ratings
    own_reviews_norm = np.nan_to_num(own_reviews - (own_mean * np.ones((1,n_movies))))
    
    # For movie j, the rating prediction will be SUM_i€S_(rating_movie_i*similarity(i,j)) /  SUM_i€S_(|similarity(i,j)|)
    # where S is the set of movies rated by me
    # SUM_i€S_(|similarity(i,j)|) = Sum_sim
    # SUM_i€S_(rating_movie_i*similarity(i,j)) = Sum_rat_sim
    Sum_sim = own_rated.dot(abs(similarity_matrix))
    Sum_rat_sim = own_reviews_norm.dot(similarity_matrix)
    Predictions = Sum_rat_sim / Sum_sim

    # If the movie was already rated, we don't want a prediction, therefore we will empty the predictions vector on columns 
    # of the movies already rated.
    Predictions = Predictions * (~own_rated)

    # Filling the prediction vector with the movies already rated and adding own_mean to get the unnormalized ratings.
    Predictions = Predictions + own_reviews_norm + own_mean
    
    # Adding the predictions in a dataset to be returned
    Predictions_df = pd.DataFrame(Predictions,columns=filtered_reviews.columns,index=['Predictions']).transpose()
    return Predictions_df

def recommend(reviews,own_reviews,how_many):
    """Recommends a few items based on the predicted ratings of the key-user

    Parameters
    ----------
    reviews : pandas.DataFrame
        The DataFrame containing several user's ratings of some items.
        Must be of shape (n_users,n_items)
    own_reviews : pandas.DataFrame
        The DataFrame containing the key user's ratings of some items.
        Must be of shape (1,n_items)
    how_many : int
        The number of items to be recommended.

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing the recommendations with their associated rating predictions.
        Shape (how_many,2)
    """
    own_reviews_array=np.array(own_reviews)
    own_rated = (own_reviews_array == own_reviews_array).transpose() # Boolean array with TRUE for rated movies in own_reviews.
    Predictions = predict(reviews, own_reviews)
    Predictions_df = pd.DataFrame(Predictions * ~own_rated) # Predictions with a 0 for movies already rated.
    return(round(Predictions_df.sort_values(by='Predictions',ascending=False)[:how_many],2))

def split(reviews,ratio):
    """Splits randomly a dataset into two, for model evaluation purpose.

    Parameters
    ----------
    reviews : pandas.DataFrame
        The DataFrame containing several user's ratings of some items.
        Must be of shape (n_users,n_items)
    ratio : float
        The ratio of the reviews from the parameter DataFrame to be included
        in the evaluation dataset

    Returns
    -------
    training_df : pandas.DataFrame
        The first returned DataFrame, of shape (n_users - int(ratio * n_users)),n_items)
    eval_df : pandas.DataFrame
        The second returned DataFrame, of shape (int(ratio * n_users),n_items)
    """
    
    n_users = len(reviews.index) # Total number of users in reviews Dataframe.
    eval_size = int(n_users * ratio) # Number of users assigned to the evaluation Dataframe. 

    # Building the 2 datasets
    train_set = random.sample(list(reviews.index), n_users - eval_size)
    test_set = set(reviews.index) - set(train_set)
    training_df = reviews.loc[train_set,:]
    eval_df = reviews.loc[test_set,:]
    
    return training_df, eval_df

def evaluate(train_df,eval_df):
    """Evaluates the accuracy of the predict function on a test dataset

    Parameters
    ----------
    train_df : pandas.DataFrame
        The training DataFrame containing several user's ratings of some items
        used to train the prediction model.
        Must be of shape (n_train_users,n_items).
    eval_df : pandas.DataFrame
        The evaluation DataFrame containing several user's ratings of some items
        used to evaluate the predictions accuracy.
        Must be of shape (n_test_users,n_items).

    Returns
    -------
    (mean_err, max_err, n_eval, max_rating)
    mean_err : float
        The average absolute error between the predictions and the ratings contained in
        eval_df
    n_eval : int
        The total number of ratings contained in eval_df on which the prediction error
        has been computed
    max_rating : int
        Higher rating in the dataframe.
    """
    # Initializing the variables.
    n_eval = 0 # Number of evaluations performed.
    err_acc = 0 # Accumulator for the prediction absolute error.
    max_rating = max(train_df.max(axis=1)) # Higher rating in the dataframe.
    
    for i in range(len(eval_df.index)): # Loop over the users in the evaluation dataframe.

        print(f'evaluating model on user {i+1} / {len(eval_df.index)+1}')
        test_reviews = eval_df.iloc[i]
        rated_movies = test_reviews[~test_reviews.isna()].index # indexes of the movies rated by this user.
        for movie in rated_movies: # Loop over the movies rated.
            # Temporally replacing the movie rating by NAN.
            test_reviews_for_evaluation = eval_df.iloc[[i]].copy()
            test_reviews_for_evaluation[movie] = np.nan

            # Predicting the ratings for this user
            predictions = predict(train_df,test_reviews_for_evaluation).transpose()
            
            if predictions[movie][0]==predictions[movie][0]: # If the movie was rated
                n_eval += 1
                err = abs(predictions[movie][0] - test_reviews[movie])
                err_acc += err

    mean_err = err_acc / n_eval
    return mean_err, n_eval, max_rating
