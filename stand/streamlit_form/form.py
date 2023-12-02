import base64
import time
from io import BytesIO
from pathlib import Path

import requests
import streamlit as st
import yaml

from stand.streamlit_form.config import DEFAULT_CONFIG
from stand.streamlit_form.typing import Config

LATITUDE_INPUT_PARAMS = {
    'label': 'Широта',
    'min_value': -90.,
    'max_value': 90.,
    'step': 1.,
    'placeholder': 'unset',
    'format': '%2.6f',
    'value': None,
}
LONGITUDE_INPUT_PARAMS = {
    'label': 'Долгота',
    'min_value': -180.,
    'max_value': 180.,
    'step': 1.,
    'placeholder': 'unset',
    'format': '%3.6f',
    'value': None,
}

CONFIG_FILE = Path('stand/streamlit_form/config.yaml')
if CONFIG_FILE.exists():
    with CONFIG_FILE.open() as fd:
        CONFIG: Config = yaml.safe_load(fd.read())
else:
    CONFIG: Config = DEFAULT_CONFIG

with open('stand/streamlit_form/static/style.css') as fd:
    st.markdown(f'<style>{fd.read()}</style>', unsafe_allow_html=True)

with st.sidebar:
    st.title('Сервис распознавания объектов на снимках местности')
    with st.form('form'):
        file = st.file_uploader(
            label='Empty',
            type=['png', 'jpg', 'jpeg', 'tif', 'tiff'],
            accept_multiple_files=False,
        )

        col1, col2 = st.columns(2)

        with col1:
            st.subheader('Координаты левого верхнего угла снимка')
            left_lon = st.number_input(**LONGITUDE_INPUT_PARAMS, key='left_lon')
            top_lat = st.number_input(**LATITUDE_INPUT_PARAMS, key='top_lat')
        with col2:
            st.subheader('Координаты правого нижнего угла снимка')
            right_lon = st.number_input(**LONGITUDE_INPUT_PARAMS, key='right_lon')
            bottom_lat = st.number_input(**LATITUDE_INPUT_PARAMS, key='bottom_lat')

        submit = st.form_submit_button('Разметить')

        if submit:
            if not file:
                st.error('Необходимо приложить снимок')
                st.stop()
            if not all(map(lambda x: x is not None, (left_lon, top_lat, right_lon, bottom_lat))):
                st.warning('Координаты и размеры объектов не будут вычислены', icon="⚠️")

if submit:
    with st.spinner('Размечаем снимок'):
        response = requests.post(
            f'{CONFIG["api_host"]}/{CONFIG["api_base_url"]}/markup',
            json={
                'image': {
                    'base64data': base64.b64encode(file.read()).decode('ascii'),
                    'filename': file.name,
                }
            },
            timeout=CONFIG['api_timeout'],
        )

    if response.status_code != 200:
        st.error('Что-то пошло не так :( Пожалуйста, попробуйте позже')
    else:
        io = BytesIO()
        io.write(base64.b64decode(response.json()['image'].encode('ascii')))
        st.image(io)
