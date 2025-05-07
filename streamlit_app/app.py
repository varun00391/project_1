import streamlit as st
from io import BytesIO

from streamlit_summarizer import summarize_pdf_file
from streamlit_transcription import transcript_pdf_file
# Import the ask_question function from the separate streamlit_chatbot module.
from streamlit_chatbot import ask_question

# Inject custom CSS to fix the chat input at the bottom of the page
st.markdown(
    """
    <style>
    /* Fix the chat input to the bottom of the main content area */
    [data-testid="stChatInput"] {
        position: fixed;
        bottom: 0;
        left: 350px; /* Adjust to match your sidebar width */
        width: calc(100% - 350px);
        background-color: white;
        z-index: 100;
        padding: 10px;
        border-top: 1px solid #e6e6e6;
    }
    
    /* Add bottom padding so chat history isn’t hidden behind the input */
    [data-testid="stVerticalBlock"] {
        padding-bottom: 70px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# def main():
#     st.title("📘 PDF Summarizer & Chatbot")

#     # Sidebar: file uploader and mode selector
#     st.sidebar.header("📂 Upload PDF")
#     uploaded_file = st.sidebar.file_uploader("Choose a PDF", type="pdf")
    
#     mode = st.sidebar.radio("Choose Mode", ["Summarize PDF", "Chat with PDF","PDF Transcription"])

#     if uploaded_file:
#         if mode == "Summarize PDF":
#             st.subheader("📝 PDF Summary")
#             if st.button("Generate Summary"):
#                 with st.spinner("Summarizing with LLM..."):
#                     summary = summarize_pdf_file(uploaded_file)
#                     st.success(summary)

#         elif mode == "Chat with PDF":
#             st.subheader("💬 Chat with PDF")
            
#             # Initialize chat history if not already in session state.
#             if "chat_history" not in st.session_state:
#                 st.session_state.chat_history = []
            
#             # Display the existing chat history.
#             for msg in st.session_state.chat_history:
#                 with st.chat_message("user"):
#                     st.markdown(msg["user"])
#                 with st.chat_message("assistant"):
#                     st.markdown(msg["bot"])
            
#             # Chat input widget (with custom CSS, the chat input is fixed at the bottom).
#             user_input = st.chat_input("Ask a question about the PDF")
#             if user_input:
#                 with st.spinner("Processing your query..."):
#                     # Pass the uploaded PDF (a file-like object) and the question to the ask_question function.
#                     answer = ask_question(uploaded_file, user_input)
#                 # Save the Q&A in the session state.
#                 st.session_state.chat_history.append({"user": user_input, "bot": answer})
#                 st.rerun()

#         elif mode == "Read PDF Transcription":
#             st.subheader("📄 PDF Transcription")
#             if st.button("Read PDF Text"):
#                 with st.spinner("Extracting text..."):
#                     raw_text = transcript_pdf_file(uploaded_file)
#                     st.text_area("📄 Extracted Text", raw_text, height=400)
#     else:
#         # When no file has been uploaded.
#         if mode == "Summarize PDF":
#             st.info("Upload a PDF from the sidebar to generate a summary.")
#         elif mode == "Chat with PDF":
#             st.info("Upload a PDF from the sidebar to initiate a chat.")
#         elif mode == "Read PDF Transcription":
#             st.info("Upload a PDF from sidebar to extract pdf text")

# if __name__ == "__main__":
#     main()

def main():
    st.title("📘 PDF Summarizer & Chatbot")

    # Sidebar: file uploader and mode selector
    st.sidebar.header("📂 Upload PDF")
    uploaded_file = st.sidebar.file_uploader("Choose a PDF", type="pdf")

    # Add new mode: Read PDF Transcription
    mode = st.sidebar.radio("Choose Mode", ["Summarize PDF", "Chat with PDF", "Read PDF Transcription"])

    if uploaded_file:
        if mode == "Summarize PDF":
            st.subheader("📝 PDF Summary")
            if st.button("Generate Summary"):
                with st.spinner("Summarizing with LLM..."):
                    summary = summarize_pdf_file(uploaded_file, return_summary=True)
                    st.success(summary)

        elif mode == "Chat with PDF":
            st.subheader("💬 Chat with PDF")
            if "chat_history" not in st.session_state:
                st.session_state.chat_history = []
            for msg in st.session_state.chat_history:
                with st.chat_message("user"):
                    st.markdown(msg["user"])
                with st.chat_message("assistant"):
                    st.markdown(msg["bot"])
            user_input = st.chat_input("Ask a question about the PDF")
            if user_input:
                with st.spinner("Processing your query..."):
                    answer = ask_question(uploaded_file, user_input)
                st.session_state.chat_history.append({"user": user_input, "bot": answer})
                st.rerun()

        elif mode == "Read PDF Transcription":
            st.subheader("📄 PDF Transcription")
            if st.button("Read PDF Text"):
                with st.spinner("Extracting text..."):
                    raw_text = transcript_pdf_file(uploaded_file) #, return_summary=False)
                    st.text_area("📄 Extracted Text", raw_text, height=400)

    else:
        if mode == "Summarize PDF":
            st.info("Upload a PDF from the sidebar to generate a summary.")
        elif mode == "Chat with PDF":
            st.info("Upload a PDF from the sidebar to initiate a chat.")
        elif mode == "Read PDF Transcription":
            st.info("Upload a PDF from the sidebar to view the extracted text.")

if __name__ == "__main__":
    main()









