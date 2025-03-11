```python
import streamlit as st
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
import os
import json

# Google OAuth2 yapılandırması
SCOPES = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
    'https://www.googleapis.com/auth/datastore'
]

def init_google_auth():
    if 'google_credentials' not in st.session_state:
        st.session_state.google_credentials = None
    if 'user_email' not in st.session_state:
        st.session_state.user_email = None

def login_page():
    st.title("Özel Ders Yönetim Sistemi")
    
    if not st.session_state.google_credentials:
        st.write("Devam etmek için Google hesabınızla giriş yapın")
        
        if st.button("Google ile Giriş Yap"):
            try:
                flow = Flow.from_client_secrets_file(
                    'client_secrets.json',
                    scopes=SCOPES,
                    redirect_uri='urn:ietf:wg:oauth:2.0:oob'
                )
                
                auth_url, _ = flow.authorization_url(prompt='consent')
                st.markdown(f"[Google Hesabınızla Giriş Yapın]({auth_url})")
                
                auth_code = st.text_input("Yetkilendirme kodunu yapıştırın:")
                if auth_code:
                    flow.fetch_token(code=auth_code)
                    credentials = flow.credentials
                    st.session_state.google_credentials = credentials
                    st.experimental_rerun()
                    
            except Exception as e:
                st.error(f"Giriş yapılırken bir hata oluştu: {str(e)}")
        
        return False
    
    return True

def is_authenticated():
    return st.session_state.google_credentials is not None
```
