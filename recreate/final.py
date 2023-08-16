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


class ImageLabel(BoxLayout):
    def __init__(self, **kwargs):
        super(ImageLabel, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.images_folder = 'letters'
        self.image_widget = KivyImage(allow_stretch=True, anim_delay=1 / 30)  # Adjust the animation delay as needed

    def display_image(self, image_path):
        if os.path.exists(image_path):
            self.clear_widgets()
            self.add_widget(self.image_widget)
            self.image_widget.source = image_path


class MainApp(MDApp):
    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)
        self.r = sr.Recognizer()
        self.audio_file = "temp.wav"  # Set the audio file name here
        self.rate = 44100
        self.chunk = 1024
        self.audio_format = pyaudio.paInt16
        self.channels = 1
        self.record_seconds = 5
        self.isl_gif = [
            'any questions', 'are you angry', 'are you busy', 'are you hungry', 'are you sick', 'be careful',
                'can we meet tomorrow', 'did you book tickets', 'did you finish homework', 'do you go to office', 'do you have money',
                'do you want something to drink', 'do you want tea or coffee', 'do you watch TV', 'dont worry', 'flower is beautiful',
                'good afternoon', 'good evening', 'good morning', 'good night', 'good question', 'had your lunch', 'happy journey',
                'hello what is your name', 'how many people are there in your family', 'i am a clerk', 'i am bore doing nothing',
                 'i am fine', 'i am sorry', 'i am thinking', 'i am tired', 'i dont understand anything', 'i go to a theatre', 'i love to shop',
                'i had to say something but i forgot', 'i have headache', 'i like pink colour', 'i live in nagpur', 'lets go for lunch', 'my mother is a homemaker',
                'my name is john', 'nice to meet you', 'no smoking please', 'open the door', 'please call me later',
                'please clean the room', 'please give me your pen', 'please use dustbin dont throw garbage', 'please wait for sometime', 'shall I help you',
                'shall we go together tommorow', 'sign language interpreter', 'sit down', 'stand up', 'take care', 'there was traffic jam', 'wait I am thinking',
                'what are you doing', 'what is the problem', 'what is todays date', 'what is your father do', 'what is your job',
                'what is your mobile number', 'what is your name', 'whats up', 'when is your interview', 'when we will go', 'where do you stay',
                'where is the bathroom', 'where is the police station', 'you are wrong','address','agra','ahemdabad', 'all', 'april', 'assam', 'august', 'australia', 'badoda', 'banana', 'banaras', 'banglore',
'bihar','bihar','bridge','cat', 'chandigarh', 'chennai', 'christmas', 'church', 'clinic', 'coconut', 'crocodile','dasara',
'deaf', 'december', 'deer', 'delhi', 'dollar', 'duck', 'febuary', 'friday', 'fruits', 'glass', 'grapes', 'gujrat', 'hello',
'hindu', 'hyderabad', 'india', 'january', 'jesus', 'job', 'july', 'july', 'karnataka', 'kerala', 'krishna', 'litre', 'mango',
'may', 'mile', 'monday', 'mumbai', 'museum', 'muslim', 'nagpur', 'october', 'orange', 'pakistan', 'pass', 'police station',
'post office', 'pune', 'punjab', 'rajasthan', 'ram', 'restaurant', 'saturday', 'september', 'shop', 'sleep', 'southafrica',
'story', 'sunday', 'tamil nadu', 'temperature', 'temple', 'thursday', 'toilet', 'tomato', 'town', 'tuesday', 'usa', 'village',
'voice', 'wednesday', 'weight','please wait for sometime','what is your mobile number','what are you doing','are you busy']

        self.arr = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                    'u', 'v', 'w', 'x', 'y', 'z']
        self.image_label = ImageLabel(size_hint_y=None, height=300)
        self.output_label = MDLabel(halign='center', theme_text_color='Secondary',
                                    text="")  # Set a default value for the label text
        self.entered_text_label = MDLabel(halign='center', theme_text_color='Secondary', font_style='H6')
        self.display_text = ""

    def build(self):
        layout = BoxLayout(orientation='vertical', spacing='16dp', padding='16dp')

        # Replace the text field with a microphone icon
        mic_icon = MDIconButton(icon="microphone", pos_hint={'center_x': 0.5})
        mic_icon.md_bg_color_disabled = [0, 0, 0, 0]  # Set the background color to transparent
        mic_icon.bind(on_release=self.start_listening_with_popup)  # Call the function with the popup message
        layout.add_widget(mic_icon)

        self.text_input = MDTextField(hint_text="Text Input", multiline=False, size_hint=(None, None), width='250dp',
                                      height='40dp')
        layout.add_widget(self.text_input)

        button = MDRaisedButton(text="Process Input", on_release=self.process_input, size_hint=(None, None),
                                width='200dp', height='50dp')
        layout.add_widget(button)

        # Use ScrollView for the image_label
        scroll_image = ScrollView(size_hint=(1, None), size=(300, 300))
        scroll_image.add_widget(self.image_label)
        layout.add_widget(scroll_image)

        # Use ScrollView for the output_label
        scroll_output = ScrollView()
        scroll_output.add_widget(self.output_label)
        layout.add_widget(scroll_output)

        # Add the label for displaying entered text
        layout.add_widget(self.entered_text_label)

        return layout

    def process_input(self, *args):
        text_input = self.text_input.text.strip()

        if text_input:
            output = self.process_text_input(text_input)
            self.entered_text_label.text = "You said: " + text_input
        else:
            output = "Please enter text input."

        self.output_label.text = output

        self.text_input.text = ""

    def process_text_input(self, text_input):
        output = ""
        for c in string.punctuation:
            text_input = text_input.replace(c, "")
        gif_filename = text_input.replace(" ", "_")
        gif_filepath = os.path.join('ISL_Gifs', '{}.gif'.format(gif_filename))

        if os.path.exists(gif_filepath):
            # output = "You said: {}".format(text_input)
            self.display_image(gif_filepath)
        else:
            images_to_display = []
            for char in text_input:
                if char in self.arr:
                    image_path = 'letters/{}.jpg'.format(char)
                    images_to_display.append(image_path)
            if images_to_display:
                self.display_images_one_by_one(images_to_display)  # Display images one by one
                self.display_text = text_input  # Store the entered text for display after images

        return output

    def display_image(self, image_path):
        if os.path.exists(image_path):
            self.image_label.display_image(image_path)

    def display_images_one_by_one(self, images_to_display):
        self.current_image_index = 0
        self.images_to_display = images_to_display
        self.display_image(images_to_display[self.current_image_index])
        Clock.schedule_interval(self.update_image, 1)  # Change image every 1 second

    def update_image(self, dt):
        self.current_image_index += 1
        if self.current_image_index < len(self.images_to_display):
            self.display_image(self.images_to_display[self.current_image_index])
        else:
            Clock.unschedule(self.update_image)  # Stop updating images
            self.display_entered_text()

    def display_entered_text(self):
        self.entered_text_label.text = "You said: " + self.display_text

    def start_listening_with_popup(self, *args):
        # Show the listening popup for 5 seconds
        self.show_listening_popup()
        # Start listening for audio after showing the popup
        Clock.schedule_once(lambda dt: self.start_listening(), 0.3)

    def show_listening_popup(self):
        # Create and open the popup
        popup = MDDialog(title="Listening", text="I am listening...", auto_dismiss=False)
        popup.open()

        # Schedule a callback to dismiss the popup after 5 seconds
        Clock.schedule_once(lambda dt: self.dismiss_popup(popup), 5)

    def dismiss_popup(self, popup):
        popup.dismiss()

    def start_listening(self):
        self.output_label.text = "I am listening..."

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

        self.on_finish_listen(None, audio)  # Call the recognition function explicitly

    def on_finish_listen(self, recognizer, audio):
        try:
            a = self.r.recognize_google(audio).lower()
            print('You Said:', a)
            self.text_input.text = a
            self.display_text = a  # Store the entered text
            self.process_input()
        except sr.UnknownValueError:
            print("Could not understand audio.")
            self.show_popup_message("Couldn't understand your voice")

        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
            self.show_popup_message("Error occurred while processing voice input. Please try again.")
        finally:
            # Revert the label back to its default value
            self.output_label.text = ""

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

if __name__ == "__main__":
    MainApp().run()
