import phonenumbers
from phonenumbers import timezone, geocoder, carrier
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import ImageTk, Image
import qrcode
import sqlite3
from ttkthemes import ThemedStyle

def generate_qr_code():
    phone_info = result_label.cget("text")
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(phone_info)
    qr.make(fit=True)
    qr_image = qr.make_image(fill_color="black", back_color="white")
    qr_image.save("qrcode.png")

    # Show the QR code image in a new window.
    qr_window = tk.Toplevel(window)
    qr_window.title("QR Code")
    qr_image_label = tk.Label(qr_window, image=ImageTk.PhotoImage(qr_image))
    qr_image_label.pack()

def get_phone_info():
    number = entry.get()

    try:
        phone = phonenumbers.parse(number, None)
        if not phonenumbers.is_valid_number(phone):
            raise phonenumbers.NumberParseException(phonenumbers.NumberParseException.NOT_A_NUMBER, "Invalid phone number format.")

        time_zones = timezone.time_zones_for_number(phone)
        carrier_name = carrier.name_for_number(phone, "en")
        region = geocoder.description_for_number(phone, "en")

        result_text = f"Phone Number: {phonenumbers.format_number(phone, phonenumbers.PhoneNumberFormat.INTERNATIONAL)}\n"
        result_text += f"Time Zones: {', '.join(time_zones)}\n"
        result_text += f"Carrier: {carrier_name}\n"
        result_text += f"Region: {region}"

        result_label.config(text=result_text)
        copy_button.config(state=tk.NORMAL)
        qr_code_button.config(state=tk.NORMAL)

        # Save to history
        save_to_history(number, result_text)

    except phonenumbers.NumberParseException as e:
        messagebox.showerror("Error", str(e))
        result_label.config(text="")
        copy_button.config(state=tk.DISABLED)
        qr_code_button.config(state=tk.DISABLED)

def copy_to_clipboard():
    phone_info = result_label.cget("text")
    window.clipboard_clear()
    window.clipboard_append(phone_info)
    messagebox.showinfo("Information", "Phone number information copied to clipboard.")

def clear_fields():
    entry.delete(0, tk.END)
    result_label.config(text="")
    copy_button.config(state=tk.DISABLED)
    qr_code_button.config(state=tk.DISABLED)

def on_enter_key(event):
    get_phone_info()

def save_to_history(number, result_text):
    conn = sqlite3.connect("phone_history.db")
    c = conn.cursor()
    c.execute("INSERT INTO phone_history (phone_number, info) VALUES (?, ?)", (number, result_text))
    conn.commit()
    conn.close()

def load_history():
    conn = sqlite3.connect("phone_history.db")
    c = conn.cursor()
    c.execute("SELECT phone_number, info FROM phone_history ORDER BY id DESC")
    history = c.fetchall()
    conn.close()
    return history

def show_history():
    history_window = tk.Toplevel(window)
    history_window.title("Query History")
    history_window.geometry("600x400")

    history_text = tk.Text(history_window, wrap=tk.WORD)
    history_text.pack(fill=tk.BOTH, expand=True)

    history = load_history()
    for entry in history:
        history_text.insert(tk.END, f"{entry[0]}\n{entry[1]}\n\n")

def export_database():
    with open("phone_history_backup.sql", "w") as file:
        conn = sqlite3.connect("phone_history.db")
        for line in conn.iterdump():
            file.write(f"{line}\n")
        conn.close()
    messagebox.showinfo("Information", "Database exported to 'phone_history_backup.sql'.")

# Create the main window
window = tk.Tk()
window.title("Phone Number Info")
window.geometry("500x500")
window.resizable(False, False)

entry_label = tk.Label(window, text="Enter your phone number:")
entry_label.pack(pady=5)

entry = tk.Entry(window)
entry.pack(padx=10, pady=5)
entry.bind("<Return>", on_enter_key)

get_info_button = tk.Button(window, text="Get Info", command=get_phone_info)
get_info_button.pack(pady=5)

result_label = ttk.Label(window, text="", wraplength=400, justify=tk.LEFT)
result_label.pack(pady=10)

copy_button = tk.Button(window, text="Copy to Clipboard", command=copy_to_clipboard, state=tk.DISABLED)
copy_button.pack(pady=5)

qr_code_button = tk.Button(window, text="Generate QR Code", command=generate_qr_code, state=tk.DISABLED)
qr_code_button.pack(pady=5)

clear_button = tk.Button(window, text="Clear Fields", command=clear_fields)
clear_button.pack(pady=5)

history_button = tk.Button(window, text="View History", command=show_history)
history_button.pack(pady=5)

export_button = tk.Button(window, text="Export Database", command=export_database)
export_button.pack(pady=5)

style = ThemedStyle(window)
style.set_theme("equilux")  # Choose a dark theme. You can use "breeze" for light mode.

# Create a SQLite database to store the history.
conn = sqlite3.connect("phone_history.db")
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS phone_history (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             phone_number TEXT NOT NULL,
             info TEXT NOT NULL)''')

conn.commit()
conn.close()

window.mainloop()
