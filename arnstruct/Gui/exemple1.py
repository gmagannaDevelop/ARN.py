import PySimpleGUI as sg



sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.
frame_seq1 = [
    [sg.FileBrowse('Importer')],
    [sg.Text("Entrer manuellement sa séquence nucléotidique")], [sg.InputText()],
    [sg.Text("ou", justification='center')],
    [sg.Text("Entrer manuellement sa structure secondaire")], [sg.InputText()],
    [sg.Text('Structure 1')]
    ]

frame_seq2 = [
        [sg.FileBrowse('Importer')],
        [sg.Text("Entrer manuellement sa séquence nucléotidique")], [sg.InputText()],
        [sg.Text("ou", justification='center')],
        [sg.Text("Entrer manuellement sa structure secondaire")], [sg.InputText()],
        [sg.Text('Structure 2')],

]

layout = [  [sg.Frame('ARN 1', frame_seq1), sg.VerticalSeparator(),sg.Frame('ARN 2', frame_seq2)],
            [sg.Button('Comparer')]
            ]
# Create the Window
window = sg.Window('Comparaison de deux séquences ARN',  layout, size=(710, 800))
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()

    if event == 'Importer':
        sg.FileBrowse()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    print('You entered ', values[0])

window.close()