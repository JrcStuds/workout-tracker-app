import kivy

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout


class SetInputRow(BoxLayout):
    def on_parent(self, instance, parent):
        if parent:
            parent.bind(height=self.update_height)
            self.update_height(parent, parent.height)
    
    def update_height(self, instance, value):
        self.height = value * 0.1


class ExerciseSets(BoxLayout):
    def add_row(self):
        self.add_widget(SetInputRow(), index=1)


class WorkoutTrackerApp(App):
    def build(self):
        Builder.load_file('app.kv')
        return ExerciseSets()


if __name__ == '__main__':
    WorkoutTrackerApp().run()