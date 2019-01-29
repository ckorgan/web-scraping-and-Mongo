import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, redirect, url_for, jsonify
import pandas as pd
from pymongo import MongoClient

def get_mars_news(session):
    nasa_news_json_response = session.get('https://mars.nasa.gov/api/v1/news_items/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest',allow_redirects=True).json()
    mars_news_dict = []
    for news_item in nasa_news_json_response['items']:
        mars_news_dict.append({'title':news_item['title'],'description': news_item['description']})

    return mars_news_dict

def get_featured_image():
    jpl_host = 'https://www.jpl.nasa.gov'
    featured_image_response = requests.get(jpl_host + '/spaceimages/?search=&category=Mars')
    html_soup = BeautifulSoup(featured_image_response.text, 'html.parser')
    full_image_element = html_soup.select('#full_image')
    full_image_url = full_image_element[0].get_attribute_list('data-fancybox-href')[0]
    return jpl_host + full_image_url

def get_mars_weather(session):
    mars_weather_tweets = session.get('https://twitter.com/marswxreport?lang=en',allow_redirects=True)
    html_soup = BeautifulSoup(mars_weather_tweets.text, 'html.parser')
    mars_weather = html_soup.select('div.js-tweet-text-container p')[0].text
    return mars_weather

def get_mars_facts(session):
    mars_facts_response = session.get('http://space-facts.com/mars/',allow_redirects=True)
    html_soup = BeautifulSoup(mars_facts_response.text, 'html.parser')
    mars_facts_properties = html_soup.select('#tablepress-mars .column-1 strong')
    mars_facts_values = html_soup.select('#tablepress-mars .column-2')
    mars_fact_dict = {}
    for fact_index in range(0,len(mars_facts_properties)):
        mars_fact_dict[mars_facts_properties[fact_index].text[:-1]] = [mars_facts_values[fact_index].text]

    mars_df = pd.DataFrame(data=mars_fact_dict).T
    mars_df.index = mars_df.index.set_names(['description'])
    mars_df.columns = ['value']
    return mars_df.to_html()


def scrape():
    mars_data_dict = {}
    session = requests.Session()
    session.headers.update({
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'
    })

    mars_data_dict['mars_news'] = get_mars_news(session)
    mars_data_dict['mars_weather'] = get_mars_weather(session)
    mars_data_dict['mars_fact'] = get_mars_facts(session)
    mars_data_dict['featured_image_url'] = get_featured_image()
    return mars_data_dict
