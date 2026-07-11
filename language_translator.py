import streamlit as st
from deep_translator import GoogleTranslator
import pyperclip
import tempfile
import os


st.set_page_config(
    page_title="AI Language Translator",
    page_icon="🌍",
    layout="centered"
)

st.markdown("""
<style>
.main{
    background-color:#f7f9fc;
}
.stButton>button{
    width:100%;
    border-radius:10px;
    height:45px;
    font-size:16px;
}
textarea{
    font-size:16px !important;
}
</style>
""", unsafe_allow_html=True)

st.title("🌍 AI Language Translation Tool")
st.write("Translate text instantly using Google Translator")


languages = {
    "Auto Detect": "auto",
    "English": "en",
    "Hindi": "hi",
    "Telugu": "te",
    "Tamil": "ta",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Marathi": "mr",
    "Gujarati": "gu",
    "Punjabi": "pa",
    "Bengali": "bn",
    "Urdu": "ur",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Italian": "it",
    "Portuguese": "pt",
    "Russian": "ru",
    "Chinese": "zh-CN",
    "Japanese": "ja",
    "Korean": "ko",
    "Arabic": "ar"
}


if "history" not in st.session_state:
    st.session_state.history = []


text = st.text_area(
    "Enter Text",
    height=180,
    placeholder="Type something here..."
)

st.caption(f"Characters: {len(text)}")

col1, col2 = st.columns(2)

with col1:
    source = st.selectbox(
        "Source Language",
        list(languages.keys()),
        index=0
    )

with col2:
    target = st.selectbox(
        "Target Language",
        list(languages.keys()),
        index=1
    )


if st.button("🔄 Swap Languages"):
    source, target = target, source

translated = ""


if st.button("🌐 Translate"):

    if text.strip() == "":
        st.warning("Please enter some text.")

    elif source == target:
        st.warning("Source and Target language cannot be the same.")

    else:

        try:

            translator = GoogleTranslator(
                source=languages[source],
                target=languages[target]
            )

            translated = translator.translate(text)

            st.success("Translation Successful")

            st.text_area(
                "Translated Text",
                translated,
                height=180
            )

            st.session_state.history.append({
                "Input": text,
                "Output": translated,
                "From": source,
                "To": target
            })


            if st.button("📋 Copy Translation"):
                pyperclip.copy(translated)
                st.success("Copied to Clipboard!")

            st.download_button(
                label="⬇ Download Translation",
                data=translated,
                file_name="translation.txt",
                mime="text/plain"
            )
        except Exception as e:
            st.error(f"Error : {e}")


st.divider()

st.subheader("📜 Translation History")

if len(st.session_state.history) == 0:
    st.info("No translations yet.")

else:

    for item in reversed(st.session_state.history):

        with st.expander(f"{item['From']} ➜ {item['To']}"):

            st.write("**Original Text**")
            st.write(item["Input"])

            st.write("**Translated Text**")
            st.write(item["Output"])