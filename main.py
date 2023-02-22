
import logging
import os
import re

import instaloader
from dotenv import load_dotenv
import streamlit as st

logging.basicConfig(level=logging.INFO)

load_dotenv()
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')


L = instaloader.Instaloader()
L.login(username, password)

posturl = st.text_input('URL')
submitbutton = st.button('Submit')

if submitbutton:
    # get shortcode
    matcher = re.match('https://www.instagram.com/p/([A-Za-z0-9]+)', posturl)
    if matcher is not None:
        shortcode = matcher.group(1)
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        for node in post.get_sidecar_nodes():
            st.image(node.display_url)
    else:
        st.warning('Invalid URL!')




