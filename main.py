
import logging
import os
import re
import urllib

from PIL import Image
import instaloader
from dotenv import load_dotenv
import streamlit as st

logging.basicConfig(level=logging.INFO)

load_dotenv()
username = os.getenv('USERNAME')


L = instaloader.Instaloader()
L.load_session_from_file(username)

posturl = st.text_input('URL')
submitbutton = st.button('Submit')

if submitbutton:
    # get shortcode
    matcher = re.match('https://www.instagram.com/p/([A-Za-z0-9\_]+)', posturl)
    if matcher is not None:
        shortcode = matcher.group(1)
        logging.info('shortcode: {}'.format(shortcode))
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        for node in post.get_sidecar_nodes():
            logging.info(node.display_url)
            img = Image.open(urllib.request.urlopen(node.display_url))
            st.image(img, width=200)
            st.components.v1.html('<a href="{}"><img src="{}"></a>'.format(node.display_url, node.display_url))
    else:
        st.warning('Invalid URL!')




