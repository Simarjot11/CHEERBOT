from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import UserUtteranceReverted
import re 
import pandas as pd
import json
from rasa_sdk.events import (
    SlotSet,
    UserUtteranceReverted,
    ConversationPaused,
    EventType,
    FollowupAction,
)
f= open('data.json')
data= json.load(f)

def redirectToSlot(slot, value, dispatcher, tracker, remapping):
    response = {slot: value} # default response

    if (slot == "mailid"):
        regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if(re.search(regex, value)):
            response = {slot: value}
        else:
            dispatcher.utter_message(template="utter_wrong_mailid")
            response = {slot: None}
    elif (slot == "phone_number"):
        if len(value) == 10:
            if(value.isdigit()):
                response = {slot: value}
            else:
                dispatcher.utter_message(template="utter_wrong_phonenumberalpha")
                response = {slot: None}  
        else:
            dispatcher.utter_message(template="utter_wrong_phone_number")
            response = {slot: None}

    if (type(remapping) == str):
        response[remapping] = None

    return response
    
    
class InfoForm(FormAction):

    def name(self) -> Text:
        return "info_form"

    @staticmethod
    def required_slots(tracker):
        return [
            "username",
            "mailid",
            "phone_number",
            ]
            
    @staticmethod
    def msg() -> List[Text]:
        return ["back1","back2"]
        
        
    def validate_username(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
     ) -> Dict[Text, Any]:
        """Validate username."""
        value=tracker.get_slot("username")

        print("validate_username() method", value)

        requestedSlot = tracker.get_last_event_for("slot", skip=1)
        if (requestedSlot['name'] == 'requested_slot'):
            if (requestedSlot['value'] == 'username'): # If requested slot was username and value also corresponds to the username 
                return redirectToSlot(requestedSlot['value'], value, dispatcher, tracker, None)
            else: # If value corresponds to the wrong slot
                return redirectToSlot(requestedSlot['value'], value, dispatcher, tracker, 'username')
        else:
            return redirectToSlot('username', value, dispatcher, tracker, None)

 
    def validate_mailid(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
     ) -> Dict[Text, Any]:
        """Validate mailid."""

        
        if value.lower() not in self.msg():
            value=tracker.get_slot("mailid")
            print("validate_mailid() method", value)

            requestedSlot = tracker.get_last_event_for("slot", skip=1)
            if (requestedSlot['name'] == 'requested_slot' and requestedSlot['value']):
                if (requestedSlot['value'] == 'mailid'): # If requested slot was mailid and value also corresponds to the mailid 
                    return redirectToSlot(requestedSlot['value'], value, dispatcher, tracker, None)
                else: # If value corresponds to the wrong slot
                    return redirectToSlot(requestedSlot['value'], value, dispatcher, tracker, 'mailid')
            else:
                return redirectToSlot('mailid', value, dispatcher, tracker, None)
        else:
            return {"username": None, "mailid": None}
            
    def validate_phone_number(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
     ) -> Dict[Text, Any]:
        """Validate phone."""

        
        if value.lower() not in self.msg():
            value=tracker.get_slot("phone_number")
            print("validate_phone_number() method  ", value)
            
            requestedSlot = tracker.get_last_event_for("slot", skip=1)
            if (requestedSlot['name'] == 'requested_slot'):
                if (requestedSlot['value'] == 'phone_number'): # If requested slot was phone_number and value also corresponds to the phone_number 
                    return redirectToSlot(requestedSlot['value'], value, dispatcher, tracker, None)
                else: # If value corresponds to the wrong slot
                    return redirectToSlot(requestedSlot['value'], value, dispatcher, tracker, 'phone_number')
            else:
                return redirectToSlot('phone_number', value, dispatcher, tracker, None)
        else:
            return {"mailid": None,"phone_number": None}
            
            
            
    def submit(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict]:
             
        username = tracker.get_slot("username")
        mailid = tracker.get_slot("mailid")
        phone_number=tracker.get_slot("phone_number")
        message="DETAILS:"+"\n\n"+"Name:"+username+"\n"+"Email:"+mailid+"\n"+"Phone Number:"+phone_number+"\nThanks! for sharing information"
        dispatcher.utter_message(message)

        return []
        
