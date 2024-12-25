import nltk
from modules.Check_API import check_openai_api_key
from modules.Main import proceed, get_user
from modules.Update_User_Details import update_details
import streamlit as st
import warnings
from modules.Login_UI import login_ui
import openai
from openai import OpenAI, OpenAIError

st.set_page_config(page_title="BlogBotter 💬 ", initial_sidebar_state="auto")
st.title("BlogBotter 💬 ")

# nltk.download("stopwords")
# nltk.download("wordnet")
warnings.filterwarnings("ignore")

if "user" not in st.session_state:
    st.session_state.user = ""


def check(model, api):
    try:
        val = model == "GPT4" and check_openai_api_key(api)
        if val:
            st.session_state.proceed_disabled = False
        else:
            st.session_state.proceed_disabled = True
            st.session_state.verify_disabled = True
    except OpenAIError as e:
        st.session_state.proceed_disabled = True
        st.session_state.verify_disabled = True
        # print(e)


def refresh():
    st.session_state.verify_disabled = False
    st.session_state.proceed_disabled = not (
        wordpress_url == ""
        or wordpress_pass == ""
        or wordpress_user == ""
        or check(select_model, api)
    )


LOGGED_IN = login_ui()

if LOGGED_IN[0]:
    username = LOGGED_IN[1]
    st.session_state.user = get_user(username)

    try:
        first_login = st.session_state.user["First_Login"]
    except:
        first_login = True

    if first_login:
        # invalid_api = True

        # if "verify_disabled" not in st.session_state:
        #     st.session_state.verify_disabled = True
        # if "proceed_disabled" not in st.session_state:
        #     st.session_state.proceed_disabled = True

        wordpress_user = st.text_input(
            "WordPress Username:",
            placeholder="Type your WordPress Username...",
        )
        wordpress_pass = st.text_input(
            "WordPress Passoword:",
            placeholder="Type your WordPress Password...",
        )
        wordpress_url = st.text_input(
            "WordPress URL:",
            placeholder="Type your WordPress Site Link...",
        )

        select_model = st.selectbox("Please select your model:", ["gpt-4", "Gemini"])
        api = st.text_input(
            "Please enter your API key",
            placeholder="API",
            # on_change=refresh
        )

        new_dt = [{
            "Wordpress": {
                "WP_USER": wordpress_user,
                "WP_URL": wordpress_url,
                "WP_PASS": wordpress_pass,
            },
            "Models": {"Model_Name": select_model, "Model": select_model, "API": api},
        }]

        # new_dt = [{
        #     "WP_USER": wordpress_user,
        #     "WP_URL": wordpress_url,
        #     "WP_PASS": wordpress_pass,
        #     "Model_Name": select_model,
        #     "Model": select_model,
        #     "API": api,
        # }]
        # print(new_dt[0])

        c1, c2 = st.columns(2)
        with c1:
            st.button(
                "Verify",
                # on_click=check,
                args=(select_model, api),
                use_container_width=True,
                # disabled=st.session_state.verify_disabled,
            )

        with c2:
            st.button(
                "Proceed",
                on_click=update_details,
                args=(new_dt),
                # disabled=st.session_state.proceed_disabled,
                use_container_width=True,
            )
    else:
        proceed()
