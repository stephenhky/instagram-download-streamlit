
import logging
from PIL import Image
import urllib

import streamlit as st
import instaloader


def show_post(post):
    st.markdown('Date: {}'.format(post.date_local.strftime('%Y-%m-%d %H:%M')))
    st.text('Profile: {}'.format(post.profile))
    try:
        profile_name = post.owner_profile.full_name
        st.text('Name: {}'.format(profile_name))
    except instaloader.exceptions.LoginRequiredException:
        st.text('Owner profile name not available: login required.')
    try:
        profile_bib = post.owner_profile.biography
        st.markdown('Profile Biography: {}'.format(profile_bib))
    except instaloader.exceptions.LoginRequiredException:
        st.text('Owner profile not available: login required.')
    st.markdown('Post caption: {}'.format(post.caption))

    nodes = post.get_sidecar_nodes()
    check_direct_url = True

    for node in nodes:
        check_direct_url = False
        logging.info(node.display_url)
        img = Image.open(urllib.request.urlopen(node.display_url))
        st.image(img, width=200)

        if node.is_video:
            video_url = node.video_url
            st.link_button('Click to Open Video', video_url)
        else:
            pic_url = node.display_url
            st.link_button('Click to Open Image', pic_url)

    if check_direct_url:
        logging.info(post.url)
        img = Image.open(urllib.request.urlopen(post.url))
        st.image(img, width=200)
        if post.is_video:
            video_url = post.video_url
            st.link_button('Click to Open Video', video_url)
        else:
            pic_url = post.url
            st.link_button('Click to Open Image', pic_url)
