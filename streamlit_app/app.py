# import streamlit as st
# import pdfplumber
# import base64
# import io

# # Function to extract text from PDF
# def extract_text_from_pdf(file):
#     text = ""
#     with pdfplumber.open(file) as pdf:
#         for page in pdf.pages:
#             page_text = page.extract_text()
#             if page_text:
#                 text += page_text + "\n"
#     return text.strip()

# # Simple summarizer (first few lines)
# def summarize_text(text, max_lines=5):
#     lines = text.split('\n')
#     summary = "\n".join(lines[:max_lines])
#     return summary.strip()

# # Simple chatbot logic
# def chat_with_pdf(query, text):
#     if query.lower() in text.lower():
#         return f"Found: \"{query}\" in PDF.\n\n{text[:500]}..."
#     else:
#         return "Sorry, no relevant info found in the PDF."

# # Embed PDF using iframe
# def embed_pdf(file_bytes):
#     base64_pdf = base64.b64encode(file_bytes).decode('utf-8')
#     pdf_display = (
#         f'<iframe src="data:application/pdf;base64,{base64_pdf}" '
#         f'width="100%" height="800" allowfullscreen></iframe>'
#     )
#     return pdf_display

# def main():
#     st.set_page_config(layout="wide")
#     st.title("📘 PDF Viewer, Summarizer & Chatbot")

#     st.sidebar.header("📂 Upload PDF")
#     uploaded_file = st.sidebar.file_uploader("Choose a PDF", type="pdf")

#     if uploaded_file:
#         file_bytes = uploaded_file.getvalue()
#         full_text = extract_text_from_pdf(io.BytesIO(file_bytes))

#         if 'chat_history' not in st.session_state:
#             st.session_state.chat_history = []

#         mode = st.sidebar.radio("Choose Mode", ["Summarize PDF", "Chat with PDF"])

#         left_col, right_col = st.columns([1.2, 1.8])

#         with right_col:
#             st.subheader("📄 PDF Viewer")
#             st.markdown(embed_pdf(file_bytes), unsafe_allow_html=True)

#         with left_col:
#             if mode == "Summarize PDF":
#                 st.subheader("📝 PDF Summary")
#                 summary = summarize_text(full_text)
#                 st.success(summary)

#             elif mode == "Chat with PDF":
#                 st.subheader("💬 Chat with PDF")

#                 # Display chat history
#                 for msg in st.session_state.chat_history:
#                     with st.chat_message("user"):
#                         st.markdown(msg["user"])
#                     with st.chat_message("assistant"):
#                         st.markdown(msg["bot"])

#                 # Chat input at bottom of left column
#                 user_input = st.chat_input("Ask a question about the PDF")
#                 if user_input:
#                     response = chat_with_pdf(user_input, full_text)
#                     st.session_state.chat_history.append({"user": user_input, "bot": response})
#                     st.rerun()  # Re-render chat immediately

#     else:
#         st.info("Upload a PDF from the sidebar to begin.")

# if __name__ == "__main__":
#     main()

########################### Above is Version-1 #####################################################################


############################ Below is version - 2###################################################################


# import streamlit as st
# import pdfplumber
# import io

# from streamlit_summarizer import summarize_pdf_file
# from streamlit_chatbot import RAGPipeline

# # Function to extract text from PDF
# def extract_text_from_pdf(file):
#     text = ""
#     with pdfplumber.open(file) as pdf:
#         for page in pdf.pages:
#             page_text = page.extract_text()
#             if page_text:
#                 text += page_text + "\n"
#     return text.strip()

# def extract_text_from_pdf(file):
#     documents = RAGPipeline.load_pdf(file)
#     return "\n".join([doc.page_content for doc in documents])

# # Simple chatbot logic
# def chat_with_pdf(query, text):
#     if query.lower() in text.lower():
#         return f"Found: \"{query}\" in PDF.\n\n{text[:500]}..."
#     else:
#         return "Sorry, no relevant info found in the PDF."

# def main():
#     st.set_page_config(layout="wide")
#     st.title("📘 PDF Summarizer & Chatbot")

#     # Inject custom CSS to make chat input fixed at the bottom of the page
#     st.markdown(
#         """
#         <style>
#         /* Fix the chat input to the bottom of the main content area */
#         [data-testid="stChatInput"] {
#             position: fixed;
#             bottom: 0;
#             left: 350px; /* Adjust this value to match your sidebar width */
#             width: calc(100% - 350px); /* Ensures the input stays within screen bounds */
#             background-color: white;
#             z-index: 100;
#             padding: 10px;
#             border-top: 1px solid #e6e6e6;
#         }
    
#         /* Add extra bottom padding on the main vertical block so that chat history isn't hidden */
#         [data-testid="stVerticalBlock"] {
#             padding-bottom: 70px;
#         }
#         </style>
#         """, unsafe_allow_html=True
#     )

#     # Sidebar for file upload and mode selection
#     st.sidebar.header("📂 Upload PDF")
#     uploaded_file = st.sidebar.file_uploader("Choose a PDF", type="pdf")
    
#     # Move the mode selection outside of the file-upload condition.
#     mode = st.sidebar.radio("Choose Mode", ["Summarize PDF", "Chat with PDF"])

#     # Prepare main panel content
#     left_col = st.columns([1.0])[0]  # Only one column for the content (left column)
#     with left_col:
#         if uploaded_file:
#             file_bytes = uploaded_file.getvalue()
#             full_text = extract_text_from_pdf(io.BytesIO(file_bytes))
            
#             # Initialize chat history if not already in session state
#             if 'chat_history' not in st.session_state:
#                 st.session_state.chat_history = []
            
#             # if mode == "Summarize PDF":
#             #     st.subheader("📝 PDF Summary")
#             #     summary = summarize_text(full_text)
#             #     st.success(summary)

#             # Summarize PDF using LLM
#             if mode == "Summarize PDF":
#                 st.subheader("📝 PDF Summary")
#                 if st.button("Generate Summary"):
#                     with st.spinner("Summarizing with LLM..."):
#                         summary = summarize_pdf_file(uploaded_file)
#                         st.success(summary)

#             elif mode == "Chat with PDF":
#                 st.subheader("💬 Chat with PDF")
                
#                 # Display chat history
#                 for msg in st.session_state.chat_history:
#                     with st.chat_message("user"):
#                         st.markdown(msg["user"])
#                     with st.chat_message("assistant"):
#                         st.markdown(msg["bot"])
                
#                 # Chat input at the bottom (this is now fixed using CSS)
#                 user_input = st.chat_input("Ask a question about the PDF")
#                 if user_input:
#                     response = chat_with_pdf(user_input, full_text)
#                     st.session_state.chat_history.append({"user": user_input, "bot": response})
#                     st.rerun()  # Re-render chat immediately
#         else:
#             # When no file is uploaded, you'll still see the mode selector at the sidebar.
#             # In the main area, display contextual hints based on the selected mode.
#             if mode == "Summarize PDF":
#                 st.info("Upload a PDF from the sidebar to generate a summary.")
#             elif mode == "Chat with PDF":
#                 st.info("Upload a PDF from the sidebar to initiate chat.")

# if __name__ == "__main__":
#     main()

###################### Version -2 is Above #############################

###################### Version -3 is Below ##############################

# import streamlit as st
# import pdfplumber
# import io

# from streamlit_summarizer import summarize_pdf_file
# from streamlit_chatbot import RAGPipeline

# # Function to extract text from PDF
# def extract_text_from_pdf(file):
#     text = ""
#     with pdfplumber.open(file) as pdf:
#         for page in pdf.pages:
#             page_text = page.extract_text()
#             if page_text:
#                 text += page_text + "\n"
#     return text.strip()

# def extract_text_from_pdf(file):
#     documents = RAGPipeline.load_pdf(file)
#     return "\n".join([doc.page_content for doc in documents])

# # Simple chatbot logic
# def chat_with_pdf(query, text):
#     if query.lower() in text.lower():
#         return f"Found: \"{query}\" in PDF.\n\n{text[:500]}..."
#     else:
#         return "Sorry, no relevant info found in the PDF."

# def main():
#     st.set_page_config(layout="wide")
#     st.title("📘 PDF Summarizer & Chatbot")

#     # Inject custom CSS to make chat input fixed at the bottom of the page
#     st.markdown(
#         """
#         <style>
#         /* Fix the chat input to the bottom of the main content area */
#         [data-testid="stChatInput"] {
#             position: fixed;
#             bottom: 0;
#             left: 350px; /* Adjust this value to match your sidebar width */
#             width: calc(100% - 350px); /* Ensures the input stays within screen bounds */
#             background-color: white;
#             z-index: 100;
#             padding: 10px;
#             border-top: 1px solid #e6e6e6;
#         }
    
#         /* Add extra bottom padding on the main vertical block so that chat history isn't hidden */
#         [data-testid="stVerticalBlock"] {
#             padding-bottom: 70px;
#         }
#         </style>
#         """, unsafe_allow_html=True
#     )

#     # Sidebar for file upload and mode selection
#     st.sidebar.header("📂 Upload PDF")
#     uploaded_file = st.sidebar.file_uploader("Choose a PDF", type="pdf")
    
#     # Move the mode selection outside of the file-upload condition.
#     mode = st.sidebar.radio("Choose Mode", ["Summarize PDF", "Chat with PDF"])

#     # Prepare main panel content
#     left_col = st.columns([1.0])[0]  # Only one column for the content (left column)
#     with left_col:
#         if uploaded_file:
#             file_bytes = uploaded_file.getvalue()
#             full_text = extract_text_from_pdf(io.BytesIO(file_bytes))
            
#             # Initialize chat history if not already in session state
#             if 'chat_history' not in st.session_state:
#                 st.session_state.chat_history = []
            
#             # if mode == "Summarize PDF":
#             #     st.subheader("📝 PDF Summary")
#             #     summary = summarize_text(full_text)
#             #     st.success(summary)

#             # Summarize PDF using LLM
#             if mode == "Summarize PDF":
#                 st.subheader("📝 PDF Summary")
#                 if st.button("Generate Summary"):
#                     with st.spinner("Summarizing with LLM..."):
#                         summary = summarize_pdf_file(uploaded_file)
#                         st.success(summary)

#             elif mode == "Chat with PDF":
#                 st.subheader("💬 Chat with PDF")
                
#                 # Display chat history
#                 for msg in st.session_state.chat_history:
#                     with st.chat_message("user"):
#                         st.markdown(msg["user"])
#                     with st.chat_message("assistant"):
#                         st.markdown(msg["bot"])
                
#                 # Chat input at the bottom (this is now fixed using CSS)
#                 user_input = st.chat_input("Ask a question about the PDF")
#                 if user_input:
#                     response = chat_with_pdf(user_input, full_text)
#                     st.session_state.chat_history.append({"user": user_input, "bot": response})
#                     st.rerun()  # Re-render chat immediately
#         else:
#             # When no file is uploaded, you'll still see the mode selector at the sidebar.
#             # In the main area, display contextual hints based on the selected mode.
#             if mode == "Summarize PDF":
#                 st.info("Upload a PDF from the sidebar to generate a summary.")
#             elif mode == "Chat with PDF":
#                 st.info("Upload a PDF from the sidebar to initiate chat.")

# if __name__ == "__main__":
#     main()

import streamlit as st
from io import BytesIO

from streamlit_summarizer import summarize_pdf_file
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

