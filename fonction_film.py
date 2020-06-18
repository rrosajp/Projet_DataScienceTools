# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 15:49:34 2020
@author: Jules
"""

from warnings import warn
import bs4
import requests
import seaborn as sns; sns.set(style="ticks", color_codes=True)
import fonction_scraping as scrap

#def extraction_movie_data_from_link(link):
def extraction_movie_data_from_link(link, mv_attributs):
    '''
    Get some information from a movie link
    
    :param1 String link: http url that point to the movie
    :param2 tupe mv_attributs : tupe of all the data frome movies
    :return tupe mv_attributs: tupe of all the data frome movies
    :rtype: tupe of list

    '''

    page_link = link
    response = requests.get(page_link)
    html = bs4.BeautifulSoup(response.text, 'html.parser')

    nb_genre = 0
    #get the movie genres
    div = html.find('div', class_="subtext")
    #test_genre = False
    for a in div.find_all('a'):
        #test_genre = False
        title = a.get('title')
        #there is a balise title which we do not want
        if title is None:
            mv_attributs[7+nb_genre].append(a.text)
            #test_genre = True
            nb_genre += 1
    if nb_genre == 1:
        mv_attributs[8].append(None)
        mv_attributs[9].append(None)
        nb_genre = 3
    if nb_genre == 2:
        mv_attributs[9].append(None)
        nb_genre = 3
        """
        if not test_genre:
            mv_attributs[7+nb_genre].append(None)
            nb_genre += 1
        """
    #get the stars acting in the movie
    stars = []
    nb_act = 0
    test_stars = False
    for credit in html.find_all('div', class_='credit_summary_item'):
        #test_stars = False
        inline = credit.h4.text
        if inline == "Stars:":
            for a in credit.find_all('a'):
                href = a.get('href')
                if href != "fullcredits/":
                    mv_attributs[10+nb_act].append(a.text)
                    test_stars = True
                    nb_act += 1

    if not test_stars:
        mv_attributs[10+nb_act].append(None)
        nb_act += 1

    award = html.find('div', id='titleAwardsRanks', class_='article highlighted')
    test_rank = False
    test_nb_oscar = False
    test_win = False
    test_nom = False

    if award is not None:

        # movie rank
        if award.find('strong') is not None:
            strong = award.find('strong').text
            rank = scrap.clean_chars(strong)
            mv_attributs[13].append(rank)
            test_rank = True


        # oscars, wins and nominations
        if award.find_all('span', class_="awards-blurb") is not None:

            for span in award.find_all('span', class_="awards-blurb"):

                osc_bool = False
                # if there is/are oscar/s
                if span.find('b') is not None:
                    nb_oscar = span.find('b').text
                    nb_oscar = scrap.clean_chars(nb_oscar)
                    mv_attributs[14].append(nb_oscar)
                    osc_bool = True
                    test_nb_oscar = True

                # if there is/are oscar/s
                elif osc_bool == True:
                    length = len(span.text)
                    win = span.text[:length - 24]
                    win = scrap.clean_chars(win)
                    mv_attributs[15].append(win)
                    test_win = True

                    nom = span.text[32:]
                    nom = scrap.clean_chars(nom)
                    mv_attributs[16].append(nom)
                    test_nom = True
                # if not
                else:
                    length = len(span.text)
                    
                    if length > 30:
                    
                        win = span.text[:length - 24]
                        win = scrap.clean_chars(win)
                        mv_attributs[15].append(win)
                        test_win = True

                        nom = span.text[15:]
                        nom = scrap.clean_chars(nom)
                        mv_attributs[16].append(nom)
                        test_nom = True
                    else:
                        win = None
                        nom = span.text
                        nom = scrap.clean_chars(nom)
                        mv_attributs[16].append(nom)
                        test_nom = True

    if not test_rank:
        mv_attributs[13].append(None)
    if not test_nb_oscar:
        mv_attributs[14].append(None)
    if not test_win:
        mv_attributs[15].append(None)
    if not test_nom:
        mv_attributs[16].append(None)

    test_runtime=False
    test_budget=False
    test_gross=False

    for div in html.find_all('div', class_="txt-block"):
        if div.find('h4', class_='inline') is not None:
            inline = div.find('h4', class_='inline').text
            # find the runtime in minutes
            if inline == "Runtime:":
                runtime = div.find('time').text
                runtime = scrap.clean_chars(runtime)
                mv_attributs[17].append(runtime)
                test_runtime = True

            # find the movie budget
            if inline == "Budget:":
                budget = div.text
                budget = scrap.clean_chars(budget)
                mv_attributs[18].append(budget)
                test_budget = True

            # find the movie worldwide gross
            if inline == "Cumulative Worldwide Gross:":
                gross = div.text
                gross = scrap.clean_chars(gross)
                mv_attributs[19].append(gross)
                test_gross = True

    if not test_runtime:
        mv_attributs[17].append(None)
    if not test_budget:
        mv_attributs[18].append(None)
    if not test_gross:
        mv_attributs[19].append(None)

    return mv_attributs


def warning_request(response, nb_requests):
    '''
    Throw a warning for any status codes different than 200
    :param string response:
    :return: void
    :rtype: None
    '''
    if response.status_code != 200:
        warn(': {}; Status code: {}'.format(nb_requests, response.status_code))


#extraction_movie_data_from_link(f"https://www.imdb.com/title/tt7286456/?ref_=hm_fanfav_tt_2_pd_fp1")