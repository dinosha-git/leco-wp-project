import os
import re
import streamlit as st
from supabase import create_client, Client

import os, streamlit as st
from dotenv import load_dotenv
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL") or st.secrets.get("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY") or st.secrets.get("SUPABASE_ANON_KEY")


# --- CONFIG (use environment vars in production) ---
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://sjdusfgwmtwaidkxaptx.supabase.co")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNqZHVzZmd3bXR3YWlka3hhcHR4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTk0ODA3OTcsImV4cCI6MjA3NTA1Njc5N30.vB_MRn9layy2TovYqUOaCX1cd0KRCewlUtJq_Jog5SE")

st.set_page_config(page_title="Simple Form", page_icon="📝", layout="centered")

# --- INIT SUPABASE ---
@st.cache_resource
def get_client() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

supabase = get_client()

#st.set_page_config(page_title="Simple Form", page_icon="📝", layout="centered")
st.title("📝 Example Submission Form")

with st.form("submission_form", clear_on_submit=False):
    full_name = st.text_input("Full name", placeholder="Jane Doe")
    email = st.text_input("Email", placeholder="jane@example.com")
    age = st.number_input("Age (optional)", min_value=0, max_value=120, step=1)
    feedback = st.text_area("Feedback (optional)", placeholder="Tell us anything...")
    submitted = st.form_submit_button("Submit")

def valid_email(s: str) -> bool:
    return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", s))

if submitted:
    # Basic validation
    if not full_name.strip():
        st.error("Full name is required.")
    elif not valid_email(email):
        st.error("Please provide a valid email.")
    else:
        try:
            row = {
                "full_name": full_name.strip(),
                "email": email.strip().lower(),
                "age": int(age) if age else None,
                "feedback": feedback.strip() if feedback else None,
            }
            resp = supabase.table("submissions").insert(row).execute()
            if resp.data:
                st.success("✅ Submitted successfully!")
                st.json(resp.data[0])  # show the inserted row briefly
            else:
                st.warning("Submission completed, but no data returned.")
        except Exception as e:
            st.error(f"❌ Error saving to database: {e}")

st.markdown("---")
st.caption("Powered by Streamlit + Supabase (Postgres).")
