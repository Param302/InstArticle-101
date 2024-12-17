import time
from click import style
import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config("Article 101", page_icon=":newspaper:", layout="wide")

# sidebar
st.sidebar.title("Articles")
articles = ["Article 1", "Article 2", "Article 3"]
if "display_article" not in st.session_state:
    st.session_state.display_article = articles[0]

for article in articles:
    if st.sidebar.button(article, key=article, type="tertiary", use_container_width=True):
        st.session_state.display_article = article

if "preview_article" not in st.session_state:
    st.session_state.preview_article = ""
def update_preview():
    st.session_state.preview_article = st.session_state.input_article

@st.dialog("Save Article")
def save_article():
    status = st.empty()
    st.write(f'Are you sure want to save the article titled "**{title}**"?')
    code = st.text_input("Enter secret code")
    yes, no = st.columns([1, 1])
    if yes.button("Yes", type="primary", use_container_width=True):
        if code == "1234":
            status.info("Saving article...")
        elif code and code != "1234":
            status.error("Invalid secret code")
    if no.button("No", use_container_width=True):
        status.warning("Article not saved")
        time.sleep(2)
        st.rerun()

tab = option_menu(
    "Article 101", 
    options=["Read", "Write"], 
    icons=["book", "pencil"], 
    orientation="horizontal",
    styles={
        "menu-title": {
            "width": "100%", 
            "display": "flex", 
            "justify-content": "center"
            }
    }
)

if tab=="Read":
    container = st.container(border=True)
    container.write("Read article here")
    container.header(st.session_state.display_article)
else:
    container = st.container(border=True)
    container.columns([1, 1, 1])[1].header("Write article here")
    # title = container.columns([1, 1])[0].text_input("**Title**", key="title")
    editor, preview = container.columns([1, 1])

    with editor.container():
        st.subheader("Editor")
        tt, at = st.columns([2, 1])

        title = tt.text_input("**Title**", key="title")
        author = at.text_input("**Your Name**", key="author")
        st.text_area("Write here",
                     label_visibility="collapsed",
                     height=500,
                     key="input_article", on_change=update_preview)

    with preview.container():
        st.subheader("Preview")
        st.header(title)
        st.markdown(st.session_state.input_article, unsafe_allow_html=True)

    container.columns([1, 1, 1])[1].button("Save", key="save_article", type="primary", use_container_width=True, disabled=bool(not (st.session_state.input_article and title)),  on_click=save_article)