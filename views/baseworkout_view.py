import flet as ft
from backend import services
from datetime import datetime



exercise_selection_panels = []



class AddExerciseDefinitionPanel(ft.AlertDialog):
    def __init__(self):
        super().__init__()

        self.name_field = ft.TextField()
        self.submit_button = ft.ElevatedButton(
            icon = ft.Icons.SEND,
            text = "Submit Exercise",
            on_click = self.submit_exercise_definition
        )

        self.content = ft.Container(
            content = ft.Column(
                controls = [
                    ft.Text("Exercise Name"),
                    self.name_field,
                    self.submit_button
                ]
            )
        )

        
    def submit_exercise_definition(self, e=None):
        data = {
            'name': self.name_field.value,
            'primary': None,
            'secondary': None
        }

        services.add_exercise_definition(data=data)

        for button in exercise_selection_panels:
            button.onload()

        self.open = False
        self.page.update()



class AddExerciseDefinitionListTile(ft.Container):
    def __init__(self):
        super().__init__()

        self.content = ft.ListTile(
            leading = ft.Icon(ft.Icons.ADD),
            title = ft.Text("Add Exercise"),
            on_click = lambda e: self.page.open(AddExerciseDefinitionPanel())
        )



class ExerciseListTile(ft.Container):
    def __init__(self, name, update_name):
        super().__init__()
        self.exercise_name = name

        self.content = ft.ListTile(
            title = ft.Text(self.exercise_name),
            on_click = lambda e: update_name(self.exercise_name)
        )



class ExerciseSelectionPanel(ft.AlertDialog):
    def __init__(self, update_name):
        super().__init__()
        self.expand = True
        self.update_name = update_name
        self.exercise_names = services.get_exercise_definitions()['exercises']
        
        self.exercise_list_tiles = []
        for name in self.exercise_names:
            self.exercise_list_tiles.append(ExerciseListTile(
                name = name,
                update_name = update_name
            ))
        self.exercise_list_tiles.append(AddExerciseDefinitionListTile())

        self.content = ft.Container(
            content = ft.ListView(
                controls = self.exercise_list_tiles
            )
        )

        exercise_selection_panels.append(self)

    
    def onload(self):
        self.exercise_names = services.get_exercise_definitions()['exercises']
        
        self.exercise_list_tiles = []
        for name in self.exercise_names:
            self.exercise_list_tiles.append(ExerciseListTile(
                name = name,
                update_name = self.update_name
            ))
        self.exercise_list_tiles.append(AddExerciseDefinitionListTile())

        self.content.content.controls = self.exercise_list_tiles
        self.content.update()
        self.update()



