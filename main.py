import tkinter as tk
from tkinter import messagebox, filedialog, ttk;
from PIL import Image, ImageTk

import mysql.connector

# import created library
from command import Command as cmd

# creating root window
root = tk.Tk()

# window dimension
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
custom_size = str(width) + 'x' + str(height)
root.geometry(custom_size)

root.resizable(False, False)
root.title('MediCare')

# frame dimension
frame_width = width * .5
image_tk = None

# container frame
create_frame = tk.Frame(root, width=width, height=height)
login_container = tk.Frame(root, width=width, height=height)


# the main container frame and image frame
def img_frame(master, frame_width, img_url):
  # frame that holds the image
  img_frame = tk.Frame(master, width=frame_width, height=height)
  img_frame.place(x=0, y=0)

  global image_tk
  image = Image.open(img_url)
  image_resized = image.resize((int(frame_width), height), Image.ANTIALIAS)
  image_tk = ImageTk.PhotoImage(image_resized)

  label_img = tk.Label(img_frame, image=image_tk)

  label_img.pack(expand=True, anchor='center')



# user login frame
def login_user_account():
  widget_font = 'Tahoma'
  widget_width = 40
  img_url = 'asset/account_bg.jpg'

  # frame that contains the other frames
  create_frame.forget()
  login_container.pack()

  # frame that holds the image
  img_frame(login_container, frame_width, img_url)

  login_frameholder = tk.Frame(login_container, width=frame_width, height=height, bg='#fff')
  login_frameholder.place(x=frame_width, y=0)
  login_frameholder.pack_propagate(flag=False)

  container = tk.Frame(login_frameholder, bg=login_frameholder['bg'])
  container.pack(expand=True, anchor='center')

  label_mail = tk.Label(container, text='Email', bg=login_frameholder['bg'], font=widget_font)
  entry_mail = tk.Entry(container, width=widget_width, highlightthickness=0, font=widget_font)

  label_mail.grid(row=0, column=0)
  entry_mail.grid(row=1, column=0)

  label_password = tk.Label(container, text='Password', bg=login_frameholder['bg'], font=widget_font)
  entry_password = tk.Entry(container, width=widget_width, highlightthickness=0, font=widget_font)

  label_password.grid(row=2, column=0)
  entry_password.grid(row=3, column=0)

  submit_btn = tk.Button(container, text='Login', width=39, padx=10, pady=10, bg='blue', fg='#fff', activebackground='blue', activeforeground='#fff', border=0, highlightthickness=0, font=widget_font)
  submit_btn.grid(row=4, column=0)

  create_account_btn = tk.Button(container, text='If you have no existing account. Create account', bg=login_frameholder['bg'], activebackground=login_frameholder['bg'], border=0, highlightthickness=0, font=widget_font, command=lambda: cmd.show_frame(login_container, create_user_account))
  create_account_btn.grid(row=5, column=0)


  for widget in container.winfo_children():
    widget.grid_configure(padx=15, pady=15)



# validate user input
def validate_create_account(value_arr):
  values = value_arr
  for value in values:
    if value[0] == 'sex' and not(value[1] == 'Male' or value[1] == 'Female') :
      messagebox.showerror('Fill the sex entry', 'Choose an option of Male or Female from the dropdown')
      return ''

    if value[0] == 'marital' and not(value[1] == 'Single' or value[1] == 'Married' or value[1] == 'Divorce'):
      messagebox.showerror('Fill the marital entry', 'Choose an option of Single, Married or Divorced from the dropdown')
      return ''

    if value[0] == 'bloodgroup' and not(value[1] == 'O+' or value[1] == 'O-' or value[1] == 'AB' or value[1] == 'AB+'):
      messagebox.showerror('Fill the blood group entry', 'Choose an option of O+, O-, AB+ or AB- from the dropdown')
      return ''
    
    if value[0] == 'genotype' and not(value[1] == 'AA' or value[1] == 'AS' or value[1] == 'SS'):
      messagebox.showerror('Fill the genotype entry', 'Choose an option of AA, AS, or SS from the dropdown')
      return ''
    
    if value[0] == 'password' and value[1] == '':
      messagebox.showerror('Fill the password entry', 'Please provide a password')
      return ''
    
    if value[0] == 'confirm_password' and value[1] == '':
      messagebox.showerror('Fill the confirm password entry', 'Please confirm your password')
      return ''
    
    if value[1] == '':
      messagebox.showerror('Empty Form', f'All inputs field must be filled: {value[0]}')
      return ''
    
  connect = mysql.connector.connect(host='localhost', password='', user='root', database='hospital_patient_data')
  cursor = connect.cursor()

  try:
    if not(connect.is_connected()): return

    create_table = 'CREATE TABLE IF NOT EXISTS user(id_key INT PRIMARY KEY AUTO_INCREMENT, first_name TEXT, last_name TEXT, sex TEXT, address TEXT, state TEXT, marital_status TEXT, blood_group TEXT, genotype TEXT, password TEXT, mail TEXT)'
    cursor.execute(create_table)

    login_user_account()

  except mysql.ConnectionError as e:
    messagebox.showerror('connection error', f'There is an error connectng to the database {e}')
    
  finally:
    cursor.close()
    connect.commit()



# create user account frame
def create_user_account():
  img_url = 'asset/account_bg.jpg'
  widget_width = 29
  combo_width = 28

  # frame that contains the other frames
  create_frame.pack()

  # frame the holds the image
  img_frame(create_frame, frame_width, img_url)
  
  # frame that contain user input widget
  user_frame = tk.Frame(create_frame, width=frame_width, height=height, bg='#fff')
  user_frame.pack_propagate(flag=False) # prevents frame from taking the size of widget
  user_frame.place(x=frame_width, y=0)

  container = tk.Frame(user_frame, width=frame_width, bg=user_frame['bg'])
  container.pack(expand=True, anchor='center')

  label_firstname = tk.Label(container, text="First Name", bg=user_frame['bg'], width=widget_width, font='Tahoma', padx=10)
  entry_firstname = tk.Entry(container, width=widget_width, font='Tahoma')

  label_firstname.grid(row=1, column=0)
  entry_firstname.grid(row=2, column=0)

  label_lastname = tk.Label(container, text="Last Name", bg=user_frame['bg'], width=widget_width, font='Tahoma')
  entry_lastname = tk.Entry(container, width=widget_width, font='Tahoma')

  label_lastname.grid(row=1, column=1)
  entry_lastname.grid(row=2, column=1)

  label_sex = tk.Label(container, text='Sex', bg=user_frame['bg'], width=widget_width, font='Tahoma')
  entry_sex = ttk.Combobox(container, values=['Male', 'Female'], width=combo_width, font='Tahoma')

  label_sex.grid(row=3, column=0)
  entry_sex.grid(row=4, column=0)

  label_address = tk.Label(container, text='Address', bg=user_frame['bg'], width=widget_width, font='Tahoma')
  entry_adress = tk.Entry(container, width=widget_width, font='Tahoma')

  label_address.grid(row=3, column=1)
  entry_adress.grid(row=4, column=1)

  label_state = tk.Label(container, text='State of Origin', bg=user_frame['bg'], width=widget_width, font='Tahoma')
  entry_state = tk.Entry(container, width=widget_width, font='Tahoma')

  label_state.grid(row=5, column=0)
  entry_state.grid(row=6, column=0)

  label_marital = tk.Label(container, text='Marital Status', bg=user_frame['bg'], width=widget_width, font='Tahoma')
  entry_marital = ttk.Combobox(container, value=['Single', 'Married', 'Divorced'], width=widget_width, font='Tahoma')

  label_marital.grid(row=5, column=1)
  entry_marital.grid(row=6, column=1)

  label_group = tk.Label(container, text='Blood Group', bg=user_frame['bg'], width=widget_width, font='Tahoma')
  entry_group = ttk.Combobox(container, value=['O+', 'O-', 'AB', 'AB+'], width=combo_width, font='Tahoma')

  label_group.grid(row=7, column=0)
  entry_group.grid(row=8, column=0)

  label_genotype = tk.Label(container, text='Genotype', bg=user_frame['bg'], width=widget_width, font='Tahoma')
  entry_genotype = ttk.Combobox(container, value=['AA', 'AS', 'SS'], width=combo_width, font='Tahoma')

  label_genotype.grid(row=7, column=1)
  entry_genotype.grid(row=8, column=1)

  label_password = tk.Label(container, text='Password', bg=user_frame['bg'], width=widget_width, font='Tahoma')
  entry_password = tk.Entry(container, width=widget_width, font='Tahoma')

  label_password.grid(row=9, column=0)
  entry_password.grid(row=10, column=0)

  label_confirm = tk.Label(container, text='Confirm Password', bg=user_frame['bg'], width=widget_width, font='Tahoma')
  entry_confirm = tk.Entry(container, width=widget_width, font='Tahoma')

  label_confirm.grid(row=9, column=1)
  entry_confirm.grid(row=10, column=1)

  label_mail = tk.Label(container, text='Email', bg=user_frame['bg'], width=widget_width, font='Tahoma')
  entry_mail = tk.Entry(container, width=widget_width, font='Tahoma')

  label_mail.grid(row=11, column=0)
  entry_mail.grid(row=12, column=0)

  def upload_picture(event=None):
    global profile_img
    filename = filedialog.askopenfilename()
    profile_img = ImageTk.PhotoImage(file=filename)
    label = tk.Label(container, image=profile_img)
    label.grid(row=11, column=1)

  btn_upload = tk.Button(container, text='Upload your profile pcture', command=upload_picture)
  btn_upload.grid(row=12, column=1)

  user_value = lambda: validate_create_account([
    ['firstname', entry_firstname.get()], ['lastname', entry_lastname.get()], ['sex', entry_sex.get()], ['address', entry_adress.get()], ['state', entry_state.get()], ['marital', entry_marital.get()], ['bloodgroup', entry_group.get()], ['genotype', entry_genotype.get()], ['password', entry_password.get()], ['confirm_password', entry_confirm.get()], ['mail', entry_mail.get()]
    ])

  # the submit button, it get all of the user input for validation
  submit_btn = tk.Button(container, text='Create Account', bg='blue', fg=user_frame['bg'],
  activebackground='blue', activeforeground=user_frame['bg'], width=75, pady=15,
  command=user_value)
  
  submit_btn.grid(row=13, column=0, columnspan=2)

  login_btn = tk.Button(container, text='If you already have an account. Login existing account', bg=user_frame['bg'], activebackground=user_frame['bg'], highlightthickness=0, borderwidth=0, command=lambda: cmd.show_frame(create_frame, login_user_account))
  login_btn.grid(row=14, column=0, columnspan=2)


  for widget in container.winfo_children():
    widget.grid_configure(padx=5, pady=5)


# create_user_account()

def patient_window():
  main_frame = tk.Frame(root, bg='#fff', width=width, height=height)
  main_frame.pack()

patient_window()

root.mainloop()