from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction
import requests
from openai import OpenAI
import logging
import os
from datetime import datetime

# Configure logging
logger = logging.getLogger(__name__)

class ActionGetOrderStatus(Action):
    def name(self) -> Text:
        return "action_get_order_status"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        order_id = tracker.get_slot("order_id")
        try:
            response = requests.get(
                f"http://localhost:5000/api/orders/{order_id}",
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            return [
                SlotSet("last_order_status", data.get("status")),
                SlotSet("order_last_checked", datetime.now().isoformat()),
                SlotSet("shipping_eta", data.get("eta"))
            ]
            
        except Exception as e:
            logger.error(f"Order status check failed: {str(e)}")
            dispatcher.utter_message(response_template="utter_order_check_failed")
            return []

class ActionGetProductStock(Action):
    def name(self) -> Text:
        return "action_get_product_stock"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        product_name = tracker.get_slot("product_name")
        try:
            response = requests.get(
                f"http://localhost:5000/api/products/{product_name}/stock",
                timeout=10
            )
            response.raise_for_status()
            stock_data = response.json()
            
            dispatcher.utter_message(
                response_template="utter_product_stock",
                product_name=product_name,
                stock=stock_data.get("stock", 0),
                restock_date=stock_data.get("restock_date", "N/A")
            )
            
            return [
                SlotSet("last_product_checked", product_name),
                SlotSet("current_stock", stock_data.get("stock")),
                FollowupAction("action_offer_restock_notification")
            ]

        except Exception as e:
            logger.error(f"Product stock check failed: {str(e)}")
            dispatcher.utter_message(response_template="utter_stock_check_failed")
            return []

# Autonomous return flow
class ActionInitiateReturn(Action):
    def name(self) -> Text:
        return "action_initiate_return"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        order_id = tracker.get_slot("order_id")
        user_email = tracker.get_slot("email")
        
        try:
            # 1. Validate return eligibility
            eligibility_response = requests.post(
                "http://localhost:5000/api/returns/validate",
                json={"order_id": order_id},
                timeout=10
            )
            
            if not eligibility_response.json().get("eligible"):
                dispatcher.utter_message(response_template="utter_return_not_eligible")
                return []

            # 2. Create return request
            return_response = requests.post(
                "http://localhost:5000/api/returns",
                json={
                    "order_id": order_id,
                    "user_email": user_email
                },
                timeout=10
            )
            return_data = return_response.json()

            # 3. Send confirmation
            dispatcher.utter_message(response_template="utter_return_initiated", 
                                   return_id=return_data["return_id"])
            
            # 4. Trigger email
            requests.post(
                "http://localhost:5000/api/emails/send",
                json={
                    "to": user_email,
                    "subject": "Return Initiated",
                    "body": f"Return ID: {return_data['return_id']}"
                },
                timeout=10
            )
            
            return [
                SlotSet("active_return_id", return_data["return_id"]),
                FollowupAction("action_list_followup_options")
            ]

        except Exception as e:
            logger.error(f"Return initiation failed: {str(e)}")
            dispatcher.utter_message(response_template="utter_return_failed")
            return []

class ActionHandleComplexQuery(Action):
    def name(self) -> Text:
        return "action_handle_complex_query"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        context = {
            "order_history": tracker.get_slot("order_history"),
            "return_policy": tracker.get_slot("return_policy"),
            "user_tier": tracker.get_slot("user_tier")
        }
        
        try:
            client = OpenAI(
                base_url="https://api.deepseek.com/v1",
                api_key=os.getenv("DEEPSEEK_API_KEY")
            )

            response = client.chat.completions.create(
                model="deepseek-r1",
                messages=[
                    {
                        "role": "system",
                        "content": f"""You are an e-commerce support agent. Context:
                        - Return policy: {context['return_policy']}
                        - User tier: {context['user_tier']}
                        - Last 3 orders: {context['order_history']}"""
                    },
                    {
                        "role": "user", 
                        "content": tracker.latest_message.get("text")
                    }
                ],
                temperature=0.3,
                max_tokens=150
            )

            bot_response = response.choices[0].message.content
            dispatcher.utter_message(text=bot_response)
            
            # Auto-detect and set slots from response
            if "return" in bot_response.lower():
                return [FollowupAction("action_initiate_return")]
            elif "stock" in bot_response.lower():
                return [FollowupAction("action_get_product_stock")]
                
            return []

        except Exception as e:
            logger.error(f"DeepSeek-R1 API error: {str(e)}")
            dispatcher.utter_message(response_template="utter_llm_fallback")
            return []

class ActionListFollowupOptions(Action):
    def name(self) -> Text:
        return "action_list_followup_options"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
        buttons = [
            {"title": "Track Return", "payload": "/track_return"},
            {"title": "Contact Support", "payload": "/human_transfer"},
            {"title": "Shop More", "payload": "/product_suggestions"}
        ]
        
        dispatcher.utter_message(
            text="What would you like to do next?",
            buttons=buttons
        )
        return []

class ActionOfferRestockNotification(Action):
    def name(self) -> Text:
        return "action_offer_restock_notification"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
        product_name = tracker.get_slot("last_product_checked")
        buttons = [
            {
                "title": "Yes, notify me",
                "payload": f"/subscribe_restock_notification{{'product_name':'{product_name}'}}"
            },
            {
                "title": "No thanks",
                "payload": "/deny_restock_notification"
            }
        ]
        
        dispatcher.utter_message(
            text="Would you like to be notified when this product is back in stock?",
            buttons=buttons
        )
        return []

class ActionRagQuery(Action):
    def name(self) -> Text:
        return "action_rag_query"

    def run(self, dispatcher, tracker, domain):
        query = tracker.latest_message.get("text", "")
        payload = {"query": query}

        try:
            response = requests.post(
                "http://localhost:8000/rag/query",
                json=payload,
                timeout=15
            )
            response.raise_for_status()
            data = response.json()

            answer = data.get("answer", "No answer.")
            sources = data.get("sources", [])
            
            # Adding toll calling info
            tool_calls = data.get("tool_calls", [])
            confidence = data.get("confidence", 0.0)

            msg = f"{answer}\n\nConfidence: {confidence:.2f}"
            if sources:
                src_list = ", ".join([s["source"] for s in sources])
                msg += f"\nSources: {src_list}"
            if tool_calls:
                tools = ", ".join([t["tool"] for t in tool_calls])
                msg += f"\nTools used: {tools}"

            dispatcher.utter_message(text=msg)

        except requests.exceptions.RequestException as e:
            dispatcher.utter_message(text=f"RAG service unavailable: {e}")
        except Exception as e:
            dispatcher.utter_message(text=f"Error: {e}")

        return []