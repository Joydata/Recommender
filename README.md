# Recommender
Python project - Recommender system

# Quick run
## Project setup
```
git clone https://github.com/Joydata/Recommender.git
pip3 install -r requirements.txt
```
## To make some recommendations using the example datasets :

1. (optionnal) If you want recommendations based on your own preferences, first remove my ratings and put a few of your owns in one of the following csvs :
- *Example_datasets/imdb_my-reviews.csv* for movie recommendations.
- *Example_datasets/mydramalist_mywife-reviews.csv* for dramas recommendations.  
  
Ratings are between 1 for the items you hate and 10 for your preferred ones.

2.  
```python recommend.py Example_datasets/imdb_light_dataset.csv Example_datasets/imdb_my-reviews.csv``` if, as me, you like movies.

```python recommend.py Example_datasets/mydramalist_light_dataset.csv Example_datasets/mydramalist_mywife-reviews.csv``` if, as my wife, you also like dramas !

- 1st argument : path to the ratings database.
- 2nd argument : path to the ratings of the user that wants some new recommendations.
- 3rd argument (optionnal) : the number of items to recommend.

## To launch an evaluation of the model
```python evaluate.py Example_datasets/mydramalist_light_dataset.csv```

- argument : path to the ratings database.

# More information about the project

## Databases
2 Databases are available to train the recommendation model :
- A Movie ratings database using the ratings shared by users on imdb website.
- A Drama ratings database using the ratings shared by users on mydramalist website.  
The *Scrappers* subdirectory contains all the code to build these databases and a light version of them.

## Recommender
The recommender model is using the cosine similarity method to calculate rating predictions on the items that have not been rated by the end user.
For more information about this method :
[https://realpython.com/build-recommendation-engine-collaborative-filtering/#memory-based](https://realpython.com/build-recommendation-engine-collaborative-filtering/#memory-based)
