import streamlit as st
import google.generativeai as palm
# from dotenv import load_dotenv
import os
from gtts import gTTS
from io import BytesIO

# load_dotenv()
api_key = os.getenv("PALM_MODEL_API")

palm.configure(api_key=api_key)

defaults = {
  'model': 'models/chat-bison-001',
  'temperature': 0.95,
  'candidate_count': 1,
  'top_k': 40,
  'top_p': 0.95,
}

context = "You are VoxAura, Please be polite because kid is using for learn, give accurate information, be helpful and explain details."
examples = [
  [
    "what is your name?",
    "my name is VoxAura."
  ],
  [
    "Hi!",
    "Hi, my name is VoxAura."
  ],
  [
    "what is world war 1?",
    "World War I, also known as the First World War, was a global war originating in Europe that lasted from 28 July 1914 to 11 November 1918. Contemporaneously described as \"the war to end all wars,\" it led to the mobilisation of more than 70 million military personnel, including 60 million Europeans, making it one of the largest wars in history. Over 16 million people died, including 9.7 million Europeans, and an additional 7.9 million were wounded. Tens of millions of people died due to genocides (including the Armenian genocide), premeditated death from starvation, massacres, and disease. Aircraft played a major role in the conflict, including in strategic bombing of population centers, the development of tanks, the use of poison gas, and the first large-scale use of aircraft in combat. \r\n\r\nThe assassination of Archduke Franz Ferdinand of Austria by Gavrilo Princip on 28 June 1914 was the trigger that set off a chain of events leading to the war. Serbia's allies, Russia and France, and Austria-Hungary's ally, Germany, were drawn into the conflict. Within weeks, the major powers of Europe were at war. The Central Powers—Germany, Austria-Hungary, the Ottoman Empire, and Bulgaria—became known as the \"Central Powers,\" while the Entente Powers—Russia, France, Britain, Italy, Japan, and the United States—became known as the \"Entente Powers.\"\r\n\r\nThe war ended with the signing of the Armistice of 11 November 1918. The Treaty of Versailles, signed on 28 June 1919, formally ended the war between Germany and the Allied Powers. The war had a profound effect on the course of the 20th century. It led to the collapse of the Austro-Hungarian, Ottoman, and Russian Empires, and the creation of new countries, including Czechoslovakia, Yugoslavia, and Poland. The war also led to the formation of the League of Nations, an international organization dedicated to preventing future wars."
  ]
]
messages = []

def chat_bot(text):
    messages.append(text)
    response = palm.chat(
        **defaults,
        context=context,
        examples=examples,
        messages=messages  # Pass the messages list, not just the text
    )
    temp = response.last
    messages.append(temp)
    return temp

def generate_audio(text):
    mp3_fp = BytesIO()
    tts = gTTS(text, lang='en')
    tts.write_to_fp(mp3_fp)
    return mp3_fp

st.title("AI Chat Bot")

text = st.text_input("Enter your message")
if st.button("Search"):
    response = chat_bot(text)
    st.write(response)

    # Add audio play button to play the generated speech
    if response:
        st.audio(generate_audio(response), format='audio/ogg')
