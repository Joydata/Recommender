from urllib.request import Request, urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import pandas as pd
import time
import re


#--------------------------------------------------------------------------------------------------------------------------------
#Get the list of movie reference numbers from imdb------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------

#Function to get the drama home pages from an url with a list of dramas
def getRef(url):
    result = []
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()

    try:
        soup = BeautifulSoup(html, 'html.parser')
        for drama in soup.find_all(class_='text-primary title'):
            ref = drama.a.attrs['href']
            result.append(ref)

    except AttributeError as e:
        return None
    return set(result)

#Function to Loop over all the pages of the dramas in the popular list (pages go from 1 to 250) and collect the drama reference tags

def tags_popular():
    result=set()
    url_dramalist = 'https://mydramalist.com/shows/popular?page='
    for i in range(1,251):
        dramas = getRef(url_dramalist+str(i))
        result = result.union(dramas)
    return result

result = tags_popular()

#Store the drama reference tags in a csv for later use
drama_tags_list = list(result)
df = pd.DataFrame(data={'drama_tags_list': drama_tags_list})
df.to_csv("drama_tags_list.csv", sep=',',index=False)



#Function to get the number of review pages for a given drama, based on its reference tag

def get_nb_of_review_pages(drama_tag):
    #url of the reviews
    url = 'https://mydramalist.com/' + str(drama_tag) + '/reviews?page='
    
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()

    try:
        soup = BeautifulSoup(html, 'html.parser')
    
    except AttributeError as e:
        print("get_nb_of_review_pages function didn't work for url ",url)
        return None
    
    if soup.find(class_='page-item last')!=None:
        href = soup.find(class_='page-item last').a['href']
        index=href.find('page=')
        return int(href[index+5:])
    else:
        nb=0
        for element in soup.find_all(class_='page-item'):
            if len(element['class'])==1:
                temp_nb=int(element.a['href'][-1])
                if temp_nb > nb:
                    nb=temp_nb
        return nb

#--------------------------------------------------------------------------------------------------------------------------------
#Function to get the reviews of a given drama, based on its reference tag--------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
drama_tag=drama_tags_list[2]
    
def getReviews(drama_tag):
    reviews = {'user':[],'note':[]}
    #url of the reviews
    url = 'https://mydramalist.com/' + str(drama_tag) + '/reviews?page='
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()
    nb_pages = get_nb_of_review_pages(drama_tag)
    #Get the drama title
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find(class_='film-title').a.text
    
    for i in range(1,nb_pages+1):
        req = Request(url+str(i), headers={'User-Agent': 'Mozilla/5.0'})
        html = urlopen(req).read()

        soup = BeautifulSoup(html, 'html.parser')
        
        for review in soup.find_all(class_='review'):
            if review.find(class_='score pull-right') !=None:
                name = review.find(class_='text-primary').text
                note = review.find(class_='score pull-right').text
                reviews['user'].append(name)
                reviews['note'].append(note)

    print('reviews added for the drama :')
    print(title)
    #Return a DataFrame with the reviews
    return pd.DataFrame(reviews['note'],index=reviews['user'],columns=[title])




#--------------------------------------------------------------------------------------------------------------------------------
#Function to create the database of reviews from a csv file containing movie tags------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------

def dramaReviews(drama_tags_list_file,start_idx,stop_idx):
    drama_reviews_df = pd.DataFrame({})
    drama_df = pd.read_csv(drama_tags_list_file, sep=',')
    drama_tags_list = drama_df['drama_tags_list'].values.tolist()
    if start_idx >= len(drama_tags_list):
        print('Error : The source file last index is ',len(drama_tags_list)-1)
        print('Execution not started')
    else:
        if stop_idx > len(drama_tags_list):
            print('Warning : The source file last index is ',len(drama_tags_list)-1)
            print('stop_index modified to ',len(drama_tags_list))
            stop_idx = len(drama_tags_list)
        for i in range(start_idx,stop_idx):
            print('getting reviews of drama no ',i+1,' / ',len(drama_tags_list),' from the file ',drama_tags_list_file,'...')
            temp_df = getReviews(drama_tags_list[i])
            drama_reviews_df = drama_reviews_df.merge(temp_df,how='outer',left_index=True,right_index=True)
        return(drama_reviews_df)

drama_tags_list_file = 'drama_tags_list.csv'
start_idx = 0
stop_idx = 5
result=dramaReviews('drama_tags_list.csv',0,5000)

result.to_csv('drama_reviews.csv')