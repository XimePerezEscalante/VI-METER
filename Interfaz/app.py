import streamlit as st

menuprincipal_page = st.Page(
    page = "pages/menuprincipal.py",
    title = "Menú Principal",
    icon = "🏠",
    default = True,
)

graficas_page = st.Page(
    page = "pages/graficas.py",
    title = "Inicio",
    icon = "🚲",
)

ajustes_page = st.Page(
    page = "pages/ajustes.py",
    title = "Información",
    icon = "ℹ️",
)

if 'username1' not in st.session_state:
    st.session_state['username1'] = "nombre de usuario"

if 'username2' not in st.session_state:
    st.session_state['username2'] = ""

if 'pwd1' not in st.session_state:
    st.session_state['pwd1'] = ""

if 'pwd2' not in st.session_state:
    st.session_state['pwd2'] = ""

if 'realname1' not in st.session_state:
    st.session_state['realname1'] = "Usuario"

if 'lastname1' not in st.session_state:
    st.session_state['lastname1'] = "Apellido"

if 'age1' not in st.session_state:
    st.session_state['age1'] = 15

if 'device1' not in st.session_state:
    st.session_state['device1'] = "VI-METER"

if 'deviceid1' not in st.session_state:
    st.session_state['deviceid1'] = "VMT_001"

if 'avghum1' not in st.session_state:
    st.session_state['avghum1'] = 0.00

if 'avgtemp' not in st.session_state:
    st.session_state['avgtemp'] = 0.00


# NAVEGACIÓN

pg = st.navigation(pages = [menuprincipal_page,graficas_page,ajustes_page], position = "hidden")
pg.run()

#Link al logo
image = "VIMLOGO.png"
#Poner logo
st.logo(image,link=None, icon_image=None)