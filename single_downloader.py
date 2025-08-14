
import logging
import os
import re

import instaloader
from dotenv import load_dotenv
import streamlit as st

from utils.post import show_post

logging.basicConfig(level=logging.INFO)

load_dotenv()
username = os.getenv('IGUSERNAME')

st.set_page_config(page_title='Instagram Content Downloader')

L = instaloader.Instaloader()
L.load_session_from_file(username)

posturl = st.text_input('URL')
submitbutton = st.button('Submit')

if submitbutton:
    # get shortcode
    matcher = re.match('https://www.instagram.com/p/([A-Za-z0-9_\-]+)', posturl)
    if matcher is not None:
        shortcode = matcher.group(1)
        logging.info('shortcode: {}'.format(shortcode))
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        show_post(post)
    else:
        st.warning('Invalid URL!')




