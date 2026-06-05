import streamlit as st
from pypdf import PdfReader
from google import genai

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="AI Resume Roaster", page_icon="🔥", layout="centered")

st.title("🔥 The Brutal AI Resume Roaster")
st.write("Upload your resume if you dare. Get a brutal roast and an honest score.")

# --- STAGE 1: READ PDF FUNCTION ---
def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    full_text = ""
    for page in reader.pages:
        text = page.extract_text()
        if text:
            full_text += text + "\n"
    return full_text

# --- STAGE 2 & 3: TALK TO AI ---
def ask_ai_to_roast(resume_text, api_key):
    try:
        client = genai.Client(api_key=api_key)
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=f"""
            You are a hilarious, highly sarcastic tech recruiter who roasts resumes. 
            Read the following resume text, give it a funny but brutally honest roast, 
            rate it out of 100, and then provide 3 simple bullet points on how to make it better.
            
            Resume text:
            {resume_text}
            """
        )
        return response.text
    except Exception as e:
        return f"❌ API Error: {str(e)}"

# --- STREAMLIT USER INTERFACE ---
# Put your working API key here inside the quotes!
MY_API_KEY = "AQ.Ab8RN6Ip6XHFfjJWxJQEGgdGntUqkPqmXjxBquuCf2B8dcvn7g"

uploaded_file = st.file_uploader("Choose your resume PDF file", type=["pdf"])

if uploaded_file is not None:
    st.success("PDF Uploaded Successfully!")
    
    if st.button("🔥 ROAST MY RESUME!"):
        with st.spinner("Recruiter is laughing at your formatting... please wait..."):
            # 1. Extract text from the newly uploaded file
            text_data = extract_text_from_pdf(uploaded_file)
            
            # 2. Get the roast from AI
            roast_result = ask_ai_to_roast(text_data, MY_API_KEY)
            
            # 3. Display the result in a nice box
            st.markdown("### 🤖 The Recruiter's Verdict:")
            st.info(roast_result)
            
if __name__ == "__main__":
    import streamlit.web.cli as stcli, sys
    sys.argv = ["streamlit", "run", __file__]
    sys.exit(stcli.main())
