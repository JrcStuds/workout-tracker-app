import flet as ft
import threading
from flask_backend import create_app
from views.previousworkouts_view import PreviousWorkoutsView
from views.newworkout_view import NewWorkoutView
from views.singleworkout_view import SingleWorkoutView
import backend


def run_flask():
    app = create_app()
    app.run(port=5000, threaded=True)

threading.Thread(target=run_flask, daemon=True).start()


def main(page: ft.Page):
    page.title = "Workout Tracker App"


    def route_change(route):
        page.views.clear()

        if route.route.startswith('/workout/'):
            date = route.route.split('/workout/')[1]
            if (
                views['singleworkout'] and
                views['singleworkout'].route == route.route and
                views['previousworkout'].route == route.route
            ):
                view = views['previousworkout']
                page.views.append(view)
                page.update()
            else:
                views['singleworkout'] = SingleWorkoutView(nav_bar=nav_bar, date=date)
                views['previousworkout'] = views['singleworkout']
                view = views['previousworkout']
                page.views.append(view)
                page.update()
                view.onload()

        elif route.route == '/newworkout':
            view = views['newworkout']
            page.views.append(view)
            page.update()

        elif route.route == '/previousworkouts':
            views['previousworkout'] = PreviousWorkoutsView(nav_bar=nav_bar)
            view = views['previousworkout']
            page.views.append(view)
            page.update()
            view.onload()


    def navigation_bar_change(e):
        screens = ['previousworkout', 'newworkout']
        page.go(views[screens[e.control.selected_index]].route)


    nav_bar = ft.NavigationBar(
        on_change=navigation_bar_change,
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.HISTORY, label="Previous Workouts"),
            ft.NavigationBarDestination(icon=ft.Icons.ADD, label="New Workout")
        ]
    )

    views = {
        'previousworkout': PreviousWorkoutsView(nav_bar=nav_bar),
        'newworkout': NewWorkoutView(nav_bar=nav_bar),
        'singleworkout': None
    }

    page.views.append(views['newworkout'])
    page.update()
    views['newworkout'].onload()

    page.on_route_change = route_change
    page.views.clear()

    page.go('/previousworkouts')


if __name__ == '__main__':
    ft.app(target=main)