
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class CalculatorApp(Gtk.Window):
    def __init__(self):
        super().__init__(title="Smart Calculator")
        self.set_default_size(400, 500)

        # Create layout
        grid = Gtk.Grid()
        self.add(grid)

        # Display
        self.display = Gtk.Entry()
        self.display.set_text("0")
        grid.attach(self.display, 0, 0, 4, 1)

        # Buttons
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('+', 4, 2), ('=', 4, 3),
        ]

        for (text, row, col) in buttons:
            button = Gtk.Button(label=text)
            button.connect("clicked", self.on_button_click, text)
            grid.attach(button, col, row, 1, 1)

        # Clear Button
        clear_button = Gtk.Button(label="C")
        clear_button.connect("clicked", self.clear_display)
        grid.attach(clear_button, 0, 5, 2, 1)

        # Add Transaction Button
        add_transaction_button = Gtk.Button(label="Add Transaction")
        add_transaction_button.connect("clicked", self.add_transaction)
        grid.attach(add_transaction_button, 2, 5, 2, 1)

    def on_button_click(self, widget, value):
        current = self.display.get_text()
        if value == '=':
            try:
                result = eval(current)
                self.display.set_text(str(result))
            except Exception:
                self.display.set_text("Error")
        elif value == 'C':
            self.display.set_text("0")
        else:
            if current == "0" and value != '.':
                self.display.set_text(value)
            else:
                self.display.set_text(current + value)

    def clear_display(self, widget):
        self.display.set_text("0")

    def add_transaction(self, widget):
        amount = self.display.get_text()
        print(f"Transaction Added: {amount}")

if __name__ == "__main__":
    win = CalculatorApp()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
