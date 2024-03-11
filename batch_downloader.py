
import logging
import os
import re
import traceback

import instaloader
from dotenv import load_dotenv
import streamlit as st

from utils.post import show_post

logging.basicConfig(level=logging.INFO)

load_dotenv()
username = os.getenv('USERNAME')

st.set_page_config(page_title='Batch Instagram Content Downloader')

L = instaloader.Instaloader()
L.load_session_from_file(username)

posturls = st.text_area('URLs (one per line)')
submitbutton = st.button('Submit')

if submitbutton:
    urls = posturls.split('\n')
    for postcounter, posturl in enumerate(urls):
        # get shortcode
        matcher = re.match('https://www.instagram.com/p/([A-Za-z0-9\_\-]+)', posturl)

        st.subheader('Post {}: {}'.format(postcounter, posturl))
        logging.info('Post {}: {}'.format(postcounter, posturl))
        if matcher is None:
            st.warning('Invalid URL!')
        else:
            shortcode = matcher.group(1)
            logging.info('shortcode: {}'.format(shortcode))
            try:
                post = instaloader.Post.from_shortcode(L.context, shortcode)
            except instaloader.BadResponseException:
                st.warning('Unable to retrieve!')
                continue
            except instaloader.ConnectionException:
                extracebackstr = traceback.format_exc()
                print(extracebackstr)
                st.warning('Connection exception!')
            show_post(post)

