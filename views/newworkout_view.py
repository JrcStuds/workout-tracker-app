import flet as ft
import requests
from datetime import datetime
from .baseworkout_view import *



class NewWorkoutView(BaseWorkoutView):
    def __init__(self, nav_bar):
        super().__init__(nav_bar=nav_bar)
        self.route = '/newworkout'
        self.add_initial_set = True


    def onload(self):
        self.add_exercise(add_initial_set=True)


    def submit_workout(self, e=None):
        # check that all of the weight, reps, and rir inputs are able to be converted into numbers
        valid = self.check_number_inputs()
        if valid is False:
            return

        result = {
            'workout': {
                'date': self.date_picker.value.strftime('%Y-%m-%d'),
                'exercises': [
                    {
                        'name': exercise.exercise_name_button.name.value,
                        'sets': [
                            {
                                'weight': set.weight_input.value,
                                'reps': set.reps_input.value,
                                'rir': set.rir_input.value
                            }
                            for set in exercise.set_rows.controls
                        ]
                    }
                    for exercise in self.exercises.controls
                ]
            }
        }
        
        requests.post(
            url = 'http://127.0.0.1:5000/addworkout',
            json = result
        )

        self.reset_view()


    def reset_view(self, e=None):
        self.exercise_count = 0
        self.exercises.controls.clear()
        self.date_picker.value = datetime.today()
        self.date_picker_on_change()
        self.update()
        self.add_exercise()