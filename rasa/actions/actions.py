from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests

class ActionGetOrderStatus(Action):
    def name(self) -> Text:
        return "action_get_order_status"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        order_id = tracker.get_slot("order_id")
        
        # Call Flask API endpoint
        response = requests.get(f"http://localhost:5000/api/orders/{order_id}").json()
        
        dispatcher.utter_message(
            response_template="utter_order_status",
            order_id=order_id,
            status=response.get("status", "unknown")
        )
        return []

class ActionGetProductStock(Action):
    def name(self) -> Text:
        return "action_get_product_stock"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        product_name = tracker.get_slot("product_name")
        
        # Call Flask API endpoint
        response = requests.get(f"http://localhost:5000/api/products/{product_name}/stock").json()
        
        dispatcher.utter_message(
            response_template="utter_product_stock",
            product_name=product_name,
            stock=response.get("stock", 0)
        )
        return []