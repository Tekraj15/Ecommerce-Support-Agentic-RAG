import streamlit as st
import requests

# API Endpoints
FLASK_API_BASE_URL = "http://localhost:5000/api"
RASA_ENDPOINT = "http://localhost:5005/webhooks/rest/webhook"

st.set_page_config(page_title="E-Commerce AI Support", layout="wide")

# Header
st.title("🛒 E-Commerce AI Support Agent")

# Sidebar for selecting actions
st.sidebar.header("Select an Option")
action = st.sidebar.radio("Choose an action:", ["Chat with AI", "Check Order Status", "Check Product Stock"])

# Function to communicate with Rasa chatbot
def get_chatbot_response(user_input):
    response = requests.post(RASA_ENDPOINT, json={"sender": "user", "message": user_input})
    return response.json()

# Function to fetch order status
def get_order_status(order_id):
    response = requests.get(f"{FLASK_API_BASE_URL}/orders/{order_id}")
    return response.json()

# Function to check product stock
def get_product_stock(product_name):
    response = requests.get(f"{FLASK_API_BASE_URL}/products/{product_name}/stock")
    return response.json()

# Chatbot interaction
if action == "Chat with AI":
    st.subheader("💬 Chat with the AI Assistant")
    user_input = st.text_input("You:", "")
    
    if st.button("Send"):
        if user_input:
            bot_response = get_chatbot_response(user_input)
            for message in bot_response:
                st.text_area("Bot:", value=message.get("text"), height=100)
        else:
            st.warning("Please enter a message.")

# Order status checking
elif action == "Check Order Status":
    st.subheader("📦 Track Your Order")
    order_id = st.text_input("Enter Order ID:")
    
    if st.button("Check Order"):
        if order_id:
            result = get_order_status(order_id)
            st.write(f"**Order ID:** {result.get('order_id')}")
            st.write(f"**Status:** {result.get('status')}")
        else:
            st.warning("Please enter a valid Order ID.")

# Product stock checking
elif action == "Check Product Stock":
    st.subheader("🛍️ Check Product Availability")
    product_name = st.text_input("Enter Product Name:")
    
    if st.button("Check Stock"):
        if product_name:
            result = get_product_stock(product_name)
            st.write(f"**Product Name:** {result.get('product_name')}")
            st.write(f"**Stock Available:** {result.get('stock')}")
        else:
            st.warning("Please enter a valid product name.")

st.sidebar.markdown("---")
st.sidebar.markdown("Developed by **Your Name**")
