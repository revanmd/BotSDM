from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet, AllSlotsReset


class ActionBackMenu(Action):

    def name(self) -> Text:
        return "action_back_menu"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text=f"!menu")
        return []

class ResetAction(Action):
	def name(self) -> Text:
		return "action_reset"

	def run(self,dispatcher: CollectingDispatcher,tracker: Tracker,domain: DomainDict)-> Dict[Text, Any]:
		print('resetGan')
		return [AllSlotsReset()]