import PySimpleGUI as sg

from config import settings
from services.hymns import Hymns
from services.utils import create_directory, get_sunday

sg.theme('Dark')  # Let's set our own color theme

THIS_SUNDAY = get_sunday()
DEFAULT_DATE = (THIS_SUNDAY.month, THIS_SUNDAY.day, THIS_SUNDAY.year)
CURRENT_LAYOUT = 'HOME'
LAYOUTS = ['HOME', 'START', 'CREATE']

def toggle_layout(
    new: str, 
    layouts: list[str] = LAYOUTS
) -> None:
    '''Toggle between layouts.'''
    global CURRENT_LAYOUT
    
    if new is None or new.upper() not in layouts:
        return

    window[CURRENT_LAYOUT].update(visible=False)
    CURRENT_LAYOUT = new.upper()
    window[new.upper()].update(visible=True)


menu = [
    ['File', ['Open', 'Save', 'Properties', 'Exit']],
    ['Edit', ['Undo', 'Paste', ['Normal', 'Special']]],
    ['Help', ['About...']]
]

# STEP 1 define the layout
home = sg.Column(
    [
        [sg.Text('Hosanna Worship Services', font=('Helvetica', 34))],
        [sg.Button('Start', button_color=('white', 'springgreen4'), size=(10, 1), border_width=0)],
        [sg.Button('Exit', button_color=('white', 'firebrick3'), size=(10, 1), border_width=0)],
    ], 
    element_justification='c', 
    key='HOME'
)

create_service = sg.Column(
    [
        [sg.Text('Create Service', font=('Helvetica', 34))],
        [
            sg.Push(),
            sg.Text('Date', size=(8, 1)), 
            sg.Input(THIS_SUNDAY, key='DATE'), 
            sg.CalendarButton('Select Day', target='DATE', format='%Y-%m-%d', default_date_m_d_y=DEFAULT_DATE, no_titlebar=False)
        ],
        [sg.Button('Create', button_color=('white', 'springgreen4'), size=(10, 1))],
    ], 
    element_justification='c', 
    visible=False, 
    key='START'
)

add_hymns = sg.Column(
    [
        [sg.Text('Add Hymns', font=('Helvetica', 34))],
        [sg.Text('', key='HYMN_LIST', size=(50, 10), font=('Helvetica', 12), justification='l', border_width=1, relief='sunken')],
        [
            sg.Push(),
            sg.Text('Hymn Number', size=(12, 1)), 
            sg.Input(key='HYMN_NUMBER')
        ],
        [
            sg.Button('Add', button_color=('white', 'springgreen4'), size=(10, 1)),
            sg.Button('Save', button_color=('white', 'green'), size=(10, 1))
        ],
    ], 
    element_justification='c', 
    visible=False, 
    key='CREATE'
)

add_liturgy = sg.Column(
    [
        [sg.Text('Add Liturgy', font=('Helvetica', 34))],
        [sg.Text('', key='LITURGY_LIST', size=(50, 10), font=('Helvetica', 12), justification='l', border_width=1, relief='sunken')],
        [
            sg.Push(),
            sg.Text('Liturgy', size=(12, 1)), 
            sg.Multiline(key='LITURGY')
        ],
        [
            sg.Button('Add', button_color=('white', 'springgreen4'), size=(10, 1)),
            sg.Button('Save', button_color=('white', 'green'), size=(10, 1))
        ],
    ], 
    element_justification='c', 
    visible=False, 
    key='LITURGY'
)

layout = [
    [sg.Menu(menu)],
    [sg.VPush()],
    [
        sg.Push(),
        sg.pin(home), 
        sg.pin(create_service),
        sg.pin(add_hymns),
        sg.Push()
    ],
    [sg.VPush()]
]

#STEP 2 - create the window
window = sg.Window(
    'Hosanna Worship Services', 
    layout, 
    size=(1200, 800), 
    icon='data/icon.ico',
    finalize=True
)

# STEP3 - the event loop
while True:
    # Read the event that happened and the values dictionary
    event, values = window.read()   
    print(event, values)

    toggle_layout(event)

    # If user closed window with X or if user clicked "Exit" button then exit
    if event == sg.WIN_CLOSED or event == 'Exit':     
        break

    if event == 'Create':
        path = f'{settings.LOCAL_DIR}/hosanna/services/{values["DATE"]}'
        create_directory(path)
        hymns = Hymns(values['DATE'])

    if event == 'Add':
        hymns.add_hymn(int(values['HYMN_NUMBER'])) 
        window['HYMN_LIST'].update('\n'.join([f'{hymn.Title} (ELW {hymn.Number})' for hymn in hymns.hymns]))

    if event == 'Save':
        hymns.save_hymns()

window.close()
