from Recommender_functions import recommend
import sys
import pandas as pd


if __name__ == "__main__":
    reviews_arg = pd.read_csv(sys.argv[1], sep = ',', index_col = 0)
    own_reviews_arg = pd.read_csv(sys.argv[2], sep = ',', index_col = 0)
    try:
        how_many_arg = int(sys.argv[3])
    except:
        how_many_arg = 5
    
    recommendations = recommend(reviews_arg, own_reviews_arg,how_many_arg)

    print(recommendations)

