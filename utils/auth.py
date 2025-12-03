"""Authentication utilities for local password protection."""
import streamlit as st

# Hardcoded password: "saymyname"
PASSWORD_HASH = "$pbkdf2-sha256$29000$BMA4RwgBQAjhPAcgZGxtDQ$rEjfGFwkUDzF0eyrf90.0Rmy0C.CePqyxY4OEEAbtow"


def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        from passlib.hash import pbkdf2_sha256
        
        if pbkdf2_sha256.verify(st.session_state["password"], PASSWORD_HASH):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store password
        else:
            st.session_state["password_correct"] = False

    # Return True if the password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password.
    st.markdown("### 🔐 Personal Dashboard Login")
    st.text_input(
        "Password", 
        type="password", 
        on_change=password_entered, 
        key="password"
    )
    
    if "password_correct" in st.session_state and not st.session_state["password_correct"]:
        st.error("😕 Password incorrect")
    
    return False


def logout():
    """Clear the authentication state."""
    st.session_state["password_correct"] = False
