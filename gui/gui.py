import PySimpleGUI as sg

sg.theme('Dark')  # Let's set our own color theme

menu = [
    ['File', ['Open', 'Save', 'Exit', 'Properties']],
    ['Edit', ['Paste', ['Special', 'Normal',], 'Undo']],
    ['Help', 'About...']
]

# STEP 1 define the layout
layout = [ 
    [sg.Menu(menu)],
    [sg.Text('This is a very basic PySimpleGUI layout')],
    [sg.Input()],
    [sg.Button('Button'), sg.Button('Exit')]
]

#STEP 2 - create the window
window = sg.Window('Hosanna Worship Services', layout, size=(1200, 800))

# STEP3 - the event loop
while True:
    # Read the event that happened and the values dictionary
    event, values = window.read()   
    print(event, values)

    # If user closed window with X or if user clicked "Exit" button then exit
    if event == sg.WIN_CLOSED or event == 'Exit':     
      break
    if event == 'Button':
      print('You pressed the button')

window.close()