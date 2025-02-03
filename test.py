import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
import json
import time
import math

# Main Application Class
class SmartCalculator(Gtk.Window):
    def __init__(self):
        super().__init__(title="Smart Calculator")
        self.set_default_size(450, 600)

        # Initialize components
        self.history_manager = HistoryManager()
        self.customer_manager = CustomerManager()
        self.transaction_manager = TransactionManager()

        # Load history and customers
        self.history_manager.load_history()
        self.customer_manager.load_customers()
        self.transaction_manager.load_transactions()

        # Display
        self.display = Gtk.Entry()
        self.display.set_text("0")
        self.display.set_editable(False)
        self.display.set_can_focus(False)

        # Grid Layout
        grid = Gtk.Grid()
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

        # Advanced Operations Dropdown
        advanced_menu = Gtk.Menu()
        for op in ["sqrt", "exp", "sin", "cos", "tan", "log"]:
            item = Gtk.MenuItem(label=op)
            item.connect("activate", self.on_advanced_operation, op)
            advanced_menu.append(item)
        advanced_menu.show_all()

        advanced_button = Gtk.Button(label="Advanced")
        advanced_button.connect("button-press-event", lambda _, __: advanced_menu.popup_at_pointer())
        grid.attach(advanced_button, 2, 5, 2, 1)

        # Hamburger Menu
        menu_button = Gtk.MenuButton()
        icon = Gtk.Image.new_from_icon_name("open-menu-symbolic", Gtk.IconSize.BUTTON)
        menu_button.set_image(icon)
        menu_button.set_popup(self.create_hamburger_menu())
        grid.attach(menu_button, 3, 0, 1, 1)

        # Add Grid to Window
        self.add(grid)

        # Keyboard Input
        self.connect("key-press-event", self.on_key_press)

    # Calculator Logic
    def on_button_click(self, widget, value):
        current = self.display.get_text()
        if value == '=':
            try:
                result = eval(current)
                self.display.set_text(str(result))
                self.history_manager.add_calculation(current, result)
            except Exception:
                self.display.set_text("Error")
        elif value == 'C':
            self.display.set_text("0")
        else:
            if current == "0" and value != '.':
                self.display.set_text(value)
            else:
                self.display.set_text(current + value)

    def on_advanced_operation(self, widget, operation):
        current = self.display.get_text()
        try:
            if operation == "sqrt":
                result = math.sqrt(float(current))
            elif operation == "exp":
                result = math.exp(float(current))
            elif operation in ["sin", "cos", "tan", "log"]:
                func = getattr(math, operation)
                result = func(float(current))
            self.display.set_text(str(result))
        except Exception:
            self.display.set_text("Error")

    def clear_display(self, widget):
        self.display.set_text("0")

    def on_key_press(self, widget, event):
        key_name = Gdk.keyval_name(event.keyval)
        if key_name.isdigit() or key_name in ['plus', 'minus', 'asterisk', 'slash', 'equal', 'period']:
            self.on_button_click(None, key_name.replace('plus', '+').replace('minus', '-').replace('asterisk', '*').replace('slash', '/').replace('equal', '='))
        elif key_name == 'Escape':
            self.clear_display(None)

    # Hamburger Menu
    def create_hamburger_menu(self):
        menu = Gtk.Menu()

        # Recent Calculations
        recent_item = Gtk.MenuItem(label="Recent Calculations")
        recent_item.connect("activate", self.show_recent_calculations)
        menu.append(recent_item)

        # Customer Management
        customer_item = Gtk.MenuItem(label="Customer List")
        submenu = Gtk.Menu()

        view_item = Gtk.MenuItem(label="View Customers")
        view_item.connect("activate", self.view_customers)
        submenu.append(view_item)

        add_item = Gtk.MenuItem(label="Add Customer")
        add_item.connect("activate", self.add_customer)
        submenu.append(add_item)

        delete_item = Gtk.MenuItem(label="Delete Customer")
        delete_item.connect("activate", self.delete_customer)
        submenu.append(delete_item)

        modify_item = Gtk.MenuItem(label="Modify Customer")
        modify_item.connect("activate", self.modify_customer)
        submenu.append(modify_item)

        customer_item.set_submenu(submenu)
        menu.append(customer_item)

        # About
        about_item = Gtk.MenuItem(label="About")
        about_item.connect("activate", self.show_about)
        menu.append(about_item)

        menu.show_all()
        return menu

    def show_recent_calculations(self, widget):
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.CLOSE,
            text="Recent Calculations",
        )
        dialog.format_secondary_text("\n".join(self.history_manager.get_history()))
        dialog.run()
        dialog.destroy()

    def view_customers(self, widget):
        customers = self.customer_manager.get_customers()
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.CLOSE,
            text="Customer List",
        )
        dialog.format_secondary_text("\n".join([f"{c['name']} - {c['phone']}" for c in customers]))
        dialog.run()
        dialog.destroy()

    def add_customer(self, widget):
        dialog = Gtk.Dialog(title="Add Customer", transient_for=self, flags=0)
        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK)

        name_entry = Gtk.Entry(placeholder_text="Name")
        phone_entry = Gtk.Entry(placeholder_text="Phone")
        email_entry = Gtk.Entry(placeholder_text="Email")
        address_entry = Gtk.Entry(placeholder_text="Address")

        box = dialog.get_content_area()
        box.add(Gtk.Label(label="Name:"))
        box.add(name_entry)
        box.add(Gtk.Label(label="Phone:"))
        box.add(phone_entry)
        box.add(Gtk.Label(label="Email:"))
        box.add(email_entry)
        box.add(Gtk.Label(label="Address:"))
        box.add(address_entry)
        box.show_all()

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            name = name_entry.get_text()
            phone = phone_entry.get_text()
            email = email_entry.get_text()
            address = address_entry.get_text()
            self.customer_manager.add_customer(name, phone, email, address)
        dialog.destroy()

    def delete_customer(self, widget):
        customers = self.customer_manager.get_customers()
        if not customers:
            return

        dialog = Gtk.Dialog(title="Delete Customer", transient_for=self, flags=0)
        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK)

        names = [c["name"] for c in customers]
        combo = Gtk.ComboBoxText()
        for name in names:
            combo.append_text(name)
        combo.set_active(0)

        box = dialog.get_content_area()
        box.add(Gtk.Label(label="Select Customer:"))
        box.add(combo)
        box.show_all()

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            selected_name = combo.get_active_text()
            self.customer_manager.delete_customer(selected_name)
        dialog.destroy()

    def modify_customer(self, widget):
        customers = self.customer_manager.get_customers()
        if not customers:
            return

        dialog = Gtk.Dialog(title="Modify Customer", transient_for=self, flags=0)
        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK)

        names = [c["name"] for c in customers]
        combo = Gtk.ComboBoxText()
        for name in names:
            combo.append_text(name)
        combo.set_active(0)

        name_entry = Gtk.Entry()
        phone_entry = Gtk.Entry()
        email_entry = Gtk.Entry()
        address_entry = Gtk.Entry()

        box = dialog.get_content_area()
        box.add(Gtk.Label(label="Select Customer:"))
        box.add(combo)
        box.add(Gtk.Label(label="New Name:"))
        box.add(name_entry)
        box.add(Gtk.Label(label="New Phone:"))
        box.add(phone_entry)
        box.add(Gtk.Label(label="New Email:"))
        box.add(email_entry)
        box.add(Gtk.Label(label="New Address:"))
        box.add(address_entry)
        box.show_all()

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            selected_name = combo.get_active_text()
            new_name = name_entry.get_text() or selected_name
            new_phone = phone_entry.get_text()
            new_email = email_entry.get_text()
            new_address = address_entry.get_text()
            self.customer_manager.modify_customer(selected_name, new_name, new_phone, new_email, new_address)
        dialog.destroy()

    def show_about(self, widget):
        dialog = Gtk.AboutDialog(
            program_name="Smart Calculator",
            version="1.0",
            comments="A modern calculator with transaction management.",
            authors=["Your Name"],
            license_type=Gtk.License.GPL_3_0,
        )
        dialog.run()
        dialog.destroy()

