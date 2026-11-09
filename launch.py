
from interfaces.controller import Controller
from interfaces.home import HomeInterface
from interfaces.profile import ProfileInterface


def main():
    app = Controller()

    app.add_frame("HomeInterface", HomeInterface)
    app.add_frame("ProfileInterface", ProfileInterface)

    app.show_frame("HomeInterface")
    app.mainloop()


if __name__ == "__main__":
    main()