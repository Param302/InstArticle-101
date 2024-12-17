from click import style
import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config("Instant Article", page_icon=":newspaper:", layout="wide")

# sidebar
st.sidebar.title("Articles")
articles = ["Article 1", "Article 2", "Article 3"]
if "display_article" not in st.session_state:
    st.session_state.display_article = articles[0]

for article in articles:
    if st.sidebar.button(article, key=article, use_container_width=True):
        st.session_state.display_article = article

tab = option_menu(
    "Instant Article", 
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
    container.write("Write article here")