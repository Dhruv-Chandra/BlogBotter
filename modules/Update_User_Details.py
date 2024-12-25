import json
from modules.Main import proceed, get_user
import streamlit as st


# @st.cache_data
def update_details(new_details):
    user = st.session_state.user

    file_path = "_secret_auth_.json"
    with open(file_path, "r+") as file:
        data = json.load(file)

        # Find the user with the specified ID
        user_found = False
        for saved_user in data:
            if saved_user["username"] == user["username"]:
                saved_user.update(new_details)
                saved_user["First_Login"] = False
                user_found = True
                break

        if not user_found:
            print(user)
            print(f"User with ID not found.")
        else:
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()
            st.session_state.user = get_user(user["username"])

            proceed()
