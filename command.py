class Command:
  '''
  This class contains commands thaat can be used through the aid of button
  '''

  def show_frame(destroy_frame, func):
    '''
    This is used to destroy an existing frame as a result of argument pass to the parameter.
    '''
    # frame.destroy()
    print(destroy_frame, func)
    func()
    destroy_frame.forget()


Command()