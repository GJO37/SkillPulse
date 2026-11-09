
from interfaces.controller import Controller
from interfaces.load import LoadInterface


def main():
    app = Controller()

    app.add_frame("LoadInterface", LoadInterface)

    app.show_frame("LoadInterface")
    app.mainloop()


if __name__ == "__main__":
    main()