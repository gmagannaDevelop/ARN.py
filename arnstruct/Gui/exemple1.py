
import PySimpleGUI as sg
from arnstruct.core.sequence import Sequence
from arnstruct.core.parentheses import Parentheses
from arnstruct.core.datastructures import Tree

sg.theme('DarkTeal2')   # Add a touch of color

# All the stuff inside your window.
frame_seq1 = [
    [sg.Text('Importer un fichier'), sg.FileBrowse('Importer')],
    [sg.Text("Entrer manuellement sa séquence nucléotidique")], [sg.InputText(key='-SEQNT1-')],

    [sg.Text("ou", justification='center')],
    [sg.Text("Entrer manuellement sa structure secondaire")], [sg.InputText(key="-STRUCT1-")],
    [sg.Text('Structure 1')]
    ]

frame_seq2 = [
        [sg.Text('Importer un fichier'), sg.FileBrowse('Importer')],
        [sg.Text("Entrer manuellement sa séquence nucléotidique")], [sg.InputText(key='-SEQNT2-')],


        [sg.Text("ou", justification='center')],
        [sg.Text("Entrer manuellement sa structure secondaire")], [sg.InputText(key="-STRUCT2-")],
        [sg.Text('Structure 2')],

]

frame_motif = [
    [sg.Text('Quelle taille de motif voulez-vous ?'), sg.InputText(key='MOTIFSIZE')]
]

frame_res = [
    [sg.Text("Structure commune")]
]
layout = [  [sg.Frame('ARN 1', frame_seq1), sg.VerticalSeparator(),sg.Frame('ARN 2', frame_seq2)],
            [sg.Frame('Recherche de motifs communs', frame_motif)], [sg.Button('Comparer les motifs de séquence', key='-COMPAREMOTIF-')],
            [sg.Button('Comparer les structures', key='-COMPARESTRUCT-')]
            ]

layout_error = [
    [sg.Text("Veuillez vérifier le format des entrées")]
]
# Create the Window
window = sg.Window('Comparaison de deux séquences ARN',  layout, size=(710, 800))

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED: # if user closes window or clicks cancel
        break


    if event == '-COMPAREMOTIF-':

        try:
            seq1 = Sequence(values['-SEQNT1-'])
            seq2 = Sequence(values['-SEQNT2-'])

            th_str = values['MOTIFSIZE']
            th_seq = int(th_str)
            motifs_seq = seq1.motif_search(seq2, th_seq)
            print("Motifs communs de taille %d" % th_seq, motifs_seq)


        except ValueError:

           sg.popup("Veuillez vérifier le format des entrées")


    if event == '-COMPARESTRUCT-':
        try:
            seq1 = Sequence(values['-SEQNT1-'])
            seq2 = Sequence(values['-SEQNT2-'])
            struct1 = Parentheses.validate_and_convert(values["-STRUCT1-"])
            struct2 = Parentheses.validate_and_convert(values["-STRUCT2-"])

            tree1 = Tree.from_parentheses_and_sequence(struct1, seq1)
            tree2 = Tree.from_parentheses_and_sequence(struct2, seq2)

            max_tree = tree1.maximum_common_subtree(tree2)
            print(tree1, tree2, max_tree, sep="\n")

        except ValueError:
            sg.popup("Veuillez vérifier le format des entrées")
        #Quand on clique sur 'Comparer'
        # maintenant tu peux deja faire :
        # my_seq = Sequence(string)


window.close()