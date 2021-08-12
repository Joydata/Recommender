import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.request import urlopen
from selenium.webdriver.chrome.options import Options
import time
import re

executable_path = 'C:/Users/johan/Software/chromedriver_win32/chromedriver.exe'

def imdb_getTags(url):
    """Get the movie reference tags from an imdb page with a list of movies

    Parameters
    ----------
    url : string
        The imdb url containing the list of movies to parse

    Returns
    -------
    A set containing the movies reference tags
    """
    result = []
    try:
        html = urlopen(url)
    except :
        print(f'url {url} not found')
        return None
    
    try:
        soup = BeautifulSoup(html.read(), 'html.parser')
        for movie in soup.find(id='main').find_all(href=re.compile('^(/title/tt)')):
            tag = movie.attrs['href'][7:16]
            result.append(tag)
    except AttributeError as e:
        return None

    return set(result)

def imdb_consolidate_tags(url_dict, file_name):
    """Consolidate the list of the movie reference tags from a collection of imdb pages with list of movies
    and store it in a csv file.

    Parameters
    ----------
    url_dict : dict of str: str
        A dicionnary with the urls of the pages to parse as values

    Returns
    -------
    A list containing the unique movie reference tags
    """
    final_set = set()
    # Loop over all the pages to collect the movie reference tags
    for page in url_dict.values():
        temp_set = imdb_getTags(page)
        final_set = final_set.union(temp_set)

    # Store the movie tags in the file
    movie_tags_list = list(final_set)
    df = pd.DataFrame(data={'movie_tags_list': movie_tags_list})
    df.to_csv(file_name, sep=',',index=False)

def imdb_getReviews(movie_tag,executable_path):
    """get the imdb reviews of a given movie, based on its reference tag.

    Parameters
    ----------
    movie_tag : string
        The imdb refererence tag of the movie
    executable_path : string
        The path to the chromedriver executable file
    Returns
    -------
    A pandas.Dataframe with the user_names and notes of users who rated the movie
    """

    #url of the reviews
    url = 'https://www.imdb.com/title/' + str(movie_tag) + '/reviews?ref_=tt_urv'
    
    #configure chromedriver options
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument("--log-level=OFF")


    #Open the url with chromedriver
    driver = webdriver.Chrome(executable_path=executable_path,options=chrome_options)
    driver.get(url)

    #Load the full content with all the reviews
    while True:
        try:
            loadMoreButton = driver.find_element_by_xpath("//button[@id='load-more-trigger']")
            loadMoreButton.click()
            time.sleep(2)
        except Exception as e:
            print (e)
            break
    
    #Cook the beautifulsoup
    pageSource = driver.page_source
    soup = BeautifulSoup(pageSource, 'html.parser')

    #Get the movie title
    title = soup.find('h3').a.text
    
    #Get the review notes of the users and store them in a dictionnary
    reviews = {'user':[],title:[]}
    
    for review in soup.find_all(class_='lister-item-content'):
        if review.find(class_='ipl-ratings-bar') != None:
            name = review.find(class_='display-name-link').text
            note = review.find(class_='rating-other-user-rating').span.text
            reviews['user'].append(name)
            reviews[title].append(note)
    print('reviews added for the movie :')
    print(title)
    #close the chromedriver
    driver.close()

    #Return a DataFrame with the reviews
    return pd.DataFrame(reviews)

def imdb_createDB(movie_tags_list_file,start_idx,stop_idx):
    """create the database of reviews from a csv file containing movie tags

    Parameters
    ----------
    movie_tags_list_file : string
        The path to the csv file containing the movie tags
    start_idx : int
        index of the first movie tag to use
    stop_idx : int
        index of the last movie tag to use

    Returns
    -------
    A pandas.Dataframe with the user_names and notes of users for the movies beween
    start_idx and stop_idx of the movie_tags_list_file
    """

    #Initiate the result dataframe
    imdb_reviews_df = pd.DataFrame({'user':[]})

    #read the input dataframe
    movie_df = pd.read_csv(movie_tags_list_file, sep=',')
    movie_tags_list = movie_df['movie_tags_list'].values.tolist()

    if start_idx >= len(movie_tags_list):
        print('Error : The source file last index is ',len(movie_tags_list)-1)
        print('Execution not started')
    else:
        if stop_idx > len(movie_tags_list):
            print('Warning : The source file last index is ',len(movie_tags_list)-1)
            print('stop_index modified to ',len(movie_tags_list))
            stop_idx = len(movie_tags_list)
        # loop over the movies
        for i in range(start_idx,stop_idx):
            print('getting reviews of movie no ',i+1,' / ',len(movie_tags_list),' from the file ',movie_tags_list_file,'...')
            # Call imdb_getReviews() to get all the reviews of this movie
            temp_df = imdb_getReviews(movie_tags_list[i],executable_path)
            # Add the reviews to the final dataframe
            imdb_reviews_df = imdb_reviews_df.merge(temp_df,on='user',how='outer')
        return(imdb_reviews_df)
