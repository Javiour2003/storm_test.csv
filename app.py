import streamlit as st
from streamlit_lottie import st_lottie
import json
from API import get_prediction
import openai
import whois

model_path = r"C:\Users\admin\OneDrive\Desktop\storm_test.csv\Phishing-Attack-Domain-Detection-main\models\Malicious_URL_Prediction.h5"

st.title("Check :red[malacious] websites here!")

def load_lottiefile(filepath: str):
    with open(filepath,'r') as f:
        return json.load(f)

with st.container():
    col1,col2 = st.columns((8,6))
    with col1:

        url = None

        url = st.text_input("Enter URL here")
        button_clicked = st.button("Search")

        if url is not None:
            if button_clicked:
                prediction = get_prediction(url,model_path)
                if prediction is not None:
                    st.write(f'The Probability of the website being malacious is {str(prediction)}%')
        else:
            st.write("Please enter a URL")
        
    with col2:
        animate = load_lottiefile("Imgs/animation_lnc0v5fs.json")
        st_lottie(
            animate,
            loop = True,
            quality="medium",
            height=250,
            width=345
        )

my_secret = st.secrets['my_secrets']

openai.api_key = my_secret['OPENAI_API_KEY']

try:
    url_whois = whois.whois(url)
except whois.parser.PywhoisError as e:
    print(f"WHOIS query failed with error: {e}")
except Exception as ex:
    print(f"An unexpected error occurred: {ex}")



st.header("💬 Ask more questions about the URL to your AI powered Anti-Phishing assistant:") 
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "I am your AI powered Anti-Phishing assistant.How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                            messages = [
                                                        {"role": "system", "content": f"You are a helpful cyber security assistant who helps to detect the possibility of a phishing website by interpreting the WHOIS data provided in {url_whois}. Do not show the unnecesary WHOIS data, just give meaningful insights in short   that would help the user to get a better undertanding if the url is malacious or not."},
                                                        {"role": "user", "content": prompt}
                                                    ])
    msg = response.choices[0].message
    st.session_state.messages.append(msg)
    st.chat_message("assistant").write(msg.content) 
      


