import streamlit as st
from io import BytesIO

from streamlit_summarizer import summarize_pdf_file
from streamlit_transcription import transcript_pdf_file
# Import the ask_question function from the separate streamlit_chatbot module.
from streamlit_chatbot import ask_question
from streamlit_option_menu import option_menu

# # Inject custom CSS to fix the chat input at the bottom of the page
# st.markdown(
#     """
#     <style>
#     /* Fix the chat input to the bottom of the main content area */
#     [data-testid="stChatInput"] {
#         position: fixed;
#         bottom: 0;
#         left: 350px; /* Adjust to match your sidebar width */
#         width: calc(100% - 350px);
#         background-color: white;
#         z-index: 100;
#         padding: 10px;
#         border-top: 1px solid #e6e6e6;
#     }
    
#     /* Add bottom padding so chat history isn’t hidden behind the input */
#     [data-testid="stVerticalBlock"] {
#         padding-bottom: 70px;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )
# def main():
#     st.title("📘 PDF Summarizer & Chatbot")

#     # Sidebar: file uploader and mode selector
#     st.sidebar.header("📂 Upload PDF")
#     uploaded_file = st.sidebar.file_uploader("Choose a PDF", type="pdf")

#     # Add new mode: Read PDF Transcription
#     mode = st.sidebar.radio("Choose Mode", ["Summarize PDF", "Chat with PDF", "Read PDF Transcription"])

#     if uploaded_file:
#         if mode == "Summarize PDF":
#             st.subheader("📝 PDF Summary")
#             if st.button("Generate Summary"):
#                 with st.spinner("Summarizing with LLM..."):
#                     summary = summarize_pdf_file(uploaded_file, return_summary=True)
#                     st.success(summary)

#         elif mode == "Chat with PDF":
#             st.subheader("💬 Chat with PDF")
#             if "chat_history" not in st.session_state:
#                 st.session_state.chat_history = []
#             for msg in st.session_state.chat_history:
#                 with st.chat_message("user"):
#                     st.markdown(msg["user"])
#                 with st.chat_message("assistant"):
#                     st.markdown(msg["bot"])
#             user_input = st.chat_input("Ask a question about the PDF")
#             if user_input:
#                 with st.spinner("Processing your query..."):
#                     answer = ask_question(uploaded_file, user_input)
#                 st.session_state.chat_history.append({"user": user_input, "bot": answer})
#                 st.rerun()

#         elif mode == "Read PDF Transcription":
#             st.subheader("📄 PDF Transcription")
#             if st.button("Read PDF Text"):
#                 with st.spinner("Extracting text..."):
#                     raw_text = transcript_pdf_file(uploaded_file) #, return_summary=False)
#                     st.text_area("📄 Extracted Text", raw_text, height=400)

#     else:
#         if mode == "Summarize PDF":
#             st.info("Upload a PDF from the sidebar to generate a summary.")
#         elif mode == "Chat with PDF":
#             st.info("Upload a PDF from the sidebar to initiate a chat.")
#         elif mode == "Read PDF Transcription":
#             st.info("Upload a PDF from the sidebar to view the extracted text.")

# if __name__ == "__main__":
#     main()

# Custom CSS to fix the chat input at the bottom of the page
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

def main():
    st.title("📘 PDF Summarizer & Chatbot")

    # Sidebar: file uploader
    st.sidebar.header("📂 Upload PDF")
    uploaded_file = st.sidebar.file_uploader("Choose a PDF", type="pdf")

    # Use streamlit-option-menu for mode selection as attractive buttons.
    mode_options = ["Summarize PDF", "Chat with PDF", "Read PDF Transcription"]
    selected_mode = option_menu(
        menu_title=None,  # No header needed
        options=mode_options,
        icons=["card-text", "chat", "file-text"],
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important"},
            "icon": {"color": "black", "font-size": "18px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "center",
                "margin": "0px",
                "color": "black",
                "--hover-color": "#eee",
            },
            "nav-link-selected": {"background-color": "#02ab21", "color": "white"},
        }
    )
    st.session_state.mode = selected_mode

    # Use the selected mode to determine what to do.
    if uploaded_file:
        if st.session_state.mode == "Summarize PDF":
            st.subheader("📝 PDF Summary")
            if st.button("Generate Summary"):
                with st.spinner("Summarizing with LLM..."):
                    summary = summarize_pdf_file(uploaded_file, return_summary=True)
                    st.success(summary)

        elif st.session_state.mode == "Chat with PDF":
            st.subheader("💬 Chat with PDF")
            if "chat_history" not in st.session_state:
                st.session_state.chat_history = []
            # Display previous messages, if any
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

        elif st.session_state.mode == "Read PDF Transcription":
            st.subheader("📄 PDF Transcription")
            if st.button("Read PDF Text"):
                with st.spinner("Extracting text..."):
                    raw_text = transcript_pdf_file(uploaded_file)
                    st.text_area("📄 Extracted Text", raw_text, height=400)
    else:
        # Guides for when no PDF has been uploaded
        if st.session_state.mode == "Summarize PDF":
            st.info("Upload a PDF from the sidebar to generate a summary.")
        elif st.session_state.mode == "Chat with PDF":
            st.info("Upload a PDF from the sidebar to initiate a chat.")
        elif st.session_state.mode == "Read PDF Transcription":
            st.info("Upload a PDF from the sidebar to view the extracted text.")


if __name__ == "__main__":
    main()







