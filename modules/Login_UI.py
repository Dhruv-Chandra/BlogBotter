from streamlit_login_auth_ui.widgets import __login__
import streamlit as st


def login_ui():
    __login__obj = __login__(
        auth_token="courier_auth_token",
        company_name="BlogBotter",
        width=200,
        height=250,
        logout_button_name="Logout",
        hide_menu_bool=False,
        hide_footer_bool=False,
        lottie_url="https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json",
        
    )

    return (__login__obj.build_login_ui(), __login__obj.get_username())