import flet as ft
import requests
from .baseworkout_view import *



class SingleWorkoutSetRow(SetRow):
    def __init__(self, index, remove_set):
        super().__init__(index=index, remove_set=remove_set)
    
    
    def onload(self, data):
        self.data = data

        self.index_text.value = self.data['set_number'] + 1
        self.weight_input.value = self.data['weight']
        self.reps_input.value = self.data['reps']
        self.rir_input.value = self.data['rir']


    def update_edit_mode(self, state):
        self.weight_input.read_only = not state
        self.reps_input.read_only = not state
        self.rir_input.read_only = not state
        self.remove_set_button.visible = state



class SingleWorkoutExercise(Exercise):
    def __init__(self, index, remove_exercise):
        super().__init__(index=index, remove_exercise=remove_exercise)

        self.set_row_obj = SingleWorkoutSetRow
        

    def onload(self, data):
        self.data = data

        self.exercise_name_button.name.value = data['name']
        self.exercise_name_button.name.update()

        for set_data in self.data['sets']:
            self.add_set()
            self.set_rows.controls[-1].onload(data=set_data)
    

    def update_edit_mode(self, state):
        for set in self.set_rows.controls:
            set.update_edit_mode(state=state)

        self.add_set_button.visible = state
        self.remove_exercise_button.visible = state

        if state is True: # adds click function and resets click animation
            self.exercise_name_button.on_click = lambda e: self.page.open(self.exercise_name_button.exercise_selection_panel)
            self.exercise_name_button.style = ft.ButtonStyle(
                overlay_color = None
            )
        else: # removes click function and makes animation invisible
            self.exercise_name_button.on_click = lambda e: None
            self.exercise_name_button.style = ft.ButtonStyle(
                overlay_color = ft.Colors.TRANSPARENT
            )



class SingleWorkoutView(BaseWorkoutView):
    def __init__(self, nav_bar, date):
        super().__init__(nav_bar=nav_bar)
        self.date = date
        self.route = f'/workout/{self.date}'
        self.edit_mode = True

        self.exercise_obj = SingleWorkoutExercise
        self.add_initial_set = False

        self.back_button = ft.IconButton(
            icon = ft.Icons.ARROW_BACK,
            on_click = lambda e: self.page.go('/previousworkouts')
        )
        self.edit_button = ft.IconButton(
            icon = ft.Icons.EDIT,
            on_click = lambda e: self.update_edit_mode()
        )

        self.appbar = ft.AppBar(
            self.back_button,
            actions = [self.edit_button]
        )

        self.submit_workout_button.icon = ft.Icons.SAVE
        self.submit_workout_button.text = "Save Workout"

        self.date_picker.value = datetime.strptime(self.date, '%Y-%m-%d')
        self.date_picker_button.text = self.date_picker.value.strftime('%Y-%m-%d')

        self.navigation_bar = nav_bar
        self.data = None
    

    def onload(self):
        self.appbar.title = ft.Text(f"Workout {self.date}")
        self.exercises.controls.clear()
        self.exercise_count = 0
        self.add_initial_set = False

        self.data = requests.get(f'http://127.0.0.1:5000/getworkout/{self.date}').json()
        
        for exercise_data in self.data['workout']['exercises']:
            self.add_exercise()
            self.exercises.controls[-1].onload(data=exercise_data)
        
        self.update()
        self.add_initial_set = True

        self.update_edit_mode()


    def submit_workout(self, e=None):
        # check that all of the weight, reps, and rir inputs are able to be converted into numbers
        valid = self.check_number_inputs()
        if valid is False:
            return

        result = {
            'workout': {
                'old_date': self.date,
                'new_date': self.date_picker.value.strftime('%Y-%m-%d'),
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
            url = 'http://127.0.0.1:5000/editworkout',
            json = result
        )

        self.date = self.date_picker.value.strftime('%Y-%m-%d')
        self.onload()


    def update_edit_mode(self, e=None):
        self.edit_mode = not self.edit_mode

        for exercise in self.exercises.controls:
            exercise.update_edit_mode(state=self.edit_mode)

        self.edit_button.disabled = self.edit_mode
        self.date_picker_button.visible = self.edit_mode
        self.add_exercise_button.visible = self.edit_mode
        self.submit_workout_button.visible = self.edit_mode
        
        self.update()