# History Manager
class HistoryManager:
    def __init__(self, filename="history.json"):
        self.filename = filename
        self.load_history()

    def load_history(self):
        try:
            with open(self.filename, "r") as f:
                self.history = json.load(f)
        except FileNotFoundError:
            self.history = []

    def save_history(self):
        with open(self.filename, "w") as f:
            json.dump(self.history, f)

    def add_calculation(self, expression, result):
        self.history.append(f"{expression} = {result}")
        self.save_history()

    def get_history(self):
        return self.history

    def clear_history(self):
        self.history = []
        self.save_history()

# Customer Manager
class CustomerManager:
    def __init__(self, filename="customers.json"):
        self.filename = filename
        self.load_customers()

    def load_customers(self):
        try:
            with open(self.filename, "r") as f:
                self.customers = json.load(f)
        except FileNotFoundError:
            self.customers = []

    def save_customers(self):
        with open(self.filename, "w") as f:
            json.dump(self.customers, f)

    def add_customer(self, name, phone, email, address):
        self.customers.append({"name": name, "phone": phone, "email": email, "address": address})
        self.save_customers()

    def delete_customer(self, name):
        self.customers = [c for c in self.customers if c["name"] != name]
        self.save_customers()

    def modify_customer(self, old_name, new_name, phone, email, address):
        for c in self.customers:
            if c["name"] == old_name:
                c["name"] = new_name
                c["phone"] = phone
                c["email"] = email
                c["address"] = address
                break
        self.save_customers()

    def get_customers(self):
        return self.customers

# Transaction Manager
class TransactionManager:
    def __init__(self, filename="transactions.json"):
        self.filename = filename
        self.load_transactions()

    def load_transactions(self):
        try:
            with open(self.filename, "r") as f:
                self.transactions = json.load(f)
        except FileNotFoundError:
            self.transactions = {}

    def save_transactions(self):
        with open(self.filename, "w") as f:
            json.dump(self.transactions, f)

    def add_transaction(self, customer_name, amount, type_):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        if customer_name not in self.transactions:
            self.transactions[customer_name] = []
        self.transactions[customer_name].append({"type": type_, "amount": amount, "timestamp": timestamp})
        self.save_transactions()

    def get_transactions(self, customer_name):
        return self.transactions.get(customer_name, [])

if __name__ == "__main__":
    app = SmartCalculator()
    app.connect("destroy", Gtk.main_quit)
    app.show_all()
    Gtk.main()
