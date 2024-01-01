
import os
import logging

from dotenv import load_dotenv
import instaloader
import streamlit as st

from utils.post import show_post


logging.basicConfig(level=logging.INFO)

load_dotenv()
username = os.environ['USERNAME']



L = instaloader.Instaloader()
L.load_session_from_file(username)

profile = instaloader.Profile.from_username(L.context, username)


top_k = st.number_input('Number of saved posts shown', min_value=1)
min_k = st.number_input('Starting from...', min_value=0)

if st.button('Retrieve'):
    if top_k <= min_k:
        st.markdown('Warning: min_k < top_k please!')
    else:
        saved_posts_iterator = profile.get_saved_posts()
        for i, post in enumerate(saved_posts_iterator):
            if i < min_k:
                continue
            if i >= top_k:
                break
            instagram_url = 'https://www.instagram.com/p/{}'.format(post.shortcode)
            st.subheader('Post {}: {}'.format(i, instagram_url))
            logging.info('Post {}: {}'.format(i, instagram_url))
            show_post(post)
            st.divider()
