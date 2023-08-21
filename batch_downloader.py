
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

st.set_page_config(page_title='Batch Instagram Content Downloader')

L = instaloader.Instaloader()
# L.load_session_from_file(username)

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
            st.text('Profile: {}'.format(post.profile))
            try:
                profile_name = post.owner_profile.full_name
                st.text('Name: {}'.format(profile_name))
            except instaloader.exceptions.LoginRequiredException:
                st.text('Owner profile name not available: login required.')
            try:
                profile_bib = post.owner_profile.biography
                st.markdown('Profile Bibliography: {}'.format(profile_bib))
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
                    st.components.v1.html(
                        '<a href="{}" target="_blank" rel="noreferrer noopener">Click to Open Video</a>'.format(
                            video_url, video_url
                        )
                    )
                else:
                    pic_url = node.display_url
                    st.components.v1.html(
                        '<a href="{}" target="_blank" rel="noreferrer noopener">Click to Open</a>'.format(
                            pic_url, pic_url
                        )
                    )

            if check_direct_url:
                logging.info(post.url)
                img = Image.open(urllib.request.urlopen(post.url))
                st.image(img, width=200)
                if post.is_video:
                    video_url = post.video_url
                    st.components.v1.html(
                        '<a href="{}" target="_blank" rel="noreferrer noopener">Click to Open Video</a>'.format(
                            video_url, video_url))
                else:
                    pic_url = post.url
                    st.components.v1.html(
                        '<a href="{}" target="_blank" rel="noreferrer noopener">Click to Open</a>'.format(pic_url,
                                                                                                          pic_url))

