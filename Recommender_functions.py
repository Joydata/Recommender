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
    
    own_reviews_array=np.array(own_reviews)
    own_rated = own_reviews_array==own_reviews_array
    
    # Calculating user's reviews average ratings and max ratings : user_mean, user_max
    #user_mean=np.array(reviews.mean(axis=1,skipna=True)).reshape(n_users,1)
    user_mean=reviews.mean(axis=1,skipna=True)
    user_max=reviews.max(axis=1,skipna=True)
    
    #Filtering users having always the same rating
    bad_raters = (user_mean==user_max)[(user_mean==user_max)].index
    filtered_reviews = reviews[~reviews.index.isin(bad_raters)]

    #Useful variables
    n_movies = filtered_reviews.shape[1] 
    n_users = filtered_reviews.shape[0]
    own_mean=own_reviews.mean(axis=1,skipna=True)[0]

    # Recomputing user's reviews average ratings with the reduced dataset
    user_mean=np.array(filtered_reviews.mean(axis=1,skipna=True)).reshape(n_users,1)

    #Normalized review matrix (user_rating - user_mean)
    reviews_norm = filtered_reviews - (user_mean * np.ones((n_users,n_movies)))
    reviews_norm.fillna(0,inplace=True)
    A=np.array(reviews_norm)

    #Calculation of the Movies Cosine-similarity matrix
    sim_num = (np.transpose(A)).dot(A)
    sim_den = np.sqrt((A*A).sum(axis=0).reshape(n_movies,1)).dot(np.transpose(np.sqrt((A*A).sum(axis=0).reshape(n_movies,1))))
    similarity_matrix = np.divide(sim_num,sim_den)
    np.nan_to_num(similarity_matrix,copy=False)

    #My own Normalized ratings
    own_reviews_norm = np.nan_to_num(own_reviews - (own_mean * np.ones((1,n_movies))))
    # For movie j, the rating prediction will be SUM_i€S_(rating_movie_i*similarity(i,j)) /  SUM_i€S_(|similarity(i,j)|)
    # where S is the set of movies rated by me
    #SUM_i€S_(|similarity(i,j)|) = Sum_sim
    #SUM_i€S_(rating_movie_i*similarity(i,j)) = Sum_rat_sim

    Sum_sim = own_rated.dot(abs(similarity_matrix))
    Sum_rat_sim = own_reviews_norm.dot(similarity_matrix)
    Predictions = Sum_rat_sim / Sum_sim


    # If the movie was already rated, we don't want a prediction, therefore we will empty the predictions vector on columns 
    # of the movies already rated.
    Predictions = Predictions * (~own_rated)

    # Now we fill the prediction vector with the movies already rated and then we add own_mean to get the unnormalized ratings.
    Predictions=Predictions + own_reviews_norm + own_mean
    Predictions_df=pd.DataFrame(Predictions*~own_rated,columns=filtered_reviews.columns,index=['Preds']).transpose()

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
    own_rated = (own_reviews_array==own_reviews_array).transpose()
    Predictions = predict(reviews,own_reviews)
    Predictions_df=pd.DataFrame(Predictions*~own_rated)
    return(Predictions_df.sort_values(by='Preds',ascending=False)[:how_many])

def split(reviews,ratio):
    """Splits randomly a dataset into two, for model evaluation purpose.

    Parameters
    ----------
    reviews : pandas.DataFrame
        The DataFrame containing several user's ratings of some items.
        Must be of shape (n_users,n_items)
    ratio : float
        The ratio of the reviews from the parameter DataFrame to be included
        in the testing dataset

    Returns
    -------
    training_df : pandas.DataFrame
        The first returned DataFrame, of shape (n_users - int(ratio * n_users)),n_items)
    testing_df : pandas.DataFrame
        The second returned DataFrame, of shape (int(ratio * n_users),n_items)
    """
    
    n_users=len(reviews.index)
    test_size=int(n_users*ratio)
    train_set = random.sample(list(reviews.index),n_users-test_size)
    test_set = set(reviews.index) - set(train_set)
    training_df = reviews.loc[train_set,:]
    test_df = reviews.loc[test_set,:]
    return training_df, test_df

def evaluate(train_df,test_df):
    """Evaluates the accuracy of the predict function on a test dataset

    Parameters
    ----------
    train_df : pandas.DataFrame
        The training DataFrame containing several user's ratings of some items
        used to train the prediction model.
        Must be of shape (n_train_users,n_items)
    test_df : pandas.DataFrame
        The testing DataFrame containing several user's ratings of some items
        used to evaluate the predictions accuracy
        Must be of shape (n_test_users,n_items)

    Returns
    -------
    (mean_err, max_err, n_eval)
    mean_err : float
        The average absolute error between the predictions and the ratings contained in
        test_df
    max_err : float
        The maximum absolute error between the predictions and the ratings contained in
        test_df
    n_eval : int
        The total number of ratings contained in test_df on which the prediction error
        has been computed
    """
    
    n_eval=0
    err_acc=0
    max_err = 0
    
    for i in range(len(test_df.index)):

        print(i,' / ',len(test_df.index))
        test_reviews=test_df.iloc[i]
        rated_dramas = test_reviews[~test_reviews.isna()].index
        for drama in rated_dramas:
            test_reviews_for_evaluation = test_df.iloc[[i]].copy()
            test_reviews_for_evaluation[drama] = np.nan
            predictions = predict(train_df,test_reviews_for_evaluation).transpose()
            if predictions[drama][0]==predictions[drama][0]:
                n_eval+=1
                err = abs(predictions[drama][0]-test_reviews[drama])
                err_acc+=err
                if err > max_err:
                    max_err = err


    mean_err = err_acc / n_eval
    return mean_err, max_err, n_eval