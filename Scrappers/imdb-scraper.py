from Scrappers.scrap_functions import *
from multiprocessing import Pool

# Creation of a dictionnary with interessant movie lists to be included in database
movies_url_dict={}
movies_url_dict['toprated'] = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'
movies_url_dict['toppopular'] = 'https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm'
movies_url_dict['topaction'] = 'https://www.imdb.com/search/title/?genres=action&sort=user_rating,desc&title_type=feature&num_votes=25000,&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=5aab685f-35eb-40f3-95f7-c53f09d542c3&pf_rd_r=644GYS39TBNX6RJC1PKH&pf_rd_s=right-6&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_gnr_1'
movies_url_dict['topadventure'] = 'https://www.imdb.com/search/title/?genres=adventure&sort=user_rating,desc&title_type=feature&num_votes=25000,&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=5aab685f-35eb-40f3-95f7-c53f09d542c3&pf_rd_r=644GYS39TBNX6RJC1PKH&pf_rd_s=right-6&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_gnr_2'
movies_url_dict['topanim'] = 'https://www.imdb.com/search/title/?genres=animation&sort=user_rating,desc&title_type=feature&num_votes=25000,&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=5aab685f-35eb-40f3-95f7-c53f09d542c3&pf_rd_r=644GYS39TBNX6RJC1PKH&pf_rd_s=right-6&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_gnr_3'
movies_url_dict['topbio'] = 'https://www.imdb.com/search/title/?genres=biography&sort=user_rating,desc&title_type=feature&num_votes=25000,&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=5aab685f-35eb-40f3-95f7-c53f09d542c3&pf_rd_r=3294KP3ZSZP484T54N8T&pf_rd_s=right-6&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_gnr_4'
movies_url_dict['topcomedy'] = 'https://www.imdb.com/search/title/?genres=comedy&sort=user_rating,desc&title_type=feature&num_votes=25000,&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=5aab685f-35eb-40f3-95f7-c53f09d542c3&pf_rd_r=3294KP3ZSZP484T54N8T&pf_rd_s=right-6&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_gnr_5'
movies_url_dict['topcrime'] = 'https://www.imdb.com/search/title/?genres=crime&sort=user_rating,desc&title_type=feature&num_votes=25000,&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=5aab685f-35eb-40f3-95f7-c53f09d542c3&pf_rd_r=3294KP3ZSZP484T54N8T&pf_rd_s=right-6&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_gnr_6'
movies_url_dict['topdrama'] = 'https://www.imdb.com/search/title/?genres=drama&sort=user_rating,desc&title_type=feature&num_votes=25000,&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=5aab685f-35eb-40f3-95f7-c53f09d542c3&pf_rd_r=3294KP3ZSZP484T54N8T&pf_rd_s=right-6&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_gnr_7'
movies_url_dict['topfamily'] = 'https://www.imdb.com/search/title/?genres=family&sort=user_rating,desc&title_type=feature&num_votes=25000,&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=5aab685f-35eb-40f3-95f7-c53f09d542c3&pf_rd_r=3294KP3ZSZP484T54N8T&pf_rd_s=right-6&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_gnr_8'
movies_url_dict['topfantasy'] = 'https://www.imdb.com/search/title/?genres=fantasy&sort=user_rating,desc&title_type=feature&num_votes=25000,&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=5aab685f-35eb-40f3-95f7-c53f09d542c3&pf_rd_r=3294KP3ZSZP484T54N8T&pf_rd_s=right-6&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_gnr_9'
movies_url_dict['topblack'] = 'https://www.imdb.com/search/title/?genres=film_noir&sort=user_rating,desc&title_type=feature&num_votes=25000,&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=5aab685f-35eb-40f3-95f7-c53f09d542c3&pf_rd_r=3294KP3ZSZP484T54N8T&pf_rd_s=right-6&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_gnr_10'
movies_url_dict['tophistory'] = 'https://www.imdb.com/search/title/?genres=history&sort=user_rating,desc&title_type=feature&num_votes=25000,&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=5aab685f-35eb-40f3-95f7-c53f09d542c3&pf_rd_r=3294KP3ZSZP484T54N8T&pf_rd_s=right-6&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_gnr_11'
movies_url_dict['tophorror'] = 'https://www.imdb.com/search/title/?genres=horror&sort=user_rating,desc&title_type=feature&num_votes=25000,&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=5aab685f-35eb-40f3-95f7-c53f09d542c3&pf_rd_r=3294KP3ZSZP484T54N8T&pf_rd_s=right-6&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_gnr_12'
movies_url_dict['topmusic'] = 'https://www.imdb.com/search/title/?genres=music&sort=user_rating,desc&title_type=feature&num_votes=25000,&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=5aab685f-35eb-40f3-95f7-c53f09d542c3&pf_rd_r=3294KP3ZSZP484T54N8T&pf_rd_s=right-6&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_gnr_13'
movies_url_dict['topmusical'] = 'https://www.imdb.com/search/title/?genres=musical&sort=user_rating,desc&title_type=feature&num_votes=25000,&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=5aab685f-35eb-40f3-95f7-c53f09d542c3&pf_rd_r=3294KP3ZSZP484T54N8T&pf_rd_s=right-6&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_gnr_14'
movies_url_dict['topmystery'] = 'https://www.imdb.com/search/title/?genres=mystery&sort=user_rating,desc&title_type=feature&num_votes=25000,&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=5aab685f-35eb-40f3-95f7-c53f09d542c3&pf_rd_r=3294KP3ZSZP484T54N8T&pf_rd_s=right-6&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_gnr_15'
movies_url_dict['topromancel'] = 'https://www.imdb.com/search/title/?genres=romance&sort=user_rating,desc&title_type=feature&num_votes=25000,&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=5aab685f-35eb-40f3-95f7-c53f09d542c3&pf_rd_r=3294KP3ZSZP484T54N8T&pf_rd_s=right-6&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_gnr_16'
movies_url_dict['topsf'] = 'https://www.imdb.com/search/title/?genres=sci_fi&sort=user_rating,desc&title_type=feature&num_votes=25000,&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=5aab685f-35eb-40f3-95f7-c53f09d542c3&pf_rd_r=3294KP3ZSZP484T54N8T&pf_rd_s=right-6&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_gnr_17'
movies_url_dict['topsport'] = 'https://www.imdb.com/search/title/?genres=sport&sort=user_rating,desc&title_type=feature&num_votes=25000,&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=5aab685f-35eb-40f3-95f7-c53f09d542c3&pf_rd_r=3294KP3ZSZP484T54N8T&pf_rd_s=right-6&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_gnr_18'
movies_url_dict['topthriller'] = 'https://www.imdb.com/search/title/?genres=thriller&sort=user_rating,desc&title_type=feature&num_votes=25000,&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=5aab685f-35eb-40f3-95f7-c53f09d542c3&pf_rd_r=3294KP3ZSZP484T54N8T&pf_rd_s=right-6&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_gnr_19'
movies_url_dict['topwar'] = 'https://www.imdb.com/search/title/?genres=war&sort=user_rating,desc&title_type=feature&num_votes=25000,&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=5aab685f-35eb-40f3-95f7-c53f09d542c3&pf_rd_r=3294KP3ZSZP484T54N8T&pf_rd_s=right-6&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_gnr_20'
movies_url_dict['topwestern'] = 'https://www.imdb.com/search/title/?genres=western&sort=user_rating,desc&title_type=feature&num_votes=25000,&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=5aab685f-35eb-40f3-95f7-c53f09d542c3&pf_rd_r=3294KP3ZSZP484T54N8T&pf_rd_s=right-6&pf_rd_t=15506&pf_rd_i=top&ref_=chttp_gnr_21'

# Get the imdb tags of all the movies on these pages and store them in a local csv
imdb_consolidate_tags(movies_url_dict, 'Scrappers/Scrappers_files/imdb_movie_tags_list.csv')

# Launch the extraction of the reviews for a batch of movies with multi-processing
start = 0 # Parameter to be set depending of what has already been processed 
stop = 12 # Parameter to be set depending of what has already been processed
chunk = stop//6

if __name__ == '__main__':
    p = Pool(processes = 6)
    p1 = p.apply_async(imdb_createDB,['Scrappers/Scrappers_files/imdb_movie_tags_list.csv',start,chunk])
    p2 = p.apply_async(imdb_createDB,['Scrappers/Scrappers_files/imdb_movie_tags_list.csv',chunk,2*chunk])
    p3 = p.apply_async(imdb_createDB,['Scrappers/Scrappers_files/imdb_movie_tags_list.csv',2*chunk,3*chunk])
    p4 = p.apply_async(imdb_createDB,['Scrappers/Scrappers_files/imdb_movie_tags_list.csv',3*chunk,4*chunk])
    p5 = p.apply_async(imdb_createDB,['Scrappers/Scrappers_files/imdb_movie_tags_list.csv',4*chunk,5*chunk])
    p6 = p.apply_async(imdb_createDB,['Scrappers/Scrappers_files/imdb_movie_tags_list.csv',5*chunk,stop])

    p.close()
    p.join()

# Merge the reviews in one Dataframe
merged_df = p1.get()
for i in range(2,7):
    temp_df = eval('p'+str(i)).get()
    merged_df = merged_df.merge(temp_df, how = 'outer')
merged_df.set_index('user')

# Store the 1st batch into a csv
out_file = f'Scrappers/Scrappers_files/imdb_reviews_{start}_to_{stop}'
merged_df.to_csv(out_file,index=True)