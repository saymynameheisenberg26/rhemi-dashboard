"""Authentication utilities for local password protection."""
import os
from passlib.hash import pbkdf2_sha256
from dotenv import load_dotenv
import streamlit as st

load_dotenv()


def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        # Try to get password hash from .env first, then from Streamlit secrets
        password_hash = os.getenv("PASSWORD_HASH")
        
        # If not in .env, try Streamlit secrets
        if not password_hash and hasattr(st, 'secrets'):
            try:
                password_hash = st.secrets.get("PASSWORD_HASH")
            except:
                pass
        
        if not password_hash:
            st.error("❌ No password hash found. Please set PASSWORD_HASH in .env or Streamlit secrets.")
            return
        
        if pbkdf2_sha256.verify(st.session_state["password"], password_hash):
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
    
    st.markdown("---")
    st.caption("💡 First time? Generate a password hash with:")
    st.code("python3 -c \"from passlib.hash import pbkdf2_sha256; print(pbkdf2_sha256.hash('your_password'))\"")
    
    return False


def logout():
    """Clear the authentication state."""
    st.session_state["password_correct"] = False