def main():
    st.title("📘 PDF Summarizer & Chatbot")

    # Sidebar: file uploader and mode selector
    st.sidebar.header("📂 Upload PDF")
    uploaded_file = st.sidebar.file_uploader("Choose a PDF", type="pdf")
    
    mode = st.sidebar.radio("Choose Mode", ["Summarize PDF", "Chat with PDF"])

    if uploaded_file:
        if mode == "Summarize PDF":
            st.subheader("📝 PDF Summary")
            if st.button("Generate Summary"):
                with st.spinner("Summarizing with LLM..."):
                    summary = summarize_pdf_file(uploaded_file)
                    st.success(summary)

        elif mode == "Chat with PDF":
            st.subheader("💬 Chat with PDF")
            
            # Initialize chat history if not already in session state.
            if "chat_history" not in st.session_state:
                st.session_state.chat_history = []
            
            # Display the existing chat history.
            for msg in st.session_state.chat_history:
                with st.chat_message("user"):
                    st.markdown(msg["user"])
                with st.chat_message("assistant"):
                    st.markdown(msg["bot"])
            
            # Chat input widget (with custom CSS, the chat input is fixed at the bottom).
            user_input = st.chat_input("Ask a question about the PDF")
            if user_input:
                with st.spinner("Processing your query..."):
                    # Pass the uploaded PDF (a file-like object) and the question to the ask_question function.
                    answer = ask_question(uploaded_file, user_input)
                # Save the Q&A in the session state.
                st.session_state.chat_history.append({"user": user_input, "bot": answer})
                st.rerun()
    else:
        # When no file has been uploaded.
        if mode == "Summarize PDF":
            st.info("Upload a PDF from the sidebar to generate a summary.")
        elif mode == "Chat with PDF":
            st.info("Upload a PDF from the sidebar to initiate a chat.")




# def main():
#     st.set_page_config(layout="wide")
#     st.title("📘 PDF Summarizer & Chatbot")

#     st.sidebar.header("📂 Upload PDF")
#     uploaded_file = st.sidebar.file_uploader("Choose a PDF", type="pdf")
    
#     mode = st.sidebar.radio("Choose Mode", ["Summarize PDF", "Chat with PDF"])
    
#     if uploaded_file:
#         if mode == "Summarize PDF":
#             st.subheader("📝 PDF Summary")
#             if st.button("Generate Summary"):
#                 with st.spinner("Summarizing with LLM..."):
#                     # The summarize_pdf_file function reads the uploaded file directly.
#                     summary = summarize_pdf_file(uploaded_file)
#                     st.success(summary)
                    
#         elif mode == "Chat with PDF":
#             st.subheader("💬 Chat with PDF")
#             # Initialize chat history if not already set in session state
#             if 'chat_history' not in st.session_state:
#                 st.session_state.chat_history = []

#             # Display the existing chat history
#             for msg in st.session_state.chat_history:
#                 with st.chat_message("user"):
#                     st.markdown(msg["user"])
#                 with st.chat_message("assistant"):
#                     st.markdown(msg["bot"])

#             # Chat input using the new st.chat_input widget (fixed by our CSS)
#             user_input = st.chat_input("Ask a question about the PDF")
#             if user_input:
#                 with st.spinner("Processing your query..."):
#                     # Since the uploaded_file may have been read already, use getvalue() to pass a fresh stream.
#                     file_bytes = uploaded_file.getvalue()
#                     # Wrap the bytes into a BytesIO object so that ask_question can treat it as a file-like object.
#                     pdf_file = BytesIO(file_bytes)
#                     answer = ask_question(pdf_file, user_input)
#                 # Append the Q&A to the chat history and re-run the app
#                 st.session_state.chat_history.append({
#                     "user": user_input,
#                     "bot": answer
#                 })
#                 st.rerun()
#     else:
#         # No file uploaded: display appropriate instructions
#         if mode == "Summarize PDF":
#             st.info("Upload a PDF from the sidebar to generate a summary.")
#         elif mode == "Chat with PDF":
#             st.info("Upload a PDF from the sidebar to initiate a chat.")


if __name__ == "__main__":
    main()









