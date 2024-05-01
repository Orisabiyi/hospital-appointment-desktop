import tkinter as tk

class Command:
  '''
  This class contains commands thaat can be used through the aid of button
  '''

  def show_frame(destroy_frame, func):
    '''
    This is used to destroy an existing frame as a result of argument pass to the parameter.
    '''
    # frame.destroy()
    func()
    destroy_frame.forget()
  
  def clear_input(objInput):
    for key, values in objInput.items():
      values.delete(0, tk.END)


Command()