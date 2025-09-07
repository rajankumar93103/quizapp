import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
import json

# Load questions from JSON file
with open("questions.json", "r", encoding="utf-8") as f:
    QUESTIONS = json.load(f)

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        layout.add_widget(Label(text="📚 DSSSB Quiz App", font_size=32))
        start_btn = Button(text="Start Quiz", font_size=24, size_hint=(1, 0.3))
        start_btn.bind(on_press=self.start_quiz)
        layout.add_widget(start_btn)
        self.add_widget(layout)

    def start_quiz(self, instance):
        self.manager.current = "quiz"

class QuizScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.index = 0
        self.score = 0
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        self.question_label = Label(text="", font_size=24, halign="center")
        self.layout.add_widget(self.question_label)
        self.option_buttons = []
        for i in range(4):
            btn = Button(text="", font_size=20)
            btn.bind(on_press=self.check_answer)
            self.layout.add_widget(btn)
            self.option_buttons.append(btn)
        self.add_widget(self.layout)
        self.load_question()

    def load_question(self):
        if self.index < len(QUESTIONS):
            q = QUESTIONS[self.index]
            self.question_label.text = q["question"]
            for i, opt in enumerate(q["options"]):
                self.option_buttons[i].text = opt
        else:
            self.manager.get_screen("result").set_score(self.score, len(QUESTIONS))
            self.manager.current = "result"

    def check_answer(self, instance):
        correct = QUESTIONS[self.index]["answer"]
        if instance.text == QUESTIONS[self.index]["options"][correct]:
            self.score += 1
        self.index += 1
        self.load_question()

class ResultScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        self.result_label = Label(text="", font_size=26)
 
        self.layout.add_widget(self.result_label)
        restart_btn = Button(text="Restart Quiz", size_hint=(1,0.3))
        restart_btn.bind(on_press=self.restart)
        self.layout.add_widget(restart_btn)
        self.add_widget(self.layout)

    def set_score(self, score, total):
        self.result_label.text = f"✅ Score: {score}/{total}"

    def restart(self, instance):
        quiz_screen = self.manager.get_screen("quiz")
        quiz_screen.index = 0
        quiz_screen.score = 0
        quiz_screen.load_question()
        self.manager.current = "home"

class QuizApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(QuizScreen(name="quiz"))
        sm.add_widget(ResultScreen(name="result"))
        return sm

if __name__ == "__main__":
    QuizApp().run()
