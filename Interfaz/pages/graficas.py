import mysql.connector
import streamlit as st
import pandas as pd
import time
import datetime
import matplotlib.pyplot as plt
import numpy as np

from streamlit_option_menu import option_menu
from streamlit_autorefresh import st_autorefresh
from time import gmtime, strftime

# PÁGINA 2

with open( "style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

connection = mysql.connector.connect(host = 'localhost', user='root', password = '', database = 'esp32_data')
cursor = connection.cursor()


tempName = st.session_state['realname1']


col_0,col_01,col_02,col_03,col_04 = st.columns(5)
with col_0:
    if st.button("Salir"):
        st.session_state['avgtemp'] = 0.00
        st.session_state['avghum1'] = 0.00
        st.switch_page("pages/menuprincipal.py")
    

with col_04:
    if st.button("Cuenta"):
        st.switch_page("pages/ajustes.py")

today = datetime.date.today()

st.title("¡Hola" + " " + st.session_state['realname1'] + "!",anchor = False)
st.header("Hoy:", anchor = False)
st.subheader(today, anchor = False)



##st.session_state
today = datetime.date.today()

todaycomplete = datetime.datetime.today()
temp = todaycomplete
antes = todaycomplete - temp
fecha = today

promedioHumedad = 0
promedioTemperatura = 0


with st.container():
    
    colempty, coltemp, colhum, colempty2 = st.columns(4)
    with coltemp:
        st.image("termometro.png", width = 80)
        st.metric("Temperatura", str(st.session_state['avgtemp']) + " °C", "")
    with colhum:
        st.image("humedad.png", width = 80)
        st.metric("Humedad", str(st.session_state['avghum1']) + "%", "")
    st.caption("Última medición tomada hace un minuto")
    if (todaycomplete.minute - 1) < 10:
        if (todaycomplete.hour - 1) < 10:
            #st.write("SELECT COUNT(*) as Total FROM sensores WHERE timestamp LIKE '" +  str(fecha) + "_0" + str(todaycomplete.hour) + ":0" + str(todaycomplete.minute - 1) + "%'" + "AND id_dispositivo = '" + st.session_state['deviceid1'] + "';")
            cursor.execute("SELECT COUNT(*) as Total FROM sensores WHERE timestamp LIKE '" +  str(fecha) + "_0" + str(todaycomplete.hour) + ":0" + str(todaycomplete.minute - 1) + "%'" + "AND id_dispositivo = '" + st.session_state['deviceid1'] + "';")
            datos = cursor.fetchall()
            df = pd.DataFrame(datos,columns=cursor.column_names)
        else:
            #st.write("SELECT COUNT(*) as Total FROM sensores WHERE timestamp LIKE '" +  str(fecha) + "_" + str(todaycomplete.hour) + ":0" + str(todaycomplete.minute - 1) + "%'" + "AND id_dispositivo = '" + st.session_state['deviceid1'] + "';")
            cursor.execute("SELECT COUNT(*) as Total FROM sensores WHERE timestamp LIKE '" +  str(fecha) + "_" + str(todaycomplete.hour) + ":0" + str(todaycomplete.minute - 1) + "%'" + "AND id_dispositivo = '" + st.session_state['deviceid1'] + "';")
            datos = cursor.fetchall()
            df = pd.DataFrame(datos,columns=cursor.column_names)
    else:
        if (todaycomplete.hour - 1) < 10:
            #st.write("SELECT COUNT(*) as Total FROM sensores WHERE timestamp LIKE '" +  str(fecha) + "_0" + str(todaycomplete.hour) + ":" + str(todaycomplete.minute - 1) + "%'" + "AND id_dispositivo = '" + st.session_state['deviceid1'] + "';")
            cursor.execute("SELECT COUNT(*) as Total FROM sensores WHERE timestamp LIKE '" +  str(fecha) + "_0" + str(todaycomplete.hour) + ":" + str(todaycomplete.minute - 1) + "%'" + "AND id_dispositivo = '" + st.session_state['deviceid1'] + "';")
            datos = cursor.fetchall()
            df = pd.DataFrame(datos,columns=cursor.column_names)
        else:
            cursor.execute("SELECT COUNT(*) as Total FROM sensores WHERE timestamp LIKE '" +  str(fecha) + "_" + str(todaycomplete.hour) + ":" + str(todaycomplete.minute - 1) + "%'" + "AND id_dispositivo = '" + st.session_state['deviceid1'] + "';")
            #st.write("SELECT COUNT(*) as Total FROM sensores WHERE timestamp LIKE '" +  str(fecha) + "_" + str(todaycomplete.hour) + ":" + str(todaycomplete.minute - 1) + "%'" + "AND id_dispositivo = '" + st.session_state['deviceid1'] + "';")
            datos = cursor.fetchall()
            df = pd.DataFrame(datos,columns=cursor.column_names)

    if df.iloc[0]['Total'] > 1:
        totalDatos = df.iloc[0]['Total']

        cont = 0
        while cont < totalDatos:
            if (todaycomplete.minute - 1) < 10:
                if (todaycomplete.hour) < 10:
                    cursor.execute("SELECT humidity, temperature FROM sensores WHERE timestamp LIKE '" +  str(fecha) + "_0" + str(todaycomplete.hour) + ":0" + str(todaycomplete.hour) + ":0" +  str(todaycomplete.minute - 1) + "%'" + "AND id_dispositivo = '" + st.session_state['deviceid1'] + "';")
                    datos = cursor.fetchall()
                    df = pd.DataFrame(datos,columns=cursor.column_names)
              
                else:
                    cursor.execute("SELECT humidity, temperature FROM sensores WHERE timestamp LIKE '" +  str(fecha) + "_" + str(todaycomplete.hour) + ":0" +  str(todaycomplete.minute - 1) + "%'" + "AND id_dispositivo = '" + st.session_state['deviceid1'] + "';")
                    datos = cursor.fetchall()
                    df = pd.DataFrame(datos,columns=cursor.column_names)
         
            else:
                if (todaycomplete.hour) < 10:
                    cursor.execute("SELECT humidity, temperature FROM sensores WHERE timestamp LIKE '" +  str(fecha) + "_0" + str(todaycomplete.hour) + ":" +  str(todaycomplete.minute - 1) + "%'" + "AND id_dispositivo = '" + st.session_state['deviceid1'] + "';")
                    datos = cursor.fetchall()
                    df = pd.DataFrame(datos,columns=cursor.column_names)
                else:
                    cursor.execute("SELECT humidity, temperature FROM sensores WHERE timestamp LIKE '" +  str(fecha) + "_" + str(todaycomplete.hour) + ":" +  str(todaycomplete.minute - 1) + "%'" + "AND id_dispositivo = '" + st.session_state['deviceid1'] + "';")
                    datos = cursor.fetchall()
                    df = pd.DataFrame(datos,columns=cursor.column_names)
            
                promedioHumedad =  df.iloc[cont]['humidity']
                promedioTemperatura = df.iloc[cont]['temperature']
            cont = cont + 1

        promedioHumedad0 = promedioHumedad / totalDatos
        promedioTemperatura0 = promedioTemperatura / totalDatos

        st.session_state['avgtemp'] = promedioTemperatura 
        st.session_state['avghum1'] = promedioHumedad

    
    medir = st.button("Actualizar")
    if medir:
        todaycomplete = datetime.datetime.today()
        
        if (todaycomplete.minute) < 10:
            if (todaycomplete.hour) < 10:
                cursor.execute("SELECT COUNT(*) as Total FROM sensores WHERE timestamp LIKE '" +  str(fecha) + "_0" + str(todaycomplete.hour) + ":0" +  str(todaycomplete.minute) + "%'" + "AND id_dispositivo = '" + st.session_state['deviceid1'] + "';")
                #st.write("SELECT COUNT(*) as Total FROM sensores WHERE timestamp LIKE '" +  str(fecha) + "_0" + str(todaycomplete.hour) + ":0" +  str(todaycomplete.minute) + "%'" + "AND id_dispositivo = '" + st.session_state['deviceid1'] + "';")
                datos = cursor.fetchall()
                df = pd.DataFrame(datos,columns=cursor.column_names)
                #st.dataframe(df)
            else:
                cursor.execute("SELECT COUNT(*) as Total FROM sensores WHERE timestamp LIKE '" +  str(fecha) + "_" + str(todaycomplete.hour) + ":0" +  str(todaycomplete.minute) + "%'" + "AND id_dispositivo = '" + st.session_state['deviceid1'] + "';")
                #st.write()
                datos = cursor.fetchall()
                df = pd.DataFrame(datos,columns=cursor.column_names)
                #st.dataframe(df)
        else:
            if (todaycomplete.hour) < 10:
                cursor.execute("SELECT COUNT(*) as Total FROM sensores WHERE timestamp LIKE '" +  str(fecha) + "_0" + str(todaycomplete.hour) + ":" +  str(todaycomplete.minute) + "%'" + "AND id_dispositivo = '" + st.session_state['deviceid1'] + "';")
                #st.write()
                datos = cursor.fetchall()
                df = pd.DataFrame(datos,columns=cursor.column_names)
                #st.dataframe(df)
            else:
                cursor.execute("SELECT COUNT(*) as Total FROM sensores WHERE timestamp LIKE '" +  str(fecha) + "_" + str(todaycomplete.hour) + ":" +  str(todaycomplete.minute) + "%'" + "AND id_dispositivo = '" + st.session_state['deviceid1'] + "';")
                #st.write()
                datos = cursor.fetchall()
                df = pd.DataFrame(datos,columns=cursor.column_names)
                #st.dataframe(df)
        
        if df.iloc[0]['Total'] > 1:
            totalDatos = df.iloc[0]['Total']
            cont = 0
            while cont < totalDatos:
                if (todaycomplete.minute - 1) < 10:
                    if (todaycomplete.hour) < 10:
                        cursor.execute("SELECT humidity, temperature FROM sensores WHERE timestamp LIKE '" +  str(fecha) + "_0" + str(todaycomplete.hour) + ":0" +  str(todaycomplete.minute) + "%'" + "AND id_dispositivo = '" + st.session_state['deviceid1'] + "';")
                        datos = cursor.fetchall()
                        df = pd.DataFrame(datos,columns=cursor.column_names)
                        #st.dataframe(df)

                    else:
                        cursor.execute("SELECT humidity, temperature FROM sensores WHERE timestamp LIKE '" +  str(fecha) + "_" + str(todaycomplete.hour) + ":0" +  str(todaycomplete.minute) + "%'" + "AND id_dispositivo = '" + st.session_state['deviceid1'] + "';")
                        datos = cursor.fetchall()
                        df = pd.DataFrame(datos,columns=cursor.column_names)
                        #st.dataframe(df)
                    
                    #promedioHumedad = promedioHumedad + df.iloc[cont]['humidity']
                    #promedioTemperatura = promedioTemperatura + df.iloc[cont]['temperature']
                else:
                    if (todaycomplete.hour) < 10:
                        cursor.execute("SELECT humidity, temperature FROM sensores WHERE timestamp LIKE '" +  str(fecha) + "_0" + str(todaycomplete.hour) + ":" +  str(todaycomplete.minute) + "%'" + "AND id_dispositivo = '" + st.session_state['deviceid1'] + "';")
                        datos = cursor.fetchall()
                        df = pd.DataFrame(datos,columns=cursor.column_names)
                        #st.dataframe(df)
                    else:
                        cursor.execute("SELECT humidity, temperature FROM sensores WHERE timestamp LIKE '" +  str(fecha) + "_" + str(todaycomplete.hour) + ":" +  str(todaycomplete.minute) + "%'" + "AND id_dispositivo = '" + st.session_state['deviceid1'] + "';")
                        datos = cursor.fetchall()
                        df = pd.DataFrame(datos,columns=cursor.column_names)
                        #st.dataframe(df)

                promedioHumedad = df.iloc[cont]['humidity']
                promedioTemperatura = df.iloc[cont]['temperature']
                cont = cont + 1

            
            if promedioHumedad > 95.0:
                promedioHumedad = 95.0
            if promedioTemperatura > 50.0:
                promedioTemperatura = 50.0
            st.session_state['avgtemp'] = promedioTemperatura
            st.session_state['avghum1'] = promedioHumedad
    
columna1, columna2 = st.columns(2)

with columna1:
    with st.container(border = True):
        info_texto= '<p style="font-family:Courier; font-size: 25px; color:"#FF43A5";, align:center"><font color="#FBA62D">Tu información:</font></p>'
        st.markdown(info_texto, unsafe_allow_html=True)
        colV, colD = st.columns(2)
        with colV:
            temp = '<p style="font-family:Courier; font-size: 20px; color:"#FF43A5";, align:center">Nombre:</p>'
            st.markdown(temp, unsafe_allow_html=True)
            temp = '<p style="font-family:Courier; font-size: 20px; color:"#FF43A5";, align:center">Apellido:</p>'
            st.markdown(temp, unsafe_allow_html=True)
            temp = '<p style="font-family:Courier; font-size: 20px; color:"#FF43A5";, align:center">Edad:</p>'
            st.markdown(temp, unsafe_allow_html=True)
        with colD:
            html_datos = f"""
                            <style>
                            p.a {{
                            font: 20px Courier;
                            }}
                            </style>
                            <p class="a">{st.session_state['realname1']}</p>
                            """
            
            st.markdown(html_datos, unsafe_allow_html=True)
            html_datos = f"""
                            <style>
                            p.a {{
                            font: 20px Courier;
                            }}
                            </style>
                            <p class="a">{st.session_state['lastname1']}</p>
                            """
            
            st.markdown(html_datos, unsafe_allow_html=True)
            html_datos = f"""
                            <style>
                            p.a {{
                            font: 20px Courier;
                            }}
                            </style>
                            <p class="a">{st.session_state['age1']}</p>
                            """
            
            st.markdown(html_datos, unsafe_allow_html=True)

with columna2:

    st.subheader("Tus datos de:", anchor = False)
    today = datetime.date.today()
    fecha = st.date_input("",today)

    cursor.execute("Select COUNT(*) as Total from sensores Where timestamp LIKE  '" + str(fecha) + "%' AND id_dispositivo ='" + st.session_state['deviceid1'] + "';")
    datos = cursor.fetchall()
    df = pd.DataFrame(datos,columns=cursor.column_names)
    if df.iloc[0]['Total'] > 0:
        cursor.execute("Select * from sensores Where timestamp LIKE  '" + str(fecha) + "%' AND id_dispositivo ='" + st.session_state['deviceid1'] + "';")
        datos = cursor.fetchall()
        df = pd.DataFrame(datos, columns=cursor.column_names)
        with st.container(border = True):
            
            fig, ax = plt.subplots()
            ax.plot(df.timestamp,df.humidity,'-', color = "orange", linewidth=1.5)
            ax.plot(df.timestamp,df.temperature, color = "#ff43a5", linewidth=2.5)
            ax.plot(df.timestamp[df.humidity > 80.0],df.humidity[df.humidity > 80.0],'o', color = "#FF6100", linewidth=1.5)
            ax.plot(df.timestamp[df.temperature > 30.0],df.temperature[df.temperature > 30.0],'o', color = "red", linewidth=1.5)
            ax.set_title('Humedad y temperatura')
            st.pyplot(fig)

            st.image("leyenda.png", width = 200)

            fig2, ax = plt.subplots()
            ax.plot(df.timestamp,df.humidity,'-', color = "orange", linewidth=1.5)
            ax.plot(df.timestamp[df.humidity > 80.0],df.humidity[df.humidity > 80.0],'o', color = "#FF6100", linewidth=1.5)
            ax.set_title('Humedad')
            st.pyplot(fig2)

            fig3, ax = plt.subplots()
            ax.plot(df.timestamp,df.temperature, color = "#ff43a5", linewidth=2.5)
            ax.plot(df.timestamp[df.temperature > 30.0],df.temperature[df.temperature > 30.0],'o', color = "red", linewidth=1.5)
            ax.set_title('Temperatura')
            st.pyplot(fig3)
            

    else:
        st.write("No se encontraron datos para esta fecha")
