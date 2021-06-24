from __future__ import unicode_literals
import pandas as pd
import urllib
from selenium import webdriver
import time
import logging

logging.basicConfig(level=logging.INFO)

video_sheet = pd.read_csv('apple_daily.csv')
video_sheet['link'] = 'https://www.youtube.com/watch?v=' + video_sheet['url']
video_sheet['link_decode'] = video_sheet['link'].apply(lambda x: urllib.parse.quote(x).replace('/','%2F'))
video_sheet['cdn_link'] = f"https://yt1s.com/en6?q=" + video_sheet['link_decode']

cdn_list = video_sheet['cdn_link'].to_list()
title_list = video_sheet['title'].to_list()

options = webdriver.ChromeOptions()
options.add_experimental_option("prefs", {"download.default_directory":"D:\Apple Daily\果籽"})
driver = webdriver.Chrome(executable_path='chromedriver.exe', options=options)
for idx, video in enumerate(cdn_list[15:]):
    try:
        driver.get(video)
        time.sleep(5)
        get_link_button = driver.find_elements_by_xpath('//*[@id="btn-action"]')
        get_link_button[0].click()
        time.sleep(5)
        download_button = driver.find_elements_by_xpath('//*[@id="asuccess"]')
        download_button[0].click()
        logging.info(f'{idx}/{len(cdn_list)} - Backup {title_list[idx]}')
    except:
        logging.info(f'SKIPPED: {idx}/{len(cdn_list)} - Backup {title_list[idx]}')
time.sleep(60)
driver.quit()
