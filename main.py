from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.storage.jsonstore import JsonStore
from datetime import datetime, timedelta
import os

class DaysSinceApp(App):
    def __init__(self):
        super().__init__()
        self.store = JsonStore('days_since_data.json')
        self.saved_date = None
        self.days_label = None
        self.hours_label = None
        self.years_label = None
        
    def build(self):
        # Set window size for testing (will be fullscreen on Android)
        Window.size = (400, 600)
        
        # Load saved date
        self.load_date()
        
        # Main layout
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # Header
        header = Label(
            text='Days since we met',
            font_size='24sp',
            bold=True,
            color=(0.22, 0.69, 0.0, 1.0),  # Green color
            size_hint_y=None,
            height=50
        )
        layout.add_widget(header)
        
        # Days label
        self.days_label = Label(
            text='Select a date to begin',
            font_size='48sp',
            bold=True,
            color=(0.13, 0.13, 0.13, 1.0),  # Dark text
            size_hint_y=None,
            height=100
        )
        layout.add_widget(self.days_label)
        
        # Hours label
        self.hours_label = Label(
            text='',
            font_size='24sp',
            color=(0.13, 0.13, 0.13, 1.0),
            size_hint_y=None,
            height=50
        )
        layout.add_widget(self.hours_label)
        
        # Years label
        self.years_label = Label(
            text='',
            font_size='24sp',
            color=(0.13, 0.13, 0.13, 1.0),
            size_hint_y=None,
            height=50
        )
        layout.add_widget(self.years_label)
        
        # Spacer
        layout.add_widget(Label(size_hint_y=1))
        
        # Change date button
        change_btn = Button(
            text='Change Date',
            size_hint_y=None,
            height=60,
            background_color=(0.22, 0.69, 0.0, 1.0),  # Green
            color=(1, 1, 1, 1)  # White text
        )
        change_btn.bind(on_press=self.show_date_popup)
        layout.add_widget(change_btn)
        
        # Update time every second
        Clock.schedule_interval(self.update_time, 1.0)
        
        return layout
    
    def load_date(self):
        """Load saved date from storage"""
        if self.store.exists('date'):
            try:
                date_str = self.store.get('date')['value']
                self.saved_date = datetime.strptime(date_str, '%Y-%m-%d')
            except:
                self.saved_date = None
        else:
            self.saved_date = None
    
    def save_date(self, date):
        """Save date to storage"""
        self.saved_date = date
        self.store.put('date', value=date.strftime('%Y-%m-%d'))
    
    def show_date_popup(self, instance):
        """Show popup to enter date"""
        content = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Instructions
        instruction = Label(
            text='Enter the special date (YYYY-MM-DD):',
            size_hint_y=None,
            height=30
        )
        content.add_widget(instruction)
        
        # Date input
        date_input = TextInput(
            text='',
            multiline=False,
            size_hint_y=None,
            height=40
        )
        content.add_widget(date_input)
        
        # Buttons
        button_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=40)
        
        def save_date(instance):
            try:
                date_str = date_input.text.strip()
                if date_str:
                    date = datetime.strptime(date_str, '%Y-%m-%d')
                    self.save_date(date)
                    self.update_time()
                    popup.dismiss()
                else:
                    # Show error
                    error_popup = Popup(
                        title='Error',
                        content=Label(text='Please enter a valid date'),
                        size_hint=(None, None),
                        size=(300, 150)
                    )
                    error_popup.open()
            except ValueError:
                # Show error
                error_popup = Popup(
                    title='Error',
                    content=Label(text='Please enter a valid date in YYYY-MM-DD format'),
                    size_hint=(None, None),
                    size=(300, 150)
                )
                error_popup.open()
        
        def cancel(instance):
            popup.dismiss()
        
        save_btn = Button(text='Save', on_press=save_date)
        cancel_btn = Button(text='Cancel', on_press=cancel)
        
        button_layout.add_widget(save_btn)
        button_layout.add_widget(cancel_btn)
        content.add_widget(button_layout)
        
        # Create popup
        popup = Popup(
            title='Select Date',
            content=content,
            size_hint=(None, None),
            size=(350, 200)
        )
        popup.open()
    
    def update_time(self, dt=None):
        """Update the displayed time"""
        if not self.saved_date:
            self.days_label.text = 'Select a date to begin'
            self.hours_label.text = ''
            self.years_label.text = ''
            return
        
        now = datetime.now()
        delta = now - self.saved_date
        
        days = delta.days
        hours = int(delta.total_seconds() // 3600)
        years = delta.total_seconds() / (365.2425 * 24 * 3600)
        
        self.days_label.text = f'{days} days'
        self.hours_label.text = f'{hours} hours'
        self.years_label.text = f'{years:.2f} years'

if __name__ == '__main__':
    DaysSinceApp().run() 