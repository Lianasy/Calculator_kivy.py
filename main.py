from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.label import Label

Builder.load_string("""
<CustomButton>:
    background_color: (0, 0.5, 0.7, 1)  # button background color
    color: (1, 1, 1, 1)  # button text color
    font_size: '30sp'  # font size

<CustomTextInput>:
    background_color: (0, 0.4353, 0.6392)  # text input background color
    foreground_color: (1, 1, 1, 1)  # text input text color
    font_size: '50sp'  # font size
""")


# Classes for buttons with modified styles
class CustomButton(Button):
    pass


class CustomTextInput(TextInput):
    pass


class ButtonHandler:
    def __init__(self, symbols, point):
        self.point = point
        self.symbols = symbols

    def handle_digit_button(self, digit, text_input):
        # Logic for buttons with numbers
        current_text = text_input.text
        if len(current_text) == 1 and current_text[0] == '0':
            return
        elif len(current_text) > 0 and current_text[len(current_text) - 1] == '0' and current_text[
            len(current_text) - 2] in self.symbols:
            return
        text_input.text += str(digit)

    def handle_operator_button(self, operator, text_input):
        # Logic for buttons with operators
        current_text = text_input.text
        if len(current_text) > 0 and current_text[len(current_text) - 1].isdigit():
            text_input.text += operator

    def handle_point_button(self, text_input):
        # Logic for the button with a decimal point
        current_text = text_input.text
        # Look back to the beginning of the number or appearance of an operator
        i = len(current_text) - 1
        if current_text[i] in self.symbols:
            return
        while i >= 0:
            if current_text[i] in self.symbols:
                break
            if current_text[i] == self.point:
                return  # If a decimal point is found in the number, return without adding a new one
            i -= 1

        text_input.text += '.'

    def handle_equals_button(self, text_input):
        # Logic for the "equals" button
        current_text = text_input.text
        if len(current_text) > 0 and current_text[len(current_text) - 1] in self.symbols:
            text_input.text = text_input.text[:-1]
        try:
            result = eval(text_input.text)
            text_input.text = str(result)
        except:
            text_input.text = "Error"

    def handle_backspace_button(self, text_input):
        # Logic for the "backspace" button
        if text_input.text:
            text_input.text = text_input.text[:-1]

    def handle_clear_button(self, text_input):
        # Logic for the "clear" button
        text_input.text = ""


class CalculatorApp(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = None
        self.operators = ['+', '-', '*', '/']
        self.point = '.'
        self.button_handler = ButtonHandler(self.operators, self.point)
        self.equаl = '='
        self.backspace = 'Backspace'
        self.AC = 'AC'

    def build(self):
        spacing_percent = 0.01  # 1% of the window width
        spacing = Window.width * spacing_percent
        root = BoxLayout(orientation='vertical', padding=(spacing, spacing, spacing, spacing))
        text_input = CustomTextInput()
        text_input.readonly = True
        text_input.size_hint_y = 0.2  # Occupies 10% of the vertical space
        root.add_widget(text_input)
        self.text = text_input
        # Create number buttons
        buttons_layout = GridLayout(cols=4, size_hint_y=0.8, spacing=spacing, padding=(0, spacing, 0, 0))
        for i in range(10):
            button = CustomButton(text=str(i))
            button.bind(on_press=self.on_button_press)
            buttons_layout.add_widget(button)
        button = CustomButton(text='.')
        button.bind(on_press=self.on_button_press)
        buttons_layout.add_widget(button)
        # Create operator buttons
        for operator in self.operators:
            button = CustomButton(text=operator)
            button.bind(on_press=self.on_button_press)
            buttons_layout.add_widget(button)
        else_buttons = [self.equаl, '', self.backspace, self.AC]
        else_button: str
        for else_button in else_buttons:
            if else_button == '':
                empty_widget = Label(size_hint=(None, None), size=(0, 0))
                buttons_layout.add_widget(empty_widget)
                continue
            if else_button == self.backspace:
                button = Button(text=" ",
                             background_normal='buttonbackspace.png',
                             size_hint=(.3, .3),
                             pos_hint={"x": 0.35, "y": 0.3}
                             )
                button.bind(on_press=self.on_button_press)
                buttons_layout.add_widget(button)
                continue
            button = CustomButton(text=else_button)
            button.bind(on_press=self.on_button_press)
            buttons_layout.add_widget(button)
        root.add_widget(buttons_layout)
        return root

    def on_button_press(self, instance):
        # Handle button press events
        button_text = instance.text
        if button_text.isdigit():
            self.button_handler.handle_digit_button(int(button_text), self.text)
        elif button_text in self.operators:
            self.button_handler.handle_operator_button(button_text, self.text)
        elif button_text == self.point:
            self.button_handler.handle_point_button(self.text)
        elif button_text == self.equаl:
            self.button_handler.handle_equals_button(self.text)
        elif button_text == ' ':
            self.button_handler.handle_backspace_button(self.text)
        elif button_text == self.AC:
            self.button_handler.handle_clear_button(self.text)
        else:
            # Possibility to add logic for other buttons
            pass


if __name__ == '__main__':
    CalculatorApp().run()
