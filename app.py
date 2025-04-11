import streamlit as st
import pandas as pd
from openai import OpenAI

# --- UI Config ---
st.set_page_config(page_title="Aranet AI Assistent", layout="wide")
st.title("🌱 Aranet AI Assistent")
st.caption("Stel hier je vragen over je gewichtsobservaties.")

# --- API Key Input ---
openai_api_key = st.text_input("Vul hier je OpenAI API key in", type="password")
if not openai_api_key:
    st.warning("Voer je OpenAI API key in om te starten.")
    st.stop()

client = OpenAI(api_key=openai_api_key)

# --- Data Loading ---
@st.cache_data
def load_data():
    df = pd.read_csv("aranet_observations.csv")
    return df

observations_df = load_data()
observations_text = "\n".join(observations_df["Observation"].tolist())

# --- User Question Input ---
user_question = st.text_area("Wat wil je weten?", placeholder="Bijv. Wat is er opvallend aan sensor 4.7E op 2 april?", height=100)

if st.button("🔍 Vraag AI"):
    if not user_question:
        st.warning("Typ eerst een vraag.")
        st.stop()

    with st.spinner("AI is aan het nadenken..."):
        prompt = f"""
Je bent een slimme assistent die gewichtsdata van Aranet-weegschalen analyseert. Hier zijn observaties:

{observations_text}

Beantwoord de volgende vraag op basis van bovenstaande observaties:

Vraag: {user_question}
Antwoord:
"""

        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
            )
            answer = response.choices[0].message.content.strip()
            st.success("✅ Antwoord van AI:")
            st.markdown(answer)

        except Exception as e:
            st.error(f"Er ging iets mis: {e}")

