
from interfaces.controller import Controller
from interfaces.home import HomeInterface


def main():
    app = Controller()

    app.add_frame("HomeInterface", HomeInterface)

    app.show_frame("HomeInterface")
    app.mainloop()


if __name__ == "__main__":
    main()