import streamlit as st
import openai


st.set_page_config(page_title="Chatbot Maker", layout="wide")

if "bot" not in st.session_state:
    st.session_state.bot = False

if "API" not in st.session_state:
    st.session_state.API = ""

def reset_bot():
    st.session_state.bot = False

def createBot(personality, charecater, profesion,nationality, phrase, short, emoji):
    if st.session_state.API:
        st.session_state.bot = True
        st.session_state.messages = []
        full_response = ""
        if len(personality) != 0:
            full_response += "You are a" + " and".join(personality) + " Person. "
        if charecater:
            full_response += "You imitate the character " + charecater + ". "
        if profesion:
            full_response += "You work as a " + profesion
        if nationality:
            full_response += "You are from " + nationality + " with an accent. "
        if phrase.strip():
            full_response += "Your catchphrase is " + phrase + "."
        if short:
            full_response += "Please keep your responses short. "
        if emoji:
            full_response += "You love using emojis. "

        st.session_state.messages.append({"role":"system", "content":full_response})



    else:
        st.session_state.bot = False
        st.warning("API key not found. Please input your API key.")
        

with st.sidebar:
    with st.popover("Provide OpenAI API Key"):
        st.session_state.API = st.text_input("API Key", on_change=reset_bot)
    personality = st.multiselect("Personality", options=["Narsasisst", "Weeb","Gamer","Dumb", "optamistic"])
    charecater = st.selectbox("Charecater", options=["Spongebob", "Master chief from Halo", "Fiona from shrek", "Mr. Krabs", "Ghost from Call of duty"])
    profesion = st.selectbox("Profesion", options=["mercinary", "Programmer", "Racist", "Firefighter", "Astronaut", "Homeless", "Streamer"])
    nationality = st.selectbox("Nationality", options=["American", "Russian", "German", "Pakistani", "British", "Saudi"])
    phrase = st.text_input("CatchPhrase")
    short = st.toggle("Make responses short", False)
    emoji = st.toggle("Make emoji fanatic", True)
    st.button("Unleash Assistant Chatbot!", on_click=createBot, args=(personality, charecater, profesion,nationality, phrase, short, emoji))

st.header("assitant Chatbot Maker!")

if not st.session_state.bot:
    st.write("<h6>Please create a bot to start chatting.</h6>", unsafe_allow_html=True)
else:
    if "openai_model" not in st.session_state:
        st.session_state.openai_model = "gpt-3.5-turbo"
    for message in st.session_state.messages[1:]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    try:
        if prompt := st.chat_input():
            st.session_state.messages.append({"role":"user", "content":prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        client = openai.OpenAI(api_key=st.session_state.API)

        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model=st.session_state.openai_model,
                messages=st.session_state.messages,
                stream=True 
            )
            response = st.write_stream(stream)
            st.session_state.messages.append({"role":"assistant", "content":response})
    except openai.AutocompleteError:
        st.error("Wrong API!")
    except openai.RateLimitError:
        st.error("Rate limit exceeded!")



