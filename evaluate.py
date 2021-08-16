from Recommender_functions import evaluate, split
import sys
import pandas as pd
import warnings

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    
    # Reading the user input arguments
    reviews_arg = pd.read_csv(sys.argv[1], sep = ',', index_col = 0)
    try:
        ratio_arg = float(sys.argv[2])
    except:
        ratio_arg = 0.01
    
    # Splitting the dataframe for evaluation
    train_df_arg, eval_df_arg = split(reviews_arg, ratio_arg)

    #Evaluating the model
    mean_err, n_eval, max_rating = evaluate(train_df_arg, eval_df_arg)

    print(f'Model evaluated on {n_eval} predictions. \n mean absolute error : {round(mean_err,2)} / {max_rating}')
