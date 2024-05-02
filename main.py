import re
import tkinter as tk
from tkinter import messagebox, ttk;
from PIL import Image, ImageTk, ImageDraw

import datetime
import calendar

import mysql.connector
from mysql.connector import Error

# import created library
from command import Command as cmd
import os

# os.environ['']
# fonts
roboto_font = ("Roboto", 12, "normal")

def validate_email(email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if(re.search(regex,email)):  
        return True  
    else:  
        return False

def main():
  # creating root window
  global root
  root = tk.Tk()

  # window dimension
  global width
  width = root.winfo_screenwidth()

  global height
  height = root.winfo_screenheight()

  custom_size = str(width) + 'x' + str(height)
  root.geometry(custom_size)

  root.resizable(False, False)
  root.title('MediCare')

  # frame dimension
  global frame_width
  frame_width = width * .5

  global image_tk
  image_tk = None

  # entry point
  create_user_account()


def validate_login():
  try:
    connect = mysql.connector.connect(host='localhost', password='', user='root', database='hospital_patient_data')
    cursor = connect.cursor()

    # fetch exsiting user from databse
    get_user = '''
    SELECT * FROM user
    WHERE mail = %s AND password = %s
    '''
    mail = entry_mail.get().strip()
    password = entry_password.get().strip()
    user = (mail, password)

    cursor.execute(get_user, user)

    user_data = cursor.fetchall()

    if user_data:
      global user_data_list
      user_data_list = list(user_data[0])
      messagebox.showinfo('User data', 'You have login Successfully')
      
      global cur_user
      cur_user = {
      'key': user_data_list[0],
      'first_name': user_data_list[1],
      'last_name': user_data_list[2],
      'user_name': user_data_list[3],
      'sex': user_data_list[4],
      'address': user_data_list[5],
      'state': user_data_list[6],
      'marital_status': user_data_list[7],
      'blood_group': user_data_list[8],
      'genotype': user_data_list[9],
      'password': user_data_list[10],
      'mail': user_data_list[11],
    }
      
    else:
      messagebox.showerror('User Data', 'NO user data found. Enter correct email or password')
      return ''
    
  except Error as e:
    messagebox.showerror('Connection Error', 'There is an error connecting to the database')

  finally:
    if connect.is_connected():
      cursor.close()
      connect.close()

  login_container.forget()
  patient_window()


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
  widget_width = 40
  img_url = 'asset/account_bg.jpg'

  # frame that contains the other frames
  create_frame.forget()

  global login_container
  login_container = tk.Frame(root, width=width, height=height)
  login_container.pack()

  # frame that holds the image
  img_frame(login_container, frame_width, img_url)

  login_frameholder = tk.Frame(login_container, width=frame_width, height=height, bg='#fff')
  login_frameholder.place(x=frame_width, y=0)
  login_frameholder.pack_propagate(flag=False)

  container = tk.Frame(login_frameholder, bg=login_frameholder['bg'])
  container.pack(expand=True, anchor='center')

  label_mail = tk.Label(container, text='Email', bg=login_frameholder['bg'], font=roboto_font)
  global entry_mail
  entry_mail = tk.Entry(container, width=widget_width, highlightthickness=0, font=roboto_font)

  label_mail.grid(row=0, column=0)
  entry_mail.grid(row=1, column=0)

  label_password = tk.Label(container, text='Password', bg=login_frameholder['bg'], font=roboto_font)
  global entry_password
  entry_password = tk.Entry(container, width=widget_width, highlightthickness=0, font=roboto_font, show='*')

  label_password.grid(row=2, column=0)
  entry_password.grid(row=3, column=0)

  submit_btn = tk.Button(container, text='Login', width=39, padx=10, pady=10, bg='blue', fg='#fff', activebackground='blue', activeforeground='#fff', border=0, highlightthickness=0, font=roboto_font, command=lambda: validate_login())
  submit_btn.grid(row=4, column=0)

  create_account_btn = tk.Button(container, text='If you have no existing account. Create account', bg=login_frameholder['bg'], activebackground=login_frameholder['bg'], border=0, highlightthickness=0, font=roboto_font, command=lambda: cmd.show_frame(login_container, create_user_account))
  create_account_btn.grid(row=5, column=0)


  for widget in container.winfo_children():
    widget.grid_configure(padx=15, pady=15)



def validate_create_account(value_arr):
  values = value_arr

  global confirm_pwd
  global pwd
  confirm_pwd = ''
  pwd = ''

  for value in values:
    if value[0] == 'sex' and not (value[1] == 'Male' or value[1] == 'Female'):
      messagebox.showerror('Fill the sex entry', 'Choose an option of Male or Female from the dropdown')
      return ''
      
    if value[0] == 'marital' and not (value[1] == 'Single' or value[1] == 'Married' or value[1] == 'Divorce'):
      messagebox.showerror('Fill the marital entry', 'Choose an option of Single, Married or Divorced from the dropdown')
      return ''
    
    if value[0] == 'bloodgroup' and not (value[1] == 'O+' or value[1] == 'O-' or value[1] == 'AB' or value[1] == 'AB+'):
      messagebox.showerror('Fill the blood group entry', 'Choose an option of O+, O-, AB+ or AB- from the dropdown')
      return ''
    
    if value[0] == 'genotype' and not (value[1] == 'AA' or value[1] == 'AS' or value[1] == 'SS'):
      messagebox.showerror('Fill the genotype entry', 'Choose an option of AA, AS, or SS from the dropdown')
      return ''

    if value[0] == 'mail':
      if not(validate_email(value[1])):
        messagebox.showerror('Invalid Email', 'The email you entered is not valid.')
        return ''
    
    if value[0] == 'password':
      pwd = value[1]
      
    if value[0] == 'confirm_password':
      confirm_pwd = value[1]
    
    if value[1] == '':
      messagebox.showerror('Empty Form', f'All inputs field must be filled: {value[0]}')
      return ''
      
  if not(pwd == confirm_pwd):
    messagebox.showerror('Password Mismatch', 'The password and confirm password do not match.')
    return ''

  try:
    connect = mysql.connector.connect(host='localhost', password='', user='root', database='hospital_patient_data')
    cursor = connect.cursor()

    # CREATE TABLE
    create_table = 'CREATE TABLE IF NOT EXISTS user(id_key INT PRIMARY KEY AUTO_INCREMENT, first_name TEXT, last_name TEXT, username TEXT, sex TEXT, address TEXT, state TEXT, marital_status TEXT, blood_group TEXT, genotype TEXT, password TEXT, mail TEXT)'
    cursor.execute(create_table)

    # Insert User
    insert_user = ''' insert into user(first_name, last_name, username, sex, address, state, marital_status, blood_group, genotype, password, mail) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    '''

    user_data = []
    for value in value_arr:
      user_data.append(value[1])

    user_data.pop(-3)
    tuple(user_data)

    cursor.execute(insert_user, user_data)
    connect.commit()

    login_user_account()

  except Error as e:
    messagebox.showerror('connection error', f'There is an error connectng to the database {e}')
    
  finally:
   if connect.is_connected():
     connect.close()
     cursor.close()

# create user account frame
def create_user_account():
  img_url = 'asset/account_bg.jpg'
  widget_width = 29
  combo_width = 28

  # frame that contains the other frames
  global create_frame
  create_frame = tk.Frame(root, width=width, height=height)
  create_frame.pack()

  # frame the holds the image
  img_frame(create_frame, frame_width, img_url)
  
  # frame that contain user input widget
  user_frame = tk.Frame(create_frame, width=frame_width, height=height, bg='#fff')
  user_frame.pack_propagate(flag=False) # prevents frame from taking the size of widget
  user_frame.place(x=frame_width, y=0)

  container = tk.Frame(user_frame, width=frame_width, bg=user_frame['bg'])
  container.pack(expand=True, anchor='center')

  label_firstname = tk.Label(container, text="First Name", bg=user_frame['bg'], width=widget_width, font=roboto_font, padx=10)
  entry_firstname = tk.Entry(container, width=widget_width, font=roboto_font)

  label_firstname.grid(row=1, column=0)
  entry_firstname.grid(row=2, column=0)

  label_lastname = tk.Label(container, text="Last Name", bg=user_frame['bg'], width=widget_width, font=roboto_font)
  entry_lastname = tk.Entry(container, width=widget_width, font=roboto_font)

  label_lastname.grid(row=1, column=1)
  entry_lastname.grid(row=2, column=1)

  label_username = tk.Label(container, text='Username', bg=user_frame['bg'], width=widget_width, font=roboto_font)
  entry_username = tk.Entry(container, width=widget_width, font=roboto_font)

  label_username.grid(row=3, column=0)
  entry_username.grid(row=4, column=0)

  label_sex = tk.Label(container, text='Sex', bg=user_frame['bg'], width=widget_width, font=roboto_font)
  entry_sex = ttk.Combobox(container, values=['Male', 'Female'], width=combo_width, font=roboto_font)

  label_sex.grid(row=3, column=1)
  entry_sex.grid(row=4, column=1)

  label_address = tk.Label(container, text='Address', bg=user_frame['bg'], width=widget_width, font=roboto_font)
  entry_adress = tk.Entry(container, width=widget_width, font=roboto_font)

  label_address.grid(row=5, column=0)
  entry_adress.grid(row=6, column=0)

  label_state = tk.Label(container, text='State of Origin', bg=user_frame['bg'], width=widget_width, font=roboto_font)
  entry_state = tk.Entry(container, width=widget_width, font=roboto_font)

  label_state.grid(row=5, column=1)
  entry_state.grid(row=6, column=1)

  label_marital = tk.Label(container, text='Marital Status', bg=user_frame['bg'], width=widget_width, font=roboto_font)
  entry_marital = ttk.Combobox(container, value=['Single', 'Married', 'Divorced'], width=widget_width, font=roboto_font)

  label_marital.grid(row=7, column=0)
  entry_marital.grid(row=8, column=0)

  label_group = tk.Label(container, text='Blood Group', bg=user_frame['bg'], width=widget_width, font=roboto_font)
  entry_group = ttk.Combobox(container, value=['O+', 'O-', 'AB', 'AB+'], width=combo_width, font=roboto_font)

  label_group.grid(row=7, column=1)
  entry_group.grid(row=8, column=1)

  label_genotype = tk.Label(container, text='Genotype', bg=user_frame['bg'], width=widget_width, font=roboto_font)
  entry_genotype = ttk.Combobox(container, value=['AA', 'AS', 'SS'], width=combo_width, font=roboto_font)

  label_genotype.grid(row=9, column=0)
  entry_genotype.grid(row=10, column=0)

  label_mail = tk.Label(container, text='Email', bg=user_frame['bg'], width=widget_width, font=roboto_font)
  entry_mail = tk.Entry(container, width=widget_width, font=roboto_font)

  label_mail.grid(row=9, column=1)
  entry_mail.grid(row=10, column=1)

  label_password = tk.Label(container, text='Password', bg=user_frame['bg'], width=widget_width, font=roboto_font)
  entry_password = tk.Entry(container, width=widget_width, font=roboto_font, show='*')

  label_password.grid(row=11, column=0)
  entry_password.grid(row=12, column=0)

  label_confirm = tk.Label(container, text='Confirm Password', bg=user_frame['bg'], width=widget_width, font=roboto_font)
  entry_confirm = tk.Entry(container, width=widget_width, font=roboto_font, show='*')

  label_confirm.grid(row=11, column=1)
  entry_confirm.grid(row=12, column=1)

  # def upload_picture(event=None):
  #   global profile_img
  #   filename = filedialog.askopenfilename()
  #   profile_img = ImageTk.PhotoImage(file=filename)
  #   label = tk.Label(container, image=profile_img)
  #   label.grid(row=11, column=1)

  user_value = lambda: validate_create_account([
    ['firstname', entry_firstname.get()], ['lastname', entry_lastname.get()], ['username', entry_username.get()], ['sex', entry_sex.get()], ['address', entry_adress.get()], ['state', entry_state.get()], ['marital', entry_marital.get()], ['bloodgroup', entry_group.get()], ['genotype', entry_genotype.get()], ['password', entry_password.get()], ['confirm_password', entry_confirm.get()], ['mail', entry_mail.get()]
    ])

  # the submit button, it get all of the user input for validation
  submit_btn = tk.Button(container, text='Create Account', bg='blue', fg=user_frame['bg'],
  activebackground='blue', activeforeground=user_frame['bg'], pady=15,
  command=user_value)
  
  submit_btn.grid(row=13, column=0, columnspan=2, sticky='nswe')

  login_btn = tk.Button(container, text='If you already have an account. Login existing account', bg=user_frame['bg'], activebackground=user_frame['bg'], highlightthickness=0, borderwidth=0, command=lambda: cmd.show_frame(create_frame, login_user_account))
  login_btn.grid(row=14, column=0, columnspan=2)


  for widget in container.winfo_children():
    widget.grid_configure(padx=8, pady=8)


# create_user_account()


# Function to create a circle with an image inside it at the center of the canvas
def create_circle_with_image(canvas, canvas_width, canvas_height, r, image_path):
    # Calculate the circle's center based on canvas dimensions
    x = canvas_width / 2
    y = canvas_height / 2

    # Create a circular mask for the image
    mask = Image.new("L", (r * 2, r * 2), 0)  # 'L' creates a grayscale image
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, r * 2, r * 2), fill=255)  # Create a filled circle mask

    # Load and resize the image to fit within the circle's diameter
    image = Image.open(image_path)
    image_resized = image.resize((r * 2, r * 2), Image.ANTIALIAS)

    # Apply the mask to the image to create a circular effect
    image_circular = Image.new("RGBA", image_resized.size)  # Create a new image with transparency
    image_circular.paste(image_resized, (0, 0), mask=mask)  # Apply the mask to the resized image

    # Convert the circular image to PhotoImage for use in Tkinter
    image_tk = ImageTk.PhotoImage(image_circular)

    # Draw the outer circle on the canvas
    canvas.create_oval(x - r, y - r, x + r, y + r, outline='#ADD8E6', width=2)

    # Place the circular image at the center of the circle
    canvas.create_image(x, y, image=image_tk, anchor='center')

    # Keep a reference to the image to avoid garbage collection
    canvas.image_tk = image_tk

    return image_tk


def schedule_appointment():
  bg_color = '#fff'
  entry_width = 30

  schedule_frame = tk.Frame(dashboard_main, bg=dashboard_main['bg'], width=dashboard_main['width'], height=dashboard_main['height'])
  schedule_frame.place(relx=0.5, rely=0.5, anchor='center')
  schedule_frame.propagate(flag=False)

  # appointment frame
  appointment_frame = tk.Frame(schedule_frame, bg=bg_color)
  appointment_frame.pack()

  label_title = tk.Label(appointment_frame, text='Schedule an Appointment', bg=bg_color, font=('roboto', 16, 'bold'), justify='center')
  label_title.pack()


  # user personal details
  personal_info_frame = tk.Frame(schedule_frame, bg=bg_color)
  personal_info_frame.pack(anchor='w')

  instruction = '''
  Please fill out the following form to schedule your appointment.
  Ensure all required fields are completed accurately.
  '''
  label_instruction = tk.Label(personal_info_frame, text=instruction, bg=bg_color, justify='left')
  label_instruction.grid(column=0, row=0, columnspan=4)

  label_name = tk.Label(personal_info_frame, text='Full Name', bg=bg_color, justify='left', anchor='w')
  label_name.grid(column=0, row=1)

  entry_name = tk.Entry(personal_info_frame, bg=bg_color, width=entry_width)
  entry_name.grid(column=1, row=1)

  label_age = tk.Label(personal_info_frame, text='Age', bg=bg_color, justify='left', anchor='w')
  label_age.grid(column=3, row=1)

  entry_age = tk.Entry(personal_info_frame, bg=bg_color, width=entry_width)
  entry_age.grid(column=4, row=1)

  label_msg = tk.Label(personal_info_frame, text='Email', bg=bg_color, justify='left', anchor='w')
  label_msg.grid(column=0, row=2)

  entry_msg = tk.Entry(personal_info_frame, bg=bg_color, width=entry_width)
  entry_msg.grid(column=1, row=2)

  label_phone = tk.Label(personal_info_frame, text='Phone Number', bg=bg_color, justify='left', anchor='w')
  label_phone.grid(column=3, row=2)

  entry_phone = tk.Entry(personal_info_frame, bg=bg_color, width=entry_width)
  entry_phone.grid(column=4, row=2)

  # clinic section
  clinic_frame = tk.Frame(schedule_frame, bg=bg_color, pady=20)
  clinic_frame.pack(anchor='w')

  label_appointment_details = tk.Label(clinic_frame, bg=bg_color, text='Appointment Details', font=('roboto', 16, 'normal'), anchor='w')
  label_appointment_details.grid(row=0, column=0, columnspan=4)

  label_appointment_type = tk.Label(clinic_frame, bg=bg_color, text='Appointment Type')
  label_appointment_type.grid(row=1, column=0)

  entry_appointment_type = ttk.Combobox(clinic_frame, value=['General Consultation', 'Specialist Visit', 'TeleHealth Consultation'], width=entry_width)
  entry_appointment_type.grid(row=1, column=1)

  label_appointment_time = tk.Label(clinic_frame, bg=bg_color, text='Appointment Time')
  label_appointment_time.grid(row=1, column=2)

  entry_appointment_time = ttk.Combobox(clinic_frame, value=['8:00 a.m. - 11:00 a.m.', '11:00 a.m. - 1:00 p.m.', '1:00 p.m. - 3:00 p.m.', '3:00 p.m. - 5:00 p.m.', '5:00 p.m. - 8:00 p.m.'], width=entry_width)
  entry_appointment_time.grid(row=1, column=3)

  label_preferred_notification = tk.Label(clinic_frame, bg=bg_color, text='Preferred Notification')
  label_preferred_notification.grid(row=2, column=0)

  entry_preferred_notification = ttk.Combobox(clinic_frame, value=['Email', 'SMS', 'Whatsapp'], width=entry_width)
  entry_preferred_notification.grid(row=2, column=1)

  label_appointment_date = tk.Label(clinic_frame, bg=bg_color, text='Appointment Date')
  label_appointment_date.grid(row=2, column=2)

  # dates for appointment
  cur_date = datetime.date.today()
  cur_day = cur_date.day

  cur_month = cur_date.month
  cur_year = cur_date.year
  
  num_days_in_month = calendar.monthrange(cur_year, cur_month)[1]

  dates_from_cur_month = [
    datetime.date(cur_year, cur_month, day) for day in range(cur_day, num_days_in_month + 1)
  ]

  entry_appointment_date = ttk.Combobox(clinic_frame, value=dates_from_cur_month, width=entry_width)
  entry_appointment_date.grid(row=2, column=3)

  schedule_appointment_button = tk.Button(schedule_frame, text='Confirm and Submit Schedule', bg=btn_color, fg=bg_color, activebackground=btn_hover, padx=10, pady=10, activeforeground=bg_color, width=50 , command=lambda: validate_schedule())
  schedule_appointment_button.pack()

  def validate_schedule():
    global user_schedule_data
    user_schedule_data = {
      'full_name': entry_name.get(),
      'age': entry_age.get(),
      'mail': entry_msg.get(),
      'mobile_num': entry_phone.get(),
      'appointment_type': entry_appointment_type.get(),
      'appointment_time': entry_appointment_time.get(),
      'appointment_date': entry_appointment_date.get(),
      'notification': entry_preferred_notification.get()
      }

    user_schedule_entry = {
      'full_name': entry_name,
      'age': entry_age,
      'mail': entry_msg,
      'mobile_num': entry_phone,
      'appointment_type': entry_appointment_type,
      'appointment_time': entry_appointment_time,
      'appointment_date': entry_appointment_date,
      'notification': entry_preferred_notification
      }
        
    for key, value in user_schedule_data.items():
      if not(value):
        messagebox.showerror('Entry Error', f'The {key} is empty')
        return ''

      if key == 'mobile_num' and (len(value) < 10 or len(value) > 15):
        messagebox.showerror('Entry Error', f'Phone number must be between 10 and 15 characters.')
        return ''

      if key == 'appointment_type' and not(value == 'General Consultation' or value == 'Specialist Visit' or value == 'TeleHealth Consultation'):
        messagebox.showerror('Entry Error', f'Provide a correct value at entry {key}')
        return ''

      if key == 'notification' and not(value == 'Email' or value == 'SMS' or value == 'Whatsapp'):
        messagebox.showerror('Entry Error', 'Provide a correct value at entry {key}')
        return ''
      
    try:
      connect = mysql.connector.connect(host='localhost', password='', user='root', database='hospital_patient_data')
      cursor = connect.cursor()

      # CREATE TABLE
      create_table = 'CREATE TABLE IF NOT EXISTS user_schedule(id_key INT PRIMARY KEY AUTO_INCREMENT, full_name TEXT, age INT, mail TEXT, mobile_number VARCHAR(15), appointment_type TEXT, appointmen_time TEXT, appointment_date TEXT, notification TEXT)'
      cursor.execute(create_table)

      # Insert Schedule
      insert_schedule = ''' insert into user_schedule(full_name, age, mail, mobile_number, appointment_type, appointment_time, appointment_date, notification) values(%s, %s, %s, %s, %s, %s, %s, %s)
      '''

      user_data = []
      for key, value in user_schedule_data.items():
        user_data.append(value)

      # convert user_data list to a tuple
      tuple(user_data)

      cursor.execute(insert_schedule, user_data)
      connect.commit()

      messagebox.showinfo('Successful', 'Hurray! your apppoinment as been scheduled successfully')

      # clear entry inputs of form
      cmd.clear_input(user_schedule_entry)

    except Error as e:
      messagebox.showerror('Connection Error', f'There is an error connecting to the database: {e}')
    finally:
      if connect.is_connected():
        connect.close()
        cursor.close()

  for child in schedule_frame.winfo_children():
    child.pack_configure(padx=20, pady=15)

  for child in personal_info_frame.winfo_children():
    child.grid_configure(padx=10, pady=10)

  for child in clinic_frame.winfo_children():
    child.grid_configure(padx=10, pady=10)

def display_appointment():
  bg_color = '#fff'
  schedule_frame = tk.Frame(dashboard_main, bg=dashboard_main['bg'], width=dashboard_main['width'], height=dashboard_main['height'], padx=10, pady=10)
  schedule_frame.place(relx=0.5, rely=0.5, anchor='center')
  schedule_frame.propagate(flag=False)

  label_title = tk.Label(schedule_frame, text='My Appointments', bg=bg_color, font=('roboto', 14, 'bold'))
  label_title.pack(anchor='w')

  try:
    connect = mysql.connector.connect(host='localhost', password='', user='root', database='hospital_patient_data')
    cursor = connect.cursor()

    get_appointment = '''
    SELECT * FROM user_schedule
    where mail = %s
    '''
    cur_user_mail = cur_user['mail']

    cursor.execute(get_appointment, (cur_user_mail, ))
    appointment_data = cursor.fetchall()

    for item in appointment_data:
      appointee_frame = tk.Frame(schedule_frame, bg=bg_color)
      appointee_frame.pack(anchor='w')

      label_appointee = tk.Label(appointee_frame, text=f'Name of Appointee: {item[1]}', bg=bg_color, justify='left')
      label_appointee.grid(row=0, column=0, sticky='w')

      label_appointment_type = tk.Label(appointee_frame, text=f'Appointment Type: {item[-4]}', bg=bg_color, justify='left')
      label_appointment_type.grid(row=0, column=1, sticky='w')

      label_appointment_time = tk.Label(appointee_frame, text=f'Appointment Time: {item[-3]}', bg=bg_color, justify='left')
      label_appointment_time.grid(row=0, column=2, sticky='w')

      label_appointment_date = tk.Label(appointee_frame, text=f'Appointment Date: {item[-2]}', bg=bg_color, justify='left')
      label_appointment_date.grid(row=1, column=0, sticky='w')

      label_appointment_notification = tk.Label(appointee_frame, text=f'Notification: {item[-1]}', bg=bg_color, justify='left')
      label_appointment_notification.grid(row=1, column=1, sticky='w')

      for child in appointee_frame.winfo_children():
        child.grid_configure(padx=10, pady=10)

  except Error as e:
    messagebox.showerror('Connection Error', f'There is an error connecting to the database: {e}')

  finally:
    if connect.is_connected():
      cursor.close()
      connect.close()

  for child in schedule_frame.winfo_children():
    child.pack_configure(padx=10, pady=10)

def logout():
  # the dialog window to show yes or no
  response = messagebox.askyesno('Logout', 'Are you sure you want to logout?')

  if response:
    login_user_account()
    dashboard_frame.forget()
  else:
    return ''

def patient_window():
  bg_color = '#fff'
  global btn_color, btn_hover
  btn_color = '#12548A'
  btn_hover = '#2B6BA0'

  nav_width = width  * 0.3
  main_width = width * 0.7
  canvas_width = 200
  canvas_height = 200
  radius = 100

  btn_width = 35
  btn_padh = 15
  image_path = "asset/doctor.jpeg"

  global dashboard_frame
  dashboard_frame = tk.Frame(root, bg=bg_color, width=width, height=height)
  dashboard_frame.pack()

  # the navigation part
  dashboard_navigation = tk.Frame(dashboard_frame, bg='#9CC3E4', width=nav_width, height=height, pady=50)
  dashboard_navigation.place(x=0, y=0)
  dashboard_navigation.pack_propagate(flag=False)

  canvas = tk.Canvas(dashboard_navigation, width=canvas_width, height=canvas_height, bg="#9CC3E4", highlightthickness=0)
  canvas.pack()

  # Draw a circle with an image at the center
  global image_tk
  image_tk = create_circle_with_image(canvas, canvas_width, canvas_height, radius, image_path)

  # dashboard navigation widget
  btn_schedule = tk.Button(dashboard_navigation, text='Schedule Appointment', width=btn_width, fg=bg_color, bg=btn_color, highlightbackground=btn_color, highlightcolor=btn_color, activebackground=btn_hover, activeforeground=bg_color, pady=btn_padh, font=roboto_font, command=lambda: schedule_appointment())
  btn_schedule.pack()

  btn_appointment = tk.Button(dashboard_navigation, text='My Appointments', width=btn_width, fg=bg_color, bg=btn_color, highlightbackground=btn_color, highlightcolor=btn_color, activebackground=btn_hover, activeforeground=bg_color, pady=btn_padh, font=roboto_font, command=lambda: display_appointment())
  btn_appointment.pack()

  btn_profile = tk.Button(dashboard_navigation, text='Logout', width=btn_width, fg=bg_color, bg=btn_color, highlightbackground=btn_color, highlightcolor=btn_color, activebackground=btn_hover, activeforeground=bg_color, pady=btn_padh, font=roboto_font, command=lambda: logout())
  btn_profile.pack()

  for widget in dashboard_navigation.winfo_children():
    widget.pack_configure(pady=20)

  # view
  global dashboard_main
  dashboard_main = tk.Frame(dashboard_frame, bg=bg_color, width=main_width, height=height)
  dashboard_main.place(x=nav_width, y=0)

  welcome_frame = tk.Frame(dashboard_main, bg=bg_color)
  welcome_frame.place(relx=0.5, rely=0.5, anchor='center')

  cur_user_name = cur_user.get('user_name')

  label_welcome = tk.Label(welcome_frame, text=f'Welcome {cur_user_name.upper()}, so good to have you here. \n {cur_user_name.upper()}, you can schedule an appointment right now', bg=bg_color, font=roboto_font)
  label_welcome.pack(anchor='center')


main()
root.mainloop()
