import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import io
from PIL import Image
import os
from openpyxl.drawing.image import Image as XLImage

# Configuració inicial de la pàgina
st.set_page_config(page_title="Sistema de Valoració - Cercle", layout="wide")

# Inicialitzar l'estat de la sessió si no existeix
if 'vots' not in st.session_state:
    st.session_state.vots = []
    st.session_state.temps = []

# Títol principal
st.title("📊 Valoració de l'espai de cercle")
st.subheader("Qué t'ha semblat avui?")

# Estil CSS per fer els botons més grans i quadrats
st.markdown("""
    <style>
    div.stButton > button {
        height: 100px;
        width: 100%;
        font-size: 24px;
        margin: 10px 0px;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    </style>
""", unsafe_allow_html=True)

# Botons de votació amb emojis
if st.button("😄 M'ha agradat!", use_container_width=True):
    st.session_state.vots.append(3)
    st.session_state.temps.append(datetime.now())
    st.success("Gràcies pel teu vot!")
    
if st.button("😐 M'ha agradat a mitges", use_container_width=True):
    st.session_state.vots.append(2)
    st.session_state.temps.append(datetime.now())
    st.success("Gràcies pel teu vot!")
    
if st.button("☹️ No m'ha agradat", use_container_width=True):
    st.session_state.vots.append(1)
    st.session_state.temps.append(datetime.now())
    st.success("Gràcies pel teu vot!")

# Mostrar gràfica si hi ha vots
if st.session_state.vots:
    df = pd.DataFrame({
        'valoració': st.session_state.vots,
        'hora': st.session_state.temps
    })
    df['valoració'] = df['valoració'].map({
        1: 'No m\'ha agradat',
        2: 'M\'ha agradat a mitges',
        3: 'M\'ha agradat'
    })
    
    fig = px.histogram(
        df,
        x='valoració',
        title="Resultats de la votació",
        category_orders={"valoració": ["No m'ha agradat", "M'ha agradat a mitges", "M'ha agradat"]},
        color='valoració',
        color_discrete_sequence=['#007DA4', '#40BF9A', '#FFD948']
    )
    
    # Fer la gràfica més alta
    fig.update_layout(height=400)
    
    st.plotly_chart(fig, use_container_width=True)

# Modificar la part de descàrrega per fer-la més simple
if st.button("💾 Descarregar resultats"):
    if st.session_state.vots:
        try:
            # Crear DataFrame amb vots i temps
            df = pd.DataFrame({
                'valoració': st.session_state.vots,
                'data_i_hora': st.session_state.temps
            })
            
            # Convertir els números a text descriptiu
            df['valoració'] = df['valoració'].map({
                1: 'No m\'ha agradat',
                2: 'M\'ha agradat a mitges',
                3: 'M\'ha agradat'
            })
            
            # Formatar la data i hora en format llegible
            df['data_i_hora'] = df['data_i_hora'].dt.strftime('%d/%m/%Y %H:%M:%S')
            
            # Crear Excel amb timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nom_arxiu = f'resultats_votacio_{timestamp}.xlsx'
            
            # Guardar només les dades en format Excel
            df.to_excel(nom_arxiu, index=False, sheet_name='Registre de vots')
            
            # Crear botó de descàrrega
            with open(nom_arxiu, 'rb') as f:
                st.download_button(
                    label="📥 Clic per descarregar l'Excel",
                    data=f,
                    file_name=nom_arxiu,
                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
            
            # Eliminar l'arxiu temporal després de la descàrrega
            os.remove(nom_arxiu)
                
        except Exception as e:
            st.error(f"Hi ha hagut un error en generar l'Excel: {str(e)}")
    else:
        st.warning("No hi ha vots per descarregar!")

# Mostrar recompte total de vots
st.markdown(f"**Total de vots: {len(st.session_state.vots)}**") 