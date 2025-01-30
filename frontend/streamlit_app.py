import streamlit as st
import requests
from datetime import datetime

# API Configuration
FLASK_API_BASE_URL = "http://localhost:5000/api"
RASA_ENDPOINT = "http://localhost:5005/webhooks/rest/webhook"

# UI Configuration
st.set_page_config(
    page_title="E-Commerce AI Support",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .stTextInput>div>div>input {
        border-radius: 20px;
        padding: 12px;
    }
    .stButton>button {
        border-radius: 20px;
        padding: 8px 20px;
        background: #2563eb;
        color: white;
    }
    .chat-message {
        padding: 15px;
        border-radius: 15px;
        margin: 10px 0;
    }
    .user-message {
        background: #f0f4f8;
    }
    .bot-message {
        background: #2563eb15;
    }
</style>
""", unsafe_allow_html=True)

# Session State Initialization
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Header Section
st.title("🛒 Smart E-Commerce Support Agent")
st.markdown("---")

# Sidebar Configuration
with st.sidebar:
    st.header("Navigation")
    action = st.radio(
        "Select Service:",
        ["AI Assistant Chat", "Order Tracking", "Product Availability"],
        index=0
    )
    
    st.markdown("---")
    st.markdown("**Need Help?**")
    st.markdown("📞 Contact Support: support@ecom.ai")
    st.markdown("📧 Email: contact@ecom.ai")

# API Helper Functions
def handle_api_call(endpoint, method='GET', params=None):
    try:
        with st.spinner("Processing..."):
            if method == 'GET':
                response = requests.get(endpoint)
            elif method == 'POST':
                response = requests.post(endpoint, json=params)
            
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {str(e)}")
        return None

# Chat Interface
if action == "AI Assistant Chat":
    st.subheader("💬 AI Support Assistant")
    
    # Chat Container
    chat_container = st.container()
    
    # Display Chat History
    with chat_container:
        for msg in st.session_state.chat_history:
            css_class = "user-message" if msg['sender'] == 'user' else "bot-message"
            st.markdown(
                f"<div class='chat-message {css_class}'>"
                f"<strong>{msg['sender'].title()}:</strong> {msg['content']}<br>"
                f"<small>{msg['timestamp']}</small>"
                "</div>", 
                unsafe_allow_html=True
            )
    
    # Input Section
    user_input = st.text_input(
        "Type your message:", 
        placeholder="How can I help you today?",
        key="chat_input"
    )
    
    col1, col2 = st.columns([1, 0.1])
    with col1:
        if st.button("Send Message", key="send_button"):
            if user_input.strip():
                # Add user message to history
                st.session_state.chat_history.append({
                    "sender": "user",
                    "content": user_input,
                    "timestamp": datetime.now().strftime("%H:%M:%S")
                })
                
                # Get bot response
                bot_response = handle_api_call(
                    RASA_ENDPOINT,
                    method='POST',
                    params={"sender": "user", "message": user_input}
                )
                
                if bot_response:
                    for message in bot_response:
                        st.session_state.chat_history.append({
                            "sender": "bot",
                            "content": message.get("text", "I didn't understand that"),
                            "timestamp": datetime.now().strftime("%H:%M:%S")
                        })
                else:
                    st.session_state.chat_history.append({
                        "sender": "bot",
                        "content": "Sorry, I'm having trouble connecting to the service.",
                        "timestamp": datetime.now().strftime("%H:%M:%S")
                    })
                
                # Rerun to update display
                st.rerun()

# Order Tracking Section
elif action == "Order Tracking":
    st.subheader("📦 Real-Time Order Tracking")
    
    with st.form("order_tracking_form"):
        order_id = st.text_input(
            "Order ID:",
            placeholder="Enter your 12-digit order number",
            max_chars=12
        )
        
        if st.form_submit_button("Track Order", use_container_width=True):
            if len(order_id) != 12 or not order_id.isalnum():
                st.error("Please enter a valid 12-character order ID")
            else:
                result = handle_api_call(f"{FLASK_API_BASE_URL}/orders/{order_id}")
                if result:
                    with st.expander("Order Details", expanded=True):
                        cols = st.columns(3)
                        cols[0].metric("Order Status", result.get('status', 'Unknown'))
                        cols[1].metric("Last Updated", result.get('last_updated', 'N/A'))
                        cols[2].metric("Estimated Delivery", result.get('delivery_date', 'N/A'))
                        
                        st.map({
                            'latitude': [result.get('location', {}).get('lat', 0)],
                            'longitude': [result.get('location', {}).get('lng', 0)]
                        })

# Product Availability Section
elif action == "Product Availability":
    st.subheader("📊 Product Stock Checker")
    
    with st.form("stock_check_form"):
        product_name = st.text_input(
            "Product Name:",
            placeholder="Enter exact product name",
            key="product_input"
        )
        
        if st.form_submit_button("Check Availability", use_container_width=True):
            if not product_name.strip():
                st.error("Please enter a product name")
            else:
                result = handle_api_call(f"{FLASK_API_BASE_URL}/products/{product_name}/stock")
                if result:
                    cols = st.columns(3)
                    cols[0].metric("Product Name", product_name)
                    cols[1].metric("Available Stock", result.get('stock', 0))
                    cols[2].metric("Restock ETA", result.get('restock_date', 'N/A'))
                    
                    st.progress(min(result.get('stock', 0)/100, 1.0))