class StudentForm(FormAction):

    def name(self):
        return "student_form"
    @staticmethod
    def required_slots(tracker):
        return [
            "student_problem",
            ]
    def validate_student_problem(self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        item=str(tracker.get_slot("student_problem"))
        
        if item=="Effect on Studies":
            dispatcher.utter_message("Check this video")
            dispatcher.utter_message(text="Items List",json_message={"payload":"cardsCarousel","data":data['data']['Effect on Studies']})
            dispatcher.utter_message(text=''' Some more links to such videos are:\n
            1.https://www.youtube.com/watch?v=z3FA2kALScU&list=PLstHkpcp5Zh1KBtzkQ8AHzaTpJXO53AIj&index=3 \n
            2.https://www.youtube.com/watch?v=Df3ysUkdB38&list=PLstHkpcp5Zh1KBtzkQ8AHzaTpJXO53AIj&index=2 \n
            3.https://www.youtube.com/watch?v=KxV5Oh0eb6Y&list=PLstHkpcp5Zh1KBtzkQ8AHzaTpJXO53AIj&index=4  \n
            4.https://www.youtube.com/watch?v=R7iN71uJcG0&list=PLstHkpcp5Zh1KBtzkQ8AHzaTpJXO53AIj&index=10 \n
            5.https://www.youtube.com/watch?v=WBGxOFspJh4&list=PLstHkpcp5Zh1KBtzkQ8AHzaTpJXO53AIj&index=14 \n ''')
            
            dispatcher.utter_message(text=''' Piece of Advice:
            Three techniques—\n
            1.elaborative interrogation, 2.self-explanation, and 3.interleaved practice—were noted to be of moderate utility. When students utilize elaborative interrogation, they aim to explain why concepts are the way they are or why they are true. Self-explanation is where the student explains the link between both new and current knowledge, and self-explanation can also be used to explain the needed steps in a problem. Interleaved practice is a strategy where the student studies different concepts in one sitting.\n
            Key: These strategies, if done well, can be useful for learning.\n
            Hope These strategies would help you.Thankyou .''')
            
            return {"student_problem":value}
        
        elif item=="Anxiety":
            dispatcher.utter_message(text='''Ohkkk! First of all clm down a bit and just watch this for next 5 min.\n
https://www.youtube.com/watch?v=Ng5qiDAkiI0&list=PLstHkpcp5Zh1cyV2SSbbZKjLi4WsQBYb3&index=2

\n Feeling better just try to watch this as well before leaving
https://www.youtube.com/watch?v=YPG_6618sWw&list=PLstHkpcp5Zh1cyV2SSbbZKjLi4WsQBYb3&index=1

\n Hope You are now feeling a lot better than when you meet me .
I am happy I could help you thankyou.
''')
            return {"student_problem":value}
        
        elif item=="Bored":
            
            dispatcher.utter_message(text='''Bored ! why we have lot of time to groom ourselves like our talents , our hobies, our health.Let me tell You some activities which will decrease your boredom:\n
            1.Chat and group video call with your friends , Nowadays there are games where all can play together and have some fun like ludo,guns of boom. Try it!\n
            2.Try do spend more time on your hobby if u don't have any hobby best time to find it.\n
            3.Spend Some time helping your mother it would ease her work and also make her and u happy and a little source for physical activity .\n
            Try These if still You feel boredom then  lets see You still feel boredom so now lets dive into activities of learning. I know it sounds boring but Very productive and fun if once starts.\n
            1. You can learn Any new language like French or Japanese .
            Let me Provide You source as well:
            https://www.inc.com/larry-kim/9-places-to-learn-a-new-language-online-for-fre.html \n
            2. If interested in computers than u can learn computer languages like Python, Java, JavaScript,C,C++.......
            Let me Provide You source as well:
            1. Learning Lad for C/C++
            2. Telusko for Python/Java.\n
            Go check them out.\n
            Now I think you understand the gist of what I am trying to say so go and explore the Internet .
            Hope These advices would help you. Thankyou :) 
''')
            return {"student_problem":value}
        
        elif item=="Health Related":

            
            dispatcher.utter_message(text='''It seems you are fitness lover , but I know pandemic has disturbed your whole health routine as well , So let me help u :\n''')
            dispatcher.utter_message(text="Check this video:)",json_message={"payload":"cardsCarousel","data":data['data']['Health Related']})
            dispatcher.utter_message(text='''For Girls:\n
            Diet Chart \n
            https://blog.decathlon.in/articles/weight-loss-indian-diet-chart \n 
            Exercise:\n
            1.https://www.youtube.com/watch?v=vG_Bs0QLc3I\n
            2.https://www.youtube.com/watch?v=LhL5SNZfnQs\n

            For Boys:\n
            Diet Plan\n
            https://www.health-total.com/weight-loss/weight-loss-for-men/ \n

            Exercise:\n
            1.https://www.youtube.com/watch?v=UVJSiuWBNYM \n
            2.https://www.youtube.com/watch?v=PcuL6L8xqRE \n
''')
            return {"student_problem":value}
        else: 
            return {"order":None}

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
    
        item=(tracker.get_slot("student_problem"))
        item= next(tracker.get_latest_entity_values("student_problem"),None)
        dispatcher.utter_message("That's Great")
        return []
        
class ProfessionalForm(FormAction):

    def name(self):
        return "professional_form"
    @staticmethod
    def required_slots(tracker):
        return [
            "professional_problem",
            ]
    def validate_professional_problem(self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        item=str(tracker.get_slot("professional_problem"))
        
        if item=="Job Related":
            
            dispatcher.utter_message(text='''First make accounts on these sites:\n
            1.  Linkedin\n
            2.  Truelancer\n
            3.  Internshala\n
            4.  Upwork\n
            5.  Broxer\n
            6.  NCubeRoot\n
            These are best sites from where we can get job or can do freelancing . We have also taken your mail id So our team will also send you notification if any opportunity is arised . You also focus on these sites.''')
            return {"professional_problem":value}
            
        elif item=="Work Stress":
            
            dispatcher.utter_message(text='''Yes I know this pandemic has brought a lot of stress and then work from home is acting like topings on cake.\n
            Some Ways to remove work from home stress:\n
            1.Start Exercising(or Exercise more): It lifts your mood. Increase Energy and also sharpens focus. Atleast 30 minutes of activity on most days.Go for walks througout the day to De-Stress\n
            2.Eat Healthy and Nutritious Foods: Reduce your sugar consumption to avoid energy crashes.Avoid stimulants like caffune or nicotine.\n
            3.Priortize And Organize: Plan regular breaks throughout your day. Prioritize your most important tasks and projects earlier in the day.\n
            4.Get Enough Sleep: Here are some tips to get your sleep schedule back on track:\n
            *	Shoot for eight hours a night. There used to be a stigma, especially among business leaders, that “sleep is for the weak.” The most productive people know that you can’t operate at peak performance without the regenerative effects of proper sleep. So don’t skimp!\n
            *    Take cat naps. We’re talking 15-20 minutes, max. While we definitely believe that naps are regenerative, don’t over do it. Again, the goal is to get in a rhythm of getting proper sleep more often than not, so you’re clear headed and ready to take on the day.\n
            *	Stick to a schedule. Set your body’s internal clock by hitting the hay at the same time every night. You should be able to fall asleep fairly quickly and wake at the same time each day without an alarm clock. And speaking of sticking to a schedule\n
            5. Stay positive. One way to do this is to express gratitude. It’s surprising how much different your outlook is when you make a point to recognize the people and things in your life that you’re lucky to have.''')
            return {"professional_problem":value}
        
        elif item=="Health Related":

            
            dispatcher.utter_message(text='''It seems you are fitness lover , but I know pandemic has disturbed your whole health routine as well , So let me help u :\n''')
            dispatcher.utter_message(text="Check this video:)",json_message={"payload":"cardsCarousel","data":data['data']['health Related']})
            dispatcher.utter_message(text='''For Women:\n
            Diet Chart \n 
            https://blog.decathlon.in/articles/weight-loss-indian-diet-chart \n 
            Exercise:\n
            1.https://www.youtube.com/watch?v=vG_Bs0QLc3I\n
            2.https://www.youtube.com/watch?v=LhL5SNZfnQs\n

            For Men:\n
            Diet Plan\n
            https://www.health-total.com/weight-loss/weight-loss-for-men/ \n

            Exercise:\n
            1.https://www.youtube.com/watch?v=UVJSiuWBNYM \n
            2.https://www.youtube.com/watch?v=PcuL6L8xqRE \n
''')
            return {"professional_problem":value}
        else: 
            return {"order":None}
    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
    
        item=(tracker.get_slot("professional_problem"))
        item= next(tracker.get_latest_entity_values("professional_problem"),None)
        dispatcher.utter_message("That's Great")
        return []
            
class ElderlyForm(FormAction):

    def name(self):
        return "elderly_form"
    @staticmethod
    def required_slots(tracker):
        return [
            "elderly_problem",
            ]
    def validate_student_problem(self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        item=str(tracker.get_slot("elderly_problem"))
        
        if item=="Medical Facilities":
            dispatcher.utter_message(text='''Yes I know Because of Pandemic there is a lot of problem for medicines so I have a solution for this , For medicines Check this out: \n
https://www.netmeds.com/ \n
https://pharmeasy.in/ \n
 And For doctors Consultation:\n
https://www.1mg.com/online-doctor-consultation  \n
https://www.doconline.com/ \n

Apps Which support online doctor support:\n
1. DocOn\n
The app lets the person consult a doctor through video call. Prescription are also given digitally and your medical history too is maintained on the app. After you book an appointment at your chosen time slot, the concerned doctor will video call you at that time.\n

2.Lybrate\n
The company which was found in 2013 is considered to be among the top brands in this field. The app not only connects patients with doctors through mobile app and website but also has a facility with which samples can be collected from the patients doorstep. The result of the test is made available online. Lybrate can be downloaded through App Store and Google Play Store.\n

3. Tata Health\n
This app can connect a person with a doctor 24*7. The consultation on the app takes place through audio calls and chats. The app also lets the user purchase medicines and book lab tests if need be. The app is available on both App Store and Play Store\n
4. Practo\n
Available on both Android and iOS, Practo lets a person book an appointment with a doctor online. The session with the doctor can be held over a voice call or chat. Both paid and free consultations are available on the portal. All queries on the app are answered, in case a query goes unanswered then, the money is refunded.
 ''')
            return {"elderly_problem":value}
        elif item=="Covid Phobia":
            dispatcher.utter_message(text='''I know listening news of deaths create a sort of fear and tension in your mind but you need to understand this is just a phase which will pass as others . We need to take precautions ,like santizing, minimal outing but there is no need to fear from this pandemic . I would suggest you to pick up some hobbies to take your mind off situations and:\n
1.	Avoid news on TV or Phone instead watch funny shows or movies .\n
2.	Eat healthy food and Exercise daily for just 30 minutes .It will boost your imunity.\n
And rest just enjoy your life ,nice talking to you Bie;
 ''')
            return {"elderly_problem":value}
        elif item=="Bored":
            dispatcher.utter_message(text=''' Ya! I know due to this pandemic our socialising activities like 
Morning Walk in park with friends/family. And now just sitting creates boredom so I have some solutions for this like develop a new hobby or play indoor games like Ludo, Carrom etc.
For hobbies I have some suggestions :\n
https://www.lifeline24.co.uk/top-15-hobby-ideas-for-older-people/ \n
just visit this page I am sure you will find best suited hobby for you.
''')
            return {"elderly_problem":value}
        elif item=="Health Related":
            #msg = { "type": "video", "payload": { "title": "Link name", "src": "https://www.youtube.com/watch?v=kokD6gGwq3M" } }
            
            dispatcher.utter_message(text='''It seems you are fitness lover , but I know pandemic has disturbed your whole health routine as well , So let me help u :\n''')
            #dispatcher.utter_message(text="Check this video",attachment=msg)
            dispatcher.utter_message(text="Check this video:)",json_message={"payload":"cardsCarousel","data":data['data']['health related']})
            dispatcher.utter_message(text='''For Women:\n
            Diet Chart \n 
           https://www.thefitindian.com/blog/diet-charts-for-aging-adults-to-maintain-weight/ \n 
            Exercise:\n
            1.https://www.youtube.com/watch?v=Ev6yE55kYGw \n
            For Men:\n
            Diet Plan\n
           http://www.shieldhealthcare.com/community/news/2012/07/10/nutrition-over-70-a-guide-to-senior-dietary-needs/ \n

            Exercise:\n
            1.https://www.youtube.com/watch?v=KJ8Cwl9IQZ0\n
          Top of All Try to walk after every meal for 5-10minutes.
''')
            return {"elderly_problem":value}
        else: 
            return {"order":None}

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
    
        item=(tracker.get_slot("elderly_problem"))
        item= next(tracker.get_latest_entity_values("elderly_problem"),None)
        dispatcher.utter_message("That's Great")
        return []

 
   