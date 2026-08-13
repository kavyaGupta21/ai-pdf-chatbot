import gradio as gr 

from rag import(
        build_vector_store,
        retrieve_documents,
        generate_answer,
        rewrite_question
    ) 



vector_store=None





def process_pdf(pdf_file):
    global vector_store

    if pdf_file is None:
        return "Please upload as pdf.",[]

        
    vector_store=build_vector_store(pdf_file)

    return "PDF processed succesfully.",[]

    

def ask_question(question,history):
    if vector_store is None:
        return history, "Please upload and process a pdf first"
    if not question.strip():
        return history, "please entera question"
    search_question=rewrite_question(
        question,
        history
    )
    print("Original question:",question)
    print("Reasked question:",search_question)
    relevant_results=retrieve_documents(
        vector_store,
        search_question
    )
    if relevant_results is None:
        answer="I could not find the answer to your question in the pdf."
    else:
        answer=generate_answer(
            search_question,
            relevant_results
        )    
    history.append({
        "role":"user",
        "content":question
    })
    history.append({
        "role":"assistant",
        "content":answer
    })
    return history,""

css = """
/* ================================
   PAGE
================================ */

body {
    background: #f7f8fa !important;
}

.gradio-container {
    max-width: 1450px !important;
    width: 95% !important;
    margin: auto !important;
    padding: 25px 20px !important;
}


/* ================================
   HEADER
================================ */

#title {
    text-align: center;
    font-size: 34px !important;
    font-weight: 700 !important;
    color: #111827 !important;
    margin-bottom: 5px;
}

#subtitle {
    text-align: center;
    color: #6b7280 !important;
    font-size: 15px;
    margin-bottom: 28px;
}


/* ================================
   MAIN TWO-COLUMN LAYOUT
================================ */

#main-row {
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    align-items: stretch !important;
    gap: 24px !important;
    width: 100% !important;
}


/* LEFT PDF PANEL */

#pdf-panel {
    flex: 0 0 320px !important;
    width: 320px !important;
    min-width: 320px !important;
    max-width: 320px !important;
    color:#6b7280 !important;

    border: 1px solid #e5e7eb !important;
    border-radius: 18px !important;

    padding: 22px !important;

    background: #ffffff !important;

    box-shadow: 0 4px 18px rgba(0,0,0,0.06) !important;
}


/* RIGHT CHAT PANEL */

#chat-panel {
    flex: 1 1 auto !important;
    width: auto !important;
    min-width: 0 !important;
    color:black !important;
    border: 1px solid #e5e7eb !important;
    border-radius: 18px !important;

    padding: 22px !important;

    background: #ffffff !important;

    box-shadow: 0 4px 18px rgba(0,0,0,0.06) !important;
}


/* ================================
   PANEL HEADINGS
================================ */

.panel-heading {
    font-size: 20px !important;
    font-weight: 600 !important;
    color: #111827 !important;
    margin-bottom: 18px !important;
}


/* ================================
   PDF UPLOAD
================================ */

#pdf-upload {
    border: 2px dashed #d1d5db !important;
    border-radius: 14px !important;
    background: #fafafa !important;
}


/* ================================
   PROCESS BUTTON
================================ */

#process-button {
    width: 100% !important;
    height: 48px !important;

    margin-top: 16px !important;

    border-radius: 12px !important;

    font-size: 15px !important;
    font-weight: 600 !important;
}


/* ================================
   STATUS
================================ */

#status {
    margin-top: 18px !important;

    border-radius: 12px !important;

    background: #f0fdf4 !important;

    border: 1px solid #bbf7d0 !important;
}


/* ================================
   CHAT
================================ */

#chatbot {
    border: none !important;

    height: 500px !important;
    min-height: 500px !important;

    background: #ffffff !important;
}


/* ================================
   QUESTION AREA
================================ */

#question-row {
    display: flex !important;
    flex-direction: row !important;
    align-items: center !important;

    gap: 12px !important;

    margin-top: 18px !important;
}


/* QUESTION INPUT */

#question-box {
    flex: 1 !important;
    color:purple !important;
}

#question-box textarea {
    min-height: 58px !important;

    border-radius: 14px !important;

    border: 1px solid #d1d5db !important;

    background: #ffffff !important;

    font-size: 15px !important;

    padding: 16px !important;
}


/* ASK BUTTON */

#ask-button {
    width: 110px !important;

    min-height: 58px !important;

    border-radius: 14px !important;

    font-size: 16px !important;

    font-weight: 600 !important;
}


/* ================================
   CLEAR BUTTON
================================ */

#clear-button {
    width: 100% !important;

    margin-top: 14px !important;

    border-radius: 12px !important;

    height: 44px !important;
}


/* ================================
   FOOTER
================================ */

.footer {
    text-align: center;

    color: #9ca3af;

    margin-top: 24px;

    font-size: 13px;
}


/* ================================
   MOBILE
================================ */

@media (max-width: 850px) {

    #main-row {
        flex-direction: column !important;
    }

    #pdf-panel {
        width: 100% !important;
        max-width: none !important;
        min-width: 0 !important;
    }

    #chat-panel {
        width: 100% !important;
    }

}
"""

