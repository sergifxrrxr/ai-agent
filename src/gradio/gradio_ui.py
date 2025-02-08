import gradio as gr
import requests
import sqlite3
import pandas as pd
from init_db import init_db

session_id = None

DB_PATH = "/data/data.db"
init_db()

def get_bookings():
    conn = sqlite3.connect(DB_PATH)
    query = "SELECT booking_id as ID, hotel, check_in, check_out, adults, children FROM booking"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def chatbot_response(message, history):
    global session_id
    
    history.append((message, ""))
    
    url = "http://api:5005/chat"
    params = {"user_input": message}
    
    if session_id:
        params["session_id"] = session_id
    
    try:
        response = requests.post(url, params=params)
        response.raise_for_status()
        response_data = response.json()
        
        bot_reply = response_data.get("message", "No response from the bot.")
        session_id = response_data.get("session_id", session_id)
    except requests.exceptions.RequestException as e:
        bot_reply = f"Error: {e}"
    except ValueError:
        bot_reply = "Invalid JSON response from the server."

    history[-1] = (message, bot_reply)
    
    return history, ""


def clear_chat():
    global session_id
    session_id = None
    return []

def update_bookings():
    df = get_bookings()
    return df

with open('styles.css', 'r') as file:
    css_styles = file.read()

with gr.Blocks(css=css_styles) as iface:
    gr.Markdown("# AI Travel Agent ✈️")
    
    with gr.Row():
        with gr.Column():
            chatbot = gr.Chatbot(elem_id="chatbot")
            msg = gr.Textbox(
                show_label=False,
                placeholder="Type your message here...",
                lines=1,
                max_lines=1,
                elem_id="textbox"
            )
            with gr.Row():
                submit_btn = gr.Button("Submit", variant="primary")
                clear = gr.Button("Clear Chat", variant="secondary")
        
        with gr.Column():
            gr.Markdown("## Bookings Data")
            bookings_table = gr.Dataframe(
                headers=["ID", "Name", "Date", "Time", "Status"],
                datatype=["str", "str", "str", "str", "str"],
                interactive=False,
                elem_id="bookings-table"
            )
            refresh_btn = gr.Button("Refresh Bookings ♻️", variant="secondary")

    submit_btn.click(
        chatbot_response, [msg, chatbot], [chatbot, msg], queue=False
    )
    msg.submit(
        chatbot_response, [msg, chatbot], [chatbot, msg], queue=False
    )

    
    clear.click(clear_chat, None, chatbot, queue=False)
    
    refresh_btn.click(update_bookings, None, bookings_table, queue=False)

    iface.load(update_bookings, None, bookings_table, queue=False)

if __name__ == "__main__":
    iface.launch(server_name='0.0.0.0')