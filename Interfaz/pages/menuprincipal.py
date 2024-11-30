import mysql.connector
import streamlit as st
import pandas as pd
import time
import datetime
import numpy as np

from time import gmtime, strftime

with open( "style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

connection = mysql.connector.connect(host = 'localhost', user='root', password = '', database = 'esp32_data')
cursor = connection.cursor()

def checarUsuario(user):
    cursor.execute("Select COUNT(*) as Total from datos_usuario WHERE nombre_usuario = '" + nombre_usuario + "';")
    datos = cursor.fetchall()
    df = pd.DataFrame(datos,columns=cursor.column_names)
    if df.iloc[0]['Total'] > 0:
        return True
    else:
        return False

registro_tab, inicio_tab = st.tabs(["Registrar cuenta","Iniciar sesión"])

with registro_tab:
    #Título
    original_title = '<p style="font-family:Courier; font-size: 100px; align:center">VI-METER</p>'
    st.markdown(original_title, unsafe_allow_html=True)
    with st.container(border = True):
        nombre_usuario = st.text_input("Nombre de usuario", "")
        if len(nombre_usuario) == 0:
            st.error("Introduce un nombre de usuario válido")
        pwd = st.text_input("Contraseña (Mínimo 8 caracteres)", "", type = "password")
        if len(pwd) < 8:
            st.error("Contraseña inválida: introduce mínimo 8 caracteres")
        nombre_real = st.text_input("Nombre", "")
        if len(nombre_real) == 0:
            st.error("Introduce tu nombre")
        apellido = st.text_input("Apellido (sólo uno)", "")
        if len(apellido) == 0:
            st.error("Introduce tu apellido")
        edad = st.number_input("Edad (15+)",15,100, value = None)
        if edad == None:
            st.error("Introduce tu edad")
        dispositivoID = st.text_input("Introduce el ID de tu VI-METER (ej: VMT_001)", "")
        if dispositivoID == None:
            st.error("Introduce un ID")
        cursor.execute("Select COUNT(*) as Total from dispositivo WHERE id_dispositivo = '" + dispositivoID + "';")
        datos = cursor.fetchall()
        df = pd.DataFrame(datos,columns=cursor.column_names)
        if df.iloc[0]['Total'] > 0:
            st.error("Este ID ya está registrado a otra cuenta")
            dispositivoID = ""
        dispositivo = st.text_input("Escoge un nombre para tu terrario", "VI-METER")
        if nombre_usuario and pwd and nombre_real and apellido and edad and dispositivoID:
            if st.button("Registrar"):
                with st.spinner("Registrando..."):
                    time.sleep(1.5)
                    
                    if checarUsuario(nombre_usuario) == True:
                        st.error("Nombre de usuario no disponible")
                    else:
                        st.session_state['username1'] = nombre_usuario
                        st.session_state['pwd1'] = pwd
                        st.session_state['realname1'] = nombre_real
                        
                        st.session_state['lastname1'] = apellido

                        st.session_state['age1'] = edad
                        st.session_state['device1'] = dispositivo
                        st.session_state['deviceid1'] = dispositivoID

                        cursor.execute("INSERT INTO dispositivo (id_dispositivo, nombre) VALUES('" + dispositivoID + "','" + dispositivo + "');")
                        connection.commit()

                        cursor.execute("INSERT INTO datos_usuario (nombre_usuario, contrasena, nombre, apellido, edad, dispositivo, id_dispositivo) VALUES('" + nombre_usuario + "','" + pwd + "','" + nombre_real + "','" + apellido + "'," + str(edad) + ",'" + dispositivo + "','" + dispositivoID + "');")
                        connection.commit()
                        cursor.execute("UPDATE dispositivo SET nombre_usuario ='" + nombre_usuario + "' WHERE id_dispositivo = '" + dispositivoID + "';")
                        connection.commit()
                        st.toast("Usuario registrado con éxito", icon = "🥳")

                        st.switch_page("pages/graficas.py")



with inicio_tab:
    #Título
    original_title = '<p style="font-family:Courier; font-size: 100px; align:center">VI-METER</p>'
    st.markdown(original_title, unsafe_allow_html=True)
    with st.container(border = True):
        nombre_usuario = st.text_input("Nombre de usuario", "", key = "username2")
        if len(nombre_usuario) == 0:
            st.error("Introduce un nombre de usuario válido")
        pwd = st.text_input("Contraseña (Mínimo 8 caracteres)", "", type = "password", key = "pwd2")
        if len(pwd) < 8:
            st.error("Contraseña inválida: introduce mínimo 8 caracteres")
        if nombre_usuario and pwd:
            if st.button("Iniciar sesión"):
                with st.spinner("Iniciando sesión..."):
                    time.sleep(1.5)
                    if checarUsuario(nombre_usuario) == True:
                        cursor.execute("SELECT contrasena,id_dispositivo,nombre,apellido,edad,dispositivo FROM `datos_usuario` WHERE nombre_usuario = '" + nombre_usuario + "';")
                        datos = cursor.fetchall()
                        df = pd.DataFrame(datos,columns=cursor.column_names)
                        if df.iloc[0]['contrasena'] == pwd:
                            st.toast("Sesión iniciada con éxito", icon = "🥳")
                            st.session_state['username1'] = nombre_usuario
                            st.session_state['pwd1'] = pwd
                            st.session_state['deviceid1'] = df.iloc[0]['id_dispositivo']
                            st.session_state['realname1'] = df.iloc[0]['nombre']
                            st.session_state['lastname1'] = df.iloc[0]['apellido']
                            st.session_state['age1'] = df.iloc[0]['edad']
                            st.session_state['device1'] = df.iloc[0]['dispositivo']
                            st.switch_page("pages/graficas.py")
                        else:
                            st.error("Contraseña incorrecta")
                    else:
                        st.error("El usuario que ingresaste no existe")
