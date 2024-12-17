import json
import re
import time
import gspread
import streamlit as st
from streamlit_option_menu import option_menu
from oauth2client.service_account import ServiceAccountCredentials


@st.cache_resource
def get_gsheet_client():
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    
    gcloud_creds = json.loads(st.secrets["google_cloud"]["sheets_api_creds"])

    creds = ServiceAccountCredentials.from_json_keyfile_dict(
        gcloud_creds, scope)
    return gspread.authorize(creds)


def get_articles():
    client = get_gsheet_client()
    sheet = client.open("Streamlit Article 101").sheet1
    records = sheet.get_all_records()
    print(records)
    print(type(records))
    return records

@st.cache_resource
def get_articles_cache():
    return get_articles()

def save_article(title, author, content):
    ...


def show_article():
    st.session_state.display_article = article
    if tab == "Write":
        st.sidebar.info("Please switch to the 'Read' tab to view the article")

def update_preview():
    st.session_state.preview_article = st.session_state.input_article

@st.dialog("Save Article")
def save_article_dialog():
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


st.set_page_config("Article 101", page_icon=":newspaper:", layout="wide")

# get_articles_cache()

if "articles" not in st.session_state:
    st.session_state.articles = get_articles_cache()

# sidebar
st.sidebar.title("Articles")
if "display_article" not in st.session_state:
    st.session_state.display_article = st.session_state.articles[0]["Id"]

for article in st.session_state.articles:
    if st.sidebar.button(article["Title"], key=article["Id"], type="tertiary", use_container_width=True, on_click=show_article):
        st.session_state.display_article = article["Id"]

if "preview_article" not in st.session_state:
    st.session_state.preview_article = ""

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

    container.columns([1, 1, 1])[1].button("Save", key="save_article", type="primary", use_container_width=True, disabled=bool(not (st.session_state.input_article and title)),  on_click=save_article_dialog)