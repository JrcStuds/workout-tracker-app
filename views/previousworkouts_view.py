import flet as ft
from backend import services


class WorkoutCard(ft.Card):
    def __init__(self, data, on_delete, on_tap):
        super().__init__()
        self.data = data
        self.on_delete = on_delete

        self.exercises_list = ft.Column()
        for exercise in data['exercises']:
            self.exercises_list.controls.append(ft.Text(exercise))

        self.options_menu = ft.PopupMenuButton(
            icon = ft.Icons.MORE_VERT,
            items = [
                ft.PopupMenuItem(
                    text = "Delete Workout",
                    icon = ft.Icons.DELETE,
                    on_click = self.delete_workout
                )
            ]
        )

        self.content = ft.GestureDetector(
            on_tap = lambda e: on_tap(date=self.data['date']),
            content = ft.Container(
                content = ft.Column([
                    ft.Row(
                        [
                            ft.Text(self.data['date'], weight=ft.FontWeight.BOLD),
                            self.options_menu
                        ],
                        alignment = ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    self.exercises_list
                ]),
                padding = ft.padding.only(20, 10, 10, 20)
            )
        )
    
    def delete_workout(self, e):
        try:
            services.delete_workout(date=self.data['date'])
            self.on_delete()
        except Exception as ex:
            self.content.content.controls.append(ft.Text(ex))
            self.update()


class PreviousWorkoutsView(ft.View):
    def __init__(self, nav_bar):
        super().__init__()
        self.route = '/previousworkouts'
        self.navigation_bar = nav_bar
        self.workout_cards = ft.Column()
        self.controls = [ft.SafeArea(content=self.workout_cards)]
        self.scroll = True
    
    def onload(self):
        self.get_workouts()

    def get_workouts(self, e=None):
        try:
            data = services.get_workouts_overview()
            self.workout_cards.controls.clear()
            for workout in data['workouts']:
                self.workout_cards.controls.append(WorkoutCard(
                    data = workout,
                    on_delete = self.get_workouts,
                    on_tap = self.handle_workoutcard_tap
                ))
        except Exception as ex:
            self.controls.append(ft.Text(f"There was an error: {ex}"))
        self.update()
    
    def refresh_workouts(self):
        self.get_workouts()

    def handle_workoutcard_tap(self, date):
        self.page.go(f'/workout/{date}')