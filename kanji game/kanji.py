import random
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation
from kivy.core.text import LabelBase
from kivy.clock import Clock

# register font for Kanji – no change here
LabelBase.register(name="NotoJP", fn_regular="fonts/NotoSansJP-Black.ttf")

class VocabularyApp(App):

    def build(self):
        # track streak
        self.streak = 0

        # lots of vocab
        self.vocab = [
            {"word": "水", "meaning": "Water"}, {"word": "火", "meaning": "Fire"},
            {"word": "木", "meaning": "Tree"},  {"word": "山", "meaning": "Mountain"},
            {"word": "川", "meaning": "River"},{"word": "空", "meaning": "Sky"},
            {"word": "金", "meaning": "Gold"}, {"word": "日", "meaning": "Sun"},
            {"word": "月", "meaning": "Moon"},{"word": "雨", "meaning": "Rain"},
            {"word": "花", "meaning": "Flower"}, {"word": "人", "meaning": "Person"},
            {"word": "車", "meaning": "Car"}, {"word": "家", "meaning": "House"},
            {"word": "犬", "meaning": "Dog"}, {"word": "猫", "meaning": "Cat"},
            {"word": "鳥", "meaning": "Bird"}, {"word": "魚", "meaning": "Fish"},
            {"word": "心", "meaning": "Heart"}, {"word": "目", "meaning": "Eye"},
            {"word": "耳", "meaning": "Ear"}, {"word": "口", "meaning": "Mouth"},
            {"word": "足", "meaning": "Foot"}, {"word": "手", "meaning": "Hand"},
            {"word": "青", "meaning": "Blue"}, {"word": "赤", "meaning": "Red"},
            {"word": "白", "meaning": "White"}, {"word": "黒", "meaning": "Black"},
            {"word": "時", "meaning": "Time"},{"word": "今日", "meaning": "Today"},
            {"word": "明日", "meaning": "Tomorrow"},{"word": "昨日", "meaning": "Yesterday"},
            {"word": "学校", "meaning": "School"},{"word": "先生", "meaning": "Teacher"},
            {"word": "学生", "meaning": "Student"},{"word": "日本", "meaning": "Japan"},
            {"word": "外国", "meaning": "Foreign country"},{"word": "国", "meaning": "Country"},
            {"word": "仕事", "meaning": "Work"},{"word": "お金", "meaning": "Money"},
            {"word": "食べる", "meaning": "Eat"},{"word": "飲む", "meaning": "Drink"},
            {"word": "読む", "meaning": "Read"},{"word": "書く", "meaning": "Write"},
            {"word": "歩く", "meaning": "Walk"},{"word": "走る", "meaning": "Run"},
        ]

        # root layout
        root = BoxLayout(orientation="vertical", padding=10, spacing=10)

        # main Kanji display
        self.word_label = Label(
            font_name="NotoJP",
            font_size=40, size_hint_y=None, height=80,
            color=(1,1,1,1)
        )
        root.add_widget(self.word_label)

        # buttons container
        self.button_layout = GridLayout(cols=1, size_hint_y=None, height=300, spacing=10)
        self.choice_buttons = []
        for i in range(4):  # sloppy: using i but not in text
            b = Button(
                font_name="NotoJP",
                font_size=22, size_hint_y=None, height=60
            )
            b.bind(on_press=self.on_choice)
            self.choice_buttons.append(b)
            self.button_layout.add_widget(b)
        root.add_widget(self.button_layout)

        # streak label
        self.streak_label = Label(
            font_name="NotoJP",
            text="Streak: 0",
            font_size=30, size_hint_y=None, height=60,
            color=(1,0.5,0,1)
        )
        root.add_widget(self.streak_label)

        # feedback
        self.feedback_label = Label(
            font_name="NotoJP",
            text="", font_size=22,
            size_hint_y=None, height=50,
            color=(1,1,1,1)
        )
        root.add_widget(self.feedback_label)

        # initial question
        self.update_question()
        return root

    def update_question(self):
        # pick and display
        self.current = random.choice(self.vocab)
        self.word_label.text = self.current["word"]
        # choices gen
        idx = random.randint(0,3)
        choices = [v["meaning"] for v in self.vocab if v != self.current]
        random.shuffle(choices)
        choices = choices[:3]
        choices.insert(idx, self.current["meaning"])
        # assign texts
        for btn, txt in zip(self.choice_buttons, choices):
            btn.text = txt
        # reset feedback
        self.feedback_label.text = ""
        self.feedback_label.color = (1,1,1,1)

    def on_choice(self, btn):
        sel = btn.text
        corr = self.current["meaning"]
        if sel == corr:
            # correct path
            self.feedback_label.text = "正解！"
            self.feedback_label.color = (0,1,0,1)
            self.animate_pulse(self.feedback_label)
            self.streak += 1
            self.streak_label.text = f"Streak: {self.streak}"
            self.animate_pulse(self.streak_label)
            Clock.schedule_once(lambda dt: self.update_question(), 0.8)
        else:
            # wrong path
            self.streak = 0
            self.streak_label.text = "Streak: 0"
            pop_content = BoxLayout(orientation="vertical", padding=10, spacing=10)
            lbl = Label(text=f"Wrong! Correct was:\n[ b ]{corr}[/b]", font_name="NotoJP",
                        font_size=24, markup=True, halign="center")
            pop_content.add_widget(lbl)
            ok = Button(text="OK", size_hint_y=None, height=50)
            pop_content.add_widget(ok)
            popup = Popup(title="Oops!", content=pop_content,
                          size_hint=(0.8,0.5), auto_dismiss=False)
            ok.bind(on_release=lambda *a: (popup.dismiss(), self.update_question()))
            popup.open()

    def animate_pulse(self, wdg):
        orig = wdg.font_size
        anim = Animation(font_size=orig+10, duration=0.2) + Animation(font_size=orig, duration=0.2)
        anim.start(wdg)

if __name__ == "__main__":
    VocabularyApp().run()