class ExerciseNameButton(ft.ElevatedButton):
    def __init__(self):
        super().__init__()

        self.name = ft.Text(value="Select Exercise", size=18)
        self.exercise_selection_panel = ExerciseSelectionPanel(update_name=self.update_name)

        self.content = ft.Container(
            content = ft.Row(
                controls = [
                    self.name,
                    ft.Icon(ft.Icons.ARROW_DROP_DOWN)
                ],
                expand = True,
                alignment = ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            padding = ft.padding.symmetric(horizontal=15)
        )

        self.expand = True
        self.height = 50
        self.on_click = lambda e: self.page.open(self.exercise_selection_panel)

    
    def update_name(self, name):
        self.name.value = name
        self.exercise_selection_panel.open = False
        self.exercise_selection_panel.update()
        self.update()



class AddExerciseButton(ft.FilledButton):
    def __init__(self, add_exercise):
        super().__init__()
        self.text = "Add Exercise"
        self.icon = ft.Icons.ADD
        self.on_click = add_exercise



class AddSetButton(ft.FilledButton):
    def __init__(self, add_set):
        super().__init__()
        self.text = "Add Set"
        self.icon = ft.Icons.ADD
        self.on_click = add_set

    

class SetRow(ft.Row):
    def __init__(self, index, remove_set):
        super().__init__()
        self.alignment = ft.MainAxisAlignment.CENTER
        
        self.index = index
        self.index_text = ft.Text(
            value = self.index + 1,
            width = 30,
            text_align = ft.TextAlign.CENTER
        )
        self.weight_input = ft.TextField(
            label = "Weight",
            expand = 1,
            input_filter = ft.InputFilter(regex_string=r"^[0-9.]*$", replacement_string="")
        )
        self.reps_input = ft.TextField(
            label = "Reps",
            expand = 1,
            input_filter = ft.InputFilter(regex_string=r"^[0-9]*$", replacement_string="")
        )
        self.rir_input = ft.TextField(
            label = "RIR",
            expand = 1,
            input_filter = ft.InputFilter(regex_string=r"^[0-9]*$", replacement_string="")
        )
        self.remove_set_button = ft.IconButton(
            icon = ft.Icons.DELETE,
            on_click = lambda e: remove_set(self.index),
            disabled = True,
        )

        self.controls = [
            self.index_text,
            self.weight_input,
            self.reps_input,
            self.rir_input,
            self.remove_set_button
        ]

    
    def onload(self):
        pass



class Exercise(ft.Column):
    def __init__(self, index, remove_exercise):
        super().__init__()
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.margin = ft.margin.symmetric(vertical=10)

        self.set_row_obj = SetRow
        
        self.index = index
        self.set_count = 0
        self.exercise_name_button = ExerciseNameButton()
        self.remove_exercise_button = ft.IconButton(
            icon = ft.Icons.DELETE,
            on_click = lambda e: remove_exercise(index=self.index),
            disabled = True
        )
        self.add_set_button = AddSetButton(add_set=self.add_set)
        self.header = ft.Row(
            controls = [
                self.exercise_name_button,
                self.remove_exercise_button
            ],
            alignment = ft.MainAxisAlignment.CENTER
        )

        self.set_rows = ft.Column()

        self.controls = [
            self.header,
            self.set_rows,
            self.add_set_button
        ]

    
    def onload():
        pass
    
    
    def add_set(self, e=None):
        new_set_row = self.set_row_obj(index=self.set_count, remove_set=self.remove_set)
        self.set_rows.controls.append(new_set_row)
        self.set_count += 1
        self.set_rows.update()
        for row in self.set_rows.controls:
            row.remove_set_button.disabled = (self.set_count == 1)
        self.update()


    def remove_set(self, index):
        self.set_rows.controls.pop(index)
        self.set_count -= 1
        for i, row in enumerate(self.set_rows.controls):
            row.index = i
            row.index_text.value = i + 1
            row.remove_set_button.disabled = (self.set_count == 1)
        self.update()



class BaseWorkoutView(ft.View):
    def __init__(self, nav_bar):
        super().__init__()
        self.route = '/baseworkout'
        self.navigation_bar = nav_bar
        self.scroll = True

        self.exercise_obj = Exercise
        self.add_initial_set = False

        self.exercise_count = 0
        self.exercises = ft.Column()
        self.add_exercise_button = AddExerciseButton(add_exercise=self.add_exercise)
        self.submit_workout_button = ft.FilledButton(
            icon = ft.Icons.SEND,
            text = "Submit Workout",
            on_click = self.submit_workout
        )

        self.date_picker = ft.DatePicker(
            value = datetime.today(),
            on_change = self.date_picker_on_change
        )
        self.date_picker_button = ft.OutlinedButton(
            text = self.date_picker.value.strftime('%Y-%m-%d'),
            on_click = lambda e: self.page.open(self.date_picker)
        )

        self.content = ft.Column(
            controls = [
                self.date_picker_button,
                self.exercises,
                self.add_exercise_button,
                self.submit_workout_button
            ],
            horizontal_alignment = ft.CrossAxisAlignment.CENTER
        )

        self.controls = [ft.SafeArea(content=self.content)]
    

    def onload(self):
        pass

    
    def add_exercise(self, e=None, add_initial_set=False):
        self.new_exercise = self.exercise_obj(
            index = self.exercise_count,
            remove_exercise = self.remove_exerise
        )

        self.exercises.controls.append(self.new_exercise)
        self.exercise_count += 1
        self.exercises.update()

        if self.add_initial_set:
            self.new_exercise.add_set()

        for i, exercise in enumerate(self.exercises.controls):
            exercise.index = i
            exercise.remove_exercise_button.disabled = (self.exercise_count == 1)
            exercise.update()

        self.update()
    
    
    def remove_exerise(self, index):
        self.exercises.controls.pop(index)
        self.exercise_count -= 1

        for i, exercise in enumerate(self.exercises.controls):
            exercise.index = i
            exercise.update()

            if self.exercise_count == 1:
                exercise.remove_exercise_button.disabled = True
            else:
                exercise.remove_exercise_button.disabled = False
            
            exercise.update()

        self.update()


    def submit_workout(self, e=None):
        pass

    
    def check_number_inputs(self):
        valid = True
        for exercise in self.exercises.controls:
            for set in exercise.set_rows.controls:
                inputs = [
                    set.weight_input,
                    set.reps_input,
                    set.rir_input
                ]

                for input in inputs:
                    try:
                        test = float(input.value)
                    except:
                        valid = False
                        input.error_text = "Field must be a number"

                    if input.value == "":
                        valid = False
                        input.error_text = "This field is required"
                
        self.update()
        return valid
    

    def date_picker_on_change(self, e=None):
        self.date_picker_button.text = self.date_picker.value.strftime('%Y-%m-%d')
        self.update()