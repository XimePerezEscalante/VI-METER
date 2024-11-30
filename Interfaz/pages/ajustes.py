import mysql.connector
import streamlit as st
import pandas as pd
import time
import datetime
import numpy as np

from streamlit_option_menu import option_menu
from streamlit_autorefresh import st_autorefresh
from time import gmtime, strftime

with open( "style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

connection = mysql.connector.connect(host = 'localhost', user='root', password = '', database = 'esp32_data')
cursor = connection.cursor()

c1, c2, c3, c4, c5 = st.columns(5)

with c5:
    if st.button("Inicio"):
        st.switch_page("pages/graficas.py")


st.title("Tu cuenta")

colVar, colVal = st.columns(2)
with colVar:
    st.subheader("Tu dispositivo: ", divider = "orange")
    st.subheader("Nombre de usuario: ", divider = "orange")
    st.subheader("Nombre del dispositivo: ", divider = "orange")


with colVal:
    st.subheader(st.session_state['deviceid1'], divider = "gray")
    st.subheader(st.session_state['username1'], divider = "gray")
    st.subheader(st.session_state['device1'], divider = "gray")


if st.button("Cerrar sesión"):
    st.session_state['avgtemp'] = 0.00
    st.session_state['avghum1'] = 0.00
    st.switch_page("pages/menuprincipal.py")
