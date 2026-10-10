"""
Gradio interface for Agent Incident Analyzer.
"""

import gradio as gr

from src.orchestrator import IncidentOrchestrator


def analyze_incident(message: str, history: list[list[str]]) -> tuple[str, list[list[str]]]:
    """
    Analyze an incident using the orchestrator.

    Args:
        message: User's incident description.
        history: Chat history.

    Returns:
        Tuple of (empty string, updated chat history).
    """
    if not message or not message.strip():
        return "", history

    # Add user message to history
    history.append([message, None])

    try:
        # Invoke orchestrator
        orchestrator = IncidentOrchestrator(require_api_key=True)
        result = orchestrator.invoke(message)

        # Add assistant response to history
        history[-1][1] = result.final_response or "No response generated"

    except Exception as e:
        error_message = f"Error analyzing incident: {str(e)}"
        history[-1][1] = error_message

    return "", history


def create_interface() -> gr.Blocks:
    """
    Create the Gradio interface.

    Returns:
        Gradio Blocks interface.
    """
    with gr.Blocks(title="Agent Incident Analyzer") as interface:
        gr.Markdown(
            """
            # Agent Incident Analyzer

            A multi-agent system for IT incident analysis.

            Describe an incident and the system will:
            - Select relevant investigation agents
            - Collect evidence from logs, API, database, and deployments
            - Determine the probable root cause
            - Recommend remediation actions
            """
        )

        chatbot = gr.Chatbot(
            label="Incident Analysis",
            height=500,
            show_copy_button=True,
        )

        with gr.Row():
            msg = gr.Textbox(
                label="Your Message",
                placeholder="Describe the incident (e.g., 'The payments API is returning HTTP 500 errors')",
                scale=4,
            )
            submit = gr.Button("Analyze", scale=1)

        gr.Examples(
            examples=[
                "The payments API is returning HTTP 500 errors.",
                "The API is slow and users are receiving database timeout errors.",
                "We started receiving many HTTP 500 errors immediately after the latest deployment.",
            ],
            inputs=msg,
        )

        # Event handlers
        submit.click(
            analyze_incident,
            inputs=[msg, chatbot],
            outputs=[msg, chatbot],
        )

        msg.submit(
            analyze_incident,
            inputs=[msg, chatbot],
            outputs=[msg, chatbot],
        )

    return interface


def main():
    """Run the Gradio interface."""
    interface = create_interface()
    interface.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
    )


if __name__ == "__main__":
    main()
