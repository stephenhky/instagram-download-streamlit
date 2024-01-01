
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


top_k = st.number_input('Number of saved posts shown', min_value=0)
if st.button('Retrieve'):
    saved_posts_iterator = profile.get_saved_posts()
    for i, post in enumerate(saved_posts_iterator):
        if i >= top_k:
            break
        show_post(post)