with gr.Blocks(
    title="AI PDF Chatbot",
    css=css
) as demo:

    # =========================
    # HEADER
    # =========================

    gr.Markdown(
        """
        <div id="title">
            🤖 AI PDF Chatbot
        </div>

        <div id="subtitle">
            Upload your PDF and ask questions about its content
        </div>
        """
    )

    # =========================
    # MAIN AREA
    # =========================

    with gr.Row(elem_id="main-row"):

        # =====================
        # LEFT PDF PANEL
        # =====================

        with gr.Column(elem_id="pdf-panel"):

            gr.Markdown(
                "📄 Upload PDF",
                elem_classes="panel-heading"
            )

            pdf_upload = gr.File(
                label="Choose a PDF",
                file_types=[".pdf"],
                type="filepath",
                elem_id="pdf-upload"
            )

            process_button = gr.Button(
                "⚡ Process PDF",
                variant="primary",
                elem_id="process-button"
            )

            status = gr.Textbox(
                label="Status",
                value="Upload a PDF to get started",
                interactive=False,
                elem_id="status"
            )

            clear_button = gr.Button(
                "🗑 Clear Chat",
                elem_id="clear-button"
            )


        # =====================
        # RIGHT CHAT PANEL
        # =====================

        with gr.Column(elem_id="chat-panel"):

            gr.Markdown(
                "💬 Conversation",
                elem_classes="panel-heading"
            )

            chatbot = gr.Chatbot(
                label="",
                elem_id="chatbot"
            )

            # =====================
            # QUESTION AREA
            # =====================

            with gr.Row(elem_id="question-row"):

                question = gr.Textbox(
                    label="",
                    placeholder="Ask something about your PDF...",
                    interactive=True,
                    scale=5,
                    elem_id="question-box"
                )

                ask_button = gr.Button(
                    "➤ Ask",
                    variant="primary",
                    scale=1,
                    elem_id="ask-button"
                )


    # =========================
    # FOOTER
    # =========================

    gr.Markdown(
        """
        <div class="footer">
            Built with Python • FAISS • HuggingFace • Qwen • Gradio
        </div>
        """
    )


    # =========================
    # BUTTON EVENTS
    # =========================

    process_button.click(
        fn=process_pdf,
        inputs=pdf_upload,
        outputs=[status, chatbot]
    )

    ask_button.click(
        fn=ask_question,
        inputs=[question, chatbot],
        outputs=[chatbot, question]
    )

    question.submit(
        fn=ask_question,
        inputs=[question, chatbot],
        outputs=[chatbot, question]
    )

    clear_button.click(
        fn=lambda: [],
        inputs=None,
        outputs=chatbot
    )


demo.launch()