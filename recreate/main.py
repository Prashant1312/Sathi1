from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivy.lang import Builder
import requests
import re
from kivymd.uix.button import MDFlatButton
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivy.uix.image import Image as KivyImage
from kivymd.uix.dialog import MDDialog
import os
import string
import speech_recognition as sr
import pyaudio
import wave
from kivy.core.window import Window
from kivy.clock import Clock

Window.size = (310, 580)

FIREBASE_URL = 'https://sathi-2023-default-rtdb.firebaseio.com/'
kv = """
ScreenManager:
    MainScreen:
        name: "main"
    LoginPage:
        name: "login"
    RegisterPage:
        name: "register"
    FinalPage:
        name:"final"    
    

<MainScreen>:
    MDFloatLayout:
        g_color:1,1,1,1
        Image:
            source:"sathi-logo1.png"
            size_hint:.3,.3
            pos_hint:{"center_x": .15, "center_y": .93}
        Image:
            source:"logo1.png"
            size_hint:.9,.9
            pos_hint:{"center_x": .5, "center_y": .60}
        MDLabel:
            text: " H e l l o !"
            font_name:"MPoppins-SemiBold"
            font_size:"23sp"
            pos_hint:{"center_y":.43}
            halign:"center"
            color: rgba(34,34,34,255)
        MDLabel:
            text: "Feel Free To Talk, We Are Listening"
            font_name:"MPoppins-Medium"
            font_size:"13sp"
            size_hint_x:.85
            pos_hint:{"center_x": .5, "center_y": .35}
            halign:"center"
            color: rgba(127,127,127,255)
        MDLabel:
            text: "Helping People To Connect"
            font_name:"MPoppins-Medium"
            font_size:"13sp"
            size_hint_x:.85
            pos_hint:{"center_x": .5, "center_y": .31}
            halign:"center"
            color: rgba(127,127,127,255)
        Button:
            text:"LOGIN"
            pos_hint:{"center_x": .5, "center_y": .20}
            font_name:"MPoppins-SemiBold"
            size_hint: .75, .065
            background_color: 0,0,0,0
            on_release:
                app.root.current = "login"  # Add this line to switch to the "login" screen
            canvas.before:
                Color:
                    rgb: rgba(52,0,231,255)
                RoundedRectangle:
                    size:self.size
                    pos: self.pos
                    radius:[5]
        Button:
            text:"REGISTER"
            size_hint: .75, .065
            pos_hint:{"center_x": .5, "center_y": .10}
            background_color: 0,0,0,0
            font_name:"MPoppins-SemiBold"
            color:  rgba(52,0,231,255)
            on_release:
                app.root.current = "register"
            canvas.before:
                Color:
                    rgb: rgba(52,0,231,255)
                Line:
                    width:1.2
                    rounded_rectangle: self.x,self.y,self.width,self.height,5,5,5,5,100

<LoginPage>:

    MDFloatLayout:
        md_bg_color: 1, 1, 1, 1
        MDIconButton:
            icon: "arrow-left"
            pos_hint: {"center_y": .95}
            user_font_size: "30sp"
            theme_text_color: "Custom"
            text_color: rgba(26, 24, 58, 255)
            on_release:
                app.root.current = "main"

        MDLabel:
            text: " W E L C O M E !"
            font_name: "MPoppins-SemiBold"
            font_size: "26sp"
            pos_hint: {"center_x": .7, "center_y": .80}
            color: rgba(0, 0, 59, 255)

        MDLabel:
            text: "      S i g n  i n  t o  c o n t i n u e"
            font_name: "MPoppins-SemiBold"
            font_size: "16sp"
            pos_hint: {"center_x": .6, "center_y": .75}
            color: rgba(135, 133, 193, 255)

        MDFloatLayout:
            size_hint: .7, .07
            pos_hint: {"center_x": .5, "center_y": .63}
            TextInput:
                id: email
                hint_text: "Email"
                font_name: "MPoppins-Medium"
                size_hint_y: .75
                pos_hint: {"center_x": .43, "center_y": .25}
                background_color: 1, 1, 1, 0
                foreground_color: rgba(0, 0, 59, 255)
                cursor_color: rgba(0, 0, 59, 255)
                font_size: "14sp"
                cursor_width: "2sp"
                helper_text: "Required"
                helper_text_mode: "on_error"
                multiline: False
                required: True

        MDFloatLayout:
            md_bg_color: rgba(178, 178, 178, 255)
            size_hint: .8, .002
            pos_hint: {"center_x": .5, "center_y": .59}

        MDFloatLayout:
            size_hint: .7, .07
            pos_hint: {"center_x": .5, "center_y": .5}
            TextInput:
                id: password
                hint_text: "Password"
                font_name: "MPoppins-Medium"
                size_hint_y: .75
                pos_hint: {"center_x": .43, "center_y": .28}
                background_color: 1, 1, 1, 0
                foreground_color: rgba(0, 0, 59, 255)
                cursor_color: rgba(0, 0, 59, 255)
                font_size: "14sp"
                cursor_width: "2sp"
                multiline: False
                password: True

        MDFloatLayout:
            md_bg_color: rgba(178, 178, 178, 255)
            size_hint: .8, .002
            pos_hint: {"center_x": .5, "center_y": .46}

        MDFillRoundFlatIconButton:
            text: "LOGIN"
            pos_hint: {"center_x": .5, "center_y": .35}
            font_name: "MPoppins-SemiBold"
            size_hint: .75, .065
            on_release:
                root.login_user(email.text, password.text)  # Use login_user method here

        MDTextButton:
            text: "Forgot Password"
            pos_hint: {"center_x": .5, "center_y": .28}
            color: rgba(68, 78, 132, 255)
            font_size: "12sp"
            font_name: "MPoppins-SemiBold"

        MDLabel:
            text: "or"
            color: rgba(52, 0, 231, 255)
            pos_hint: {"center_y": .22}
            font_size: "13sp"
            font_name: "MPoppins-SemiBold"
            halign: "center"

        MDFloatLayout:
            md_bg_color: rgba(178, 178, 178, 255)
            size_hint: .3, .002
            pos_hint: {"center_x": .3, "center_y": .218}

        MDFloatLayout:
            md_bg_color: rgba(178, 178, 178, 255)
            size_hint: .3, .002
            pos_hint: {"center_x": .7, "center_y": .218}

        MDLabel:
            text: "Social Media Login"
            font_name: "MPoppins-SemiBold"
            font_size: "13sp"
            halign: "center"
            pos_hint: {"center_y": .16}
            color: rgba(135, 133, 193, 255)

        MDGridLayout:
            cols: 3
            size_hint: .30, .10
            pos_hint: {"center_x": .5, "center_y": .1}
            Image:
                source: "google.png"
            Image:
                source: "facebook.png"
            Image:
                source: "apple.png"

        MDLabel:
            text: "Don't have an account?"
            font_name: "MPoppins-SemiBold"
            font_size: "11sp"
            pos_hint: {"center_x": .68, "center_y": .04}
            color: rgba(135, 133, 193, 255)

        MDTextButton:
            text: "Sign up"
            font_name: "MPoppins-SemiBold"
            font_size: "11sp"
            pos_hint: {"center_x": .75, "center_y": .04}
            color: rgba(52, 0, 231, 255)
            on_release:
                app.root.current = "register"

<RegisterPage>:
    MDFloatLayout:
        md_bg_color: 1, 1, 1, 1
        MDIconButton:
            icon: "arrow-left"
            pos_hint: {"center_y": .95}
            user_font_size: "30sp"
            theme_text_color: "Custom"
            text_color: rgba(26, 24, 58, 255)
            on_release:
                app.root.current = "login"

        MDLabel:
            text: " W E L C O M E !"
            font_name: "MPoppins-SemiBold"
            font_size: "26sp"
            pos_hint: {"center_x": .7, "center_y": .90}
            color: rgba(0, 0, 59, 255)

        MDLabel:
            text: "      R e g i s t e r   y o u r  a c c o u n t"
            font_name: "MPoppins-SemiBold"
            font_size: "16sp"
            pos_hint: {"center_x": .5, "center_y": .85}
            color: rgba(135, 133, 193, 255)

        MDFloatLayout:
            size_hint: .7, .07
            pos_hint: {"center_x": .5, "center_y": .75}
            TextInput:
                id: username
                hint_text: "Username"
                font_name: "MPoppins-Medium"
                size_hint_y: .75
                pos_hint: {"center_x": .43, "center_y": .25}
                background_color: 1, 1, 1, 0
                foreground_color: rgba(0, 0, 59, 255)
                cursor_color: rgba(0, 0, 59, 255)
                font_size: "14sp"
                cursor_width: "2sp"
                helper_text: "Required"
                helper_text_mode: "on_error"
                multiline: False
                required: True

        MDFloatLayout:
            md_bg_color: rgba(178, 178, 178, 255)
            size_hint: .8, .002
            pos_hint: {"center_x": .5, "center_y": .70}

        MDFloatLayout:
            size_hint: .7, .07
            pos_hint: {"center_x": .5, "center_y": .63}
            TextInput:
                id: email
                hint_text: "Email"
                font_name: "MPoppins-Medium"
                size_hint_y: .75
                pos_hint: {"center_x": .43, "center_y": .60}
                background_color: 1, 1, 1, 0
                foreground_color: rgba(0, 0, 59, 255)
                cursor_color: rgba(0, 0, 59, 255)
                font_size: "14sp"
                cursor_width: "2sp"
                helper_text: "Required"
                helper_text_mode: "on_error"
                multiline: False
                required: True

        MDFloatLayout:
            md_bg_color: rgba(178, 178, 178, 255)
            size_hint: .8, .002
            pos_hint: {"center_x": .5, "center_y": .60}

        MDFloatLayout:
            size_hint: .7, .07
            pos_hint: {"center_x": .5, "center_y": .56}
            TextInput:
                id: password
                hint_text: "Password"
                font_name: "MPoppins-Medium"
                size_hint_y: .75
                pos_hint: {"center_x": .43, "center_y": .28}
                background_color: 1, 1, 1, 0
                foreground_color: rgba(0, 0, 59, 255)
                cursor_color: rgba(0, 0, 59, 255)
                font_size: "14sp"
                cursor_width: "2sp"
                helper_text: "Required"
                helper_text_mode: "on_error"
                multiline: False
                password: True
                required: True

        MDFloatLayout:
            md_bg_color: rgba(178, 178, 178, 255)
            size_hint: .8, .002
            pos_hint: {"center_x": .5, "center_y": .50}

        MDFloatLayout:
            size_hint: .7, .07
            pos_hint: {"center_x": .5, "center_y": .45}
            TextInput:
                id: confirm_password
                hint_text: "Confirm Password"
                font_name: "MPoppins-Medium"
                size_hint_y: .75
                pos_hint: {"center_x": .43, "center_y": .28}
                background_color: 1, 1, 1, 0
                foreground_color: rgba(0, 0, 59, 255)
                cursor_color: rgba(0, 0, 59, 255)
                font_size: "14sp"
                cursor_width: "2sp"
                helper_text: "Required"
                helper_text_mode: "on_error"
                multiline: False
                password: True
                required: True

        MDFloatLayout:
            md_bg_color: rgba(178, 178, 178, 255)
            size_hint: .8, .002
            pos_hint: {"center_x": .5, "center_y": .39}

        MDFillRoundFlatIconButton:
            text: "REGISTER"
            pos_hint: {"center_x": .5, "center_y": .30}
            font_name: "MPoppins-SemiBold"
            size_hint: .75, .065
            on_release:
                root.register_user(
                root.ids.username.text, root.ids.email.text, root.ids.password.text, root.ids.confirm_password.text)

    MDLabel:
        text: "or"
        color: rgba(52, 0, 231, 255)
        pos_hint: {"center_y": .23}
        font_size: "13sp"
        font_name: "MPoppins-SemiBold"
        halign: "center"

    MDFloatLayout:
        md_bg_color: rgba(178, 178, 178, 255)
        size_hint: .3, .002
        pos_hint: {"center_x": .3, "center_y": .22}

    MDFloatLayout:
        md_bg_color: rgba(178, 178, 178, 255)
        size_hint: .3, .002
        pos_hint: {"center_x": .7, "center_y": .22}

    MDLabel:
        text: "Social Media Login"
        font_name: "MPoppins-SemiBold"
        font_size: "13sp"
        halign: "center"
        pos_hint: {"center_y": .18}
        color: rgba(135, 133, 193, 255)

    MDGridLayout:
        cols: 3
        size_hint: .30, .10
        pos_hint: {"center_x": .5, "center_y": .12}
        Image:
            source: "google.png"
        Image:
            source: "facebook.png"
        Image:
            source: "apple.png"
    MDLabel:
        text: "Already have an account?        "
        font_name: "MPoppins-SemiBold"
        font_size: "11sp"
        pos_hint: {"center_x": .68, "center_y": .05}
        color: rgba(135, 133, 193, 255)

    MDTextButton:
        text: "       Sign in"
        font_name: "MPoppins-SemiBold"
        font_size: "11sp"
        pos_hint: {"center_x": .75, "center_y": .05}
        color: rgba(52, 0, 231, 255)
        on_release:
            app.root.current = "login"
           
<FinalPage>:
    name: 'final'
    
    
            
"""


class MainScreen(Screen):
    pass


class LoginPage(Screen):
    def login_user(self, email, password):
        # Validate email and password
        if not self.is_valid_email(email) or not self.is_strong_password(password):
            self.show_error_popup("Invalid Credentials", "Invalid email or password.")
            return

        try:
            # Retrieve user data from Firebase Realtime Database
            response = requests.get(FIREBASE_URL + '/users.json')
            if response.ok:
                user_data = response.json()
                for key, data in user_data.items():
                    if data.get('email') == email and data.get('password') == password:
                        print("Login successful!")
                        self.manager.current = "final"
                        return

            self.show_error_popup("Login Failed", "Invalid email or password.")
        except Exception as e:
            self.show_error_popup("Login Failed", "An error occurred during login.")
            print("Login failed. Error:", e)

    def is_valid_email(self, email):
        # Simple regex-based email validation
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(email_pattern, email)

    def is_strong_password(self, password):
        # Check if the password is strong (contains uppercase, lowercase, and digit) and at least 8 characters long.
        return any(c.isupper() for c in password) and any(c.islower() for c in password) and any(
            c.isdigit() for c in password) and len(password) >= 8

    def show_error_popup(self, title, text):
        dialog = MDDialog(
            title=title,
            text=text,
            buttons=[
                MDFlatButton(
                    text="OK", on_release=lambda x: dialog.dismiss()
                )
            ],
        )
        dialog.open()


class RegisterPage(Screen):
    class RegisterPage(Screen):
        def register_user(self, username, email, password, confirm_password):
            if password == confirm_password:
                try:
                    # Validate email
                    if not self.is_valid_email(email):
                        self.show_popup("Invalid email format.")
                        return

                    # Validate password
                    if not self.is_strong_password(password):
                        self.show_popup(
                            "Password must be at least 8 characters long and contain uppercase, lowercase, and digit.")
                        return

                    # Data to be sent
                    data = {
                        'username': username,
                        'email': email,
                        'password': password
                    }

                    # Send data to Firebase Realtime Database
                    response = requests.post(FIREBASE_URL + '/users.json', json=data)

                    if response.ok:
                        self.show_popup("User registered successfully!")
                    else:
                        self.show_popup("Failed to register user.")
                except Exception as e:
                    self.show_popup(f"Registration failed.: {e}")
            else:
                self.show_popup("Password and Confirm Password do not match.")

        def is_valid_email(self, email):
            # Simple regex-based email validation
            email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
            return re.match(email_pattern, email)

        def is_strong_password(self, password):
            # Check if the password is strong (contains uppercase, lowercase, and digit) and at least 8 characters long.
            return any(c.isupper() for c in password) and any(c.islower() for c in password) and any(
                c.isdigit() for c in password) and len(password) >= 8

        def show_popup(self, message):
            ok_button = MDFlatButton(text="OK", on_release=self.close_popup)
            self.popup = MDDialog(title="", text=message, size_hint=(0.7, 0.2), buttons=[ok_button])
            self.popup.open()

        def close_popup(self, *args):
            if hasattr(self, "popup") and self.popup:
                self.popup.dismiss()


class FinalPage(Screen):
    class ImageLabel(BoxLayout):
        def __init__(self, **kwargs):
            super(FinalPage.ImageLabel, self).__init__(**kwargs)
            self.orientation = 'vertical'
            self.images_folder = 'letters'
            self.image_widget = KivyImage(allow_stretch=True, anim_delay=1 / 30)  # Adjust the animation delay as needed

        def display_image(self, image_path):
            if os.path.exists(image_path):
                self.clear_widgets()
                self.add_widget(self.image_widget)
                self.image_widget.source = image_path

    class OutputLabel(ScrollView):
        def __init__(self, **kwargs):
            super(FinalPage.OutputLabel, self).__init__(**kwargs)
            self.add_widget(MDLabel(halign='center', theme_text_color='Secondary'))

    def __init__(self, **kwargs):
        super(FinalPage, self).__init__(**kwargs)
        self.r = sr.Recognizer()
        self.audio_file = "temp.wav"  # Set the audio file name here
        self.rate = 44100
        self.chunk = 1024
        self.audio_format = pyaudio.paInt16
        self.channels = 1
        self.record_seconds = 5
        self.isl_gif = [
            'any questions', 'are you angry', 'are you busy', 'are you hungry', 'are you sick', 'be careful',
            'can we meet tomorrow', 'did you book tickets', 'did you finish homework', 'do you go to office',
            'do you have money',
            'do you want something to drink', 'do you want tea or coffee', 'do you watch TV', 'dont worry',
            'flower is beautiful',
            'good afternoon', 'good evening', 'good morning', 'good night', 'good question', 'had your lunch',
            'happy journey',
            'hello what is your name', 'how many people are there in your family', 'i am a clerk',
            'i am bore doing nothing',
            'i am fine', 'i am sorry', 'i am thinking', 'i am tired', 'i dont understand anything', 'i go to a theatre',
            'i love to shop',
            'i had to say something but i forgot', 'i have headache', 'i like pink colour', 'i live in nagpur',
            'lets go for lunch', 'my mother is a homemaker',
            'my name is john', 'nice to meet you', 'no smoking please', 'open the door', 'please call me later',
            'please clean the room', 'please give me your pen', 'please use dustbin dont throw garbage',
            'please wait for sometime', 'shall I help you',
            'shall we go together tommorow', 'sign language interpreter', 'sit down', 'stand up', 'take care',
            'there was traffic jam', 'wait I am thinking',
            'what are you doing', 'what is the problem', 'what is todays date', 'what is your father do',
            'what is your job',
            'what is your mobile number', 'what is your name', 'whats up', 'when is your interview', 'when we will go',
            'where do you stay',
            'where is the bathroom', 'where is the police station', 'you are wrong', 'address', 'agra', 'ahemdabad',
            'all', 'april', 'assam', 'august', 'australia', 'badoda', 'banana', 'banaras', 'banglore',
            'bihar', 'bihar', 'bridge', 'cat', 'chandigarh', 'chennai', 'christmas', 'church', 'clinic', 'coconut',
            'crocodile', 'dasara',
            'deaf', 'december', 'deer', 'delhi', 'dollar', 'duck', 'febuary', 'friday', 'fruits', 'glass', 'grapes',
            'gujrat', 'hello',
            'hindu', 'hyderabad', 'india', 'january', 'jesus', 'job', 'july', 'july', 'karnataka', 'kerala', 'krishna',
            'litre', 'mango',
            'may', 'mile', 'monday', 'mumbai', 'museum', 'muslim', 'nagpur', 'october', 'orange', 'pakistan', 'pass',
            'police station',
            'post office', 'pune', 'punjab', 'rajasthan', 'ram', 'restaurant', 'saturday', 'september', 'shop', 'sleep',
            'southafrica',
            'story', 'sunday', 'tamil nadu', 'temperature', 'temple', 'thursday', 'toilet', 'tomato', 'town', 'tuesday',
            'usa', 'village',
            'voice', 'wednesday', 'weight', 'please wait for sometime', 'what is your mobile number',
            'what are you doing', 'are you busy'
        ]

        self.arr = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                    'u', 'v', 'w', 'x', 'y', 'z']
        self.image_label = self.ImageLabel(size_hint_y=None, height=300)
        self.output_label = self.OutputLabel(size_hint_y=None, height=400)
        self.entered_text_label = MDLabel(halign='center', theme_text_color='Secondary', font_style='H6')
        self.display_text = ""

        layout = BoxLayout(orientation='vertical', spacing='16dp', padding='16dp')

        mic_icon = MDIconButton(icon="microphone", pos_hint={'center_x': 0.5})
        mic_icon.md_bg_color_disabled = [0, 0, 0, 0]
        mic_icon.bind(on_release=self.start_listening_with_popup)
        layout.add_widget(mic_icon)

        self.text_input = MDTextField(hint_text="Text Input", multiline=False, size_hint=(None, None), width='250dp',
                                      height='40dp')
        layout.add_widget(self.text_input)

        button = MDRaisedButton(text="Process Input", on_release=self.process_input, size_hint=(None, None),
                                width='200dp', height='50dp')
        layout.add_widget(button)

        scroll_image = ScrollView(size_hint=(1, None), size=(300, 300))
        scroll_image.add_widget(self.image_label)
        layout.add_widget(scroll_image)

        scroll_output = ScrollView()
        scroll_output.add_widget(self.output_label)
        layout.add_widget(scroll_output)

        layout.add_widget(self.entered_text_label)

        self.add_widget(layout)

    def process_input(self, *args):
        text_input = self.text_input.text.strip()

        if text_input:
            output = self.process_text_input(text_input)
            self.entered_text_label.text = "You said: " + text_input
        else:
            output = "Please enter text input."

        self.output_label.children[0].text = output
        self.text_input.text = ""

    def process_text_input(self, text_input):
        output = ""
        for c in string.punctuation:
            text_input = text_input.replace(c, "")
        gif_filename = text_input.replace(" ", "_")
        gif_filepath = os.path.join('ISL_Gifs', '{}.gif'.format(gif_filename))

        if os.path.exists(gif_filepath):
            self.display_image(gif_filepath)
        else:
            images_to_display = []
            for char in text_input:
                if char in self.arr:
                    image_path = 'letters/{}.jpg'.format(char)
                    images_to_display.append(image_path)
            if images_to_display:
                self.display_images_one_by_one(images_to_display)
                self.display_text = text_input

        return output

    def display_image(self, image_path):
        if os.path.exists(image_path):
            self.image_label.display_image(image_path)

    def display_images_one_by_one(self, images_to_display):
        self.current_image_index = 0
        self.images_to_display = images_to_display
        self.display_image(images_to_display[self.current_image_index])
        Clock.schedule_interval(self.update_image, 1)

    def update_image(self, dt):
        self.current_image_index += 1
        if self.current_image_index < len(self.images_to_display):
            self.display_image(self.images_to_display[self.current_image_index])
        else:
            Clock.unschedule(self.update_image)
            self.display_entered_text()

    def display_entered_text(self):
        self.entered_text_label.text = "You said: " + self.display_text

    def start_listening_with_popup(self, *args):
        self.show_listening_popup()
        Clock.schedule_once(lambda dt: self.start_listening(), 0.3)

    def show_listening_popup(self):
        popup = MDDialog(title="Listening", text="I am listening...", auto_dismiss=False)
        popup.open()
        Clock.schedule_once(lambda dt: self.dismiss_popup(popup), 5)

    def dismiss_popup(self, popup):
        popup.dismiss()

    def start_listening(self):
        self.output_label.children[0].text = "I am listening..."

        audio = pyaudio.PyAudio()
        stream = audio.open(format=self.audio_format, channels=self.channels,
                            rate=self.rate, input=True, frames_per_buffer=self.chunk)
        frames = []

        for i in range(int(self.rate / self.chunk * self.record_seconds)):
            data = stream.read(self.chunk)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        audio.terminate()

        with wave.open(self.audio_file, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(audio.get_sample_size(self.audio_format))
            wf.setframerate(self.rate)
            wf.writeframes(b''.join(frames))

        with sr.AudioFile(self.audio_file) as source:
            audio = self.r.listen(source, timeout=self.record_seconds)

        self.on_finish_listen(None, audio)

    def on_finish_listen(self, recognizer, audio):
        try:
            a = self.r.recognize_google(audio).lower()
            print('You Said:', a)
            self.text_input.text = a
            self.display_text = a
            self.process_input()
        except sr.UnknownValueError:
            print("Could not understand audio.")
            self.show_popup_message("Couldn't understand your voice")
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
            self.show_popup_message("Error occurred while processing voice input. Please try again.")
        finally:
            self.output_label.children[0].text = ""

    def show_popup_message(self, message):
        popup_layout = BoxLayout(orientation='vertical', spacing='10dp', padding='10dp')
        popup_label = Label(text=message, font_size=16, halign='center')
        popup_button = Button(text="Try Again", size_hint=(None, None), size=('150dp', '40dp'))
        popup_layout.add_widget(popup_label)
        popup_layout.add_widget(popup_button)

        popup = Popup(title='Voice Input Error',
                      content=popup_layout,
                      size_hint=(None, None), size=('300dp', '200dp'))
        popup_button.bind(on_release=popup.dismiss)
        popup.open()

class SathiApp(MDApp):
    def build(self):
        # Register custom fonts
        self.icon="sathi-logo1.png"
        LabelBase.register(name="MPoppins-Medium", fn_regular="Poppins-Medium.ttf")
        LabelBase.register(name="MPoppins-SemiBold", fn_regular="Poppins-SemiBold.ttf")

        return Builder.load_string(kv)


if __name__ == "__main__":
    SathiApp().run()
