import PySimpleGUI as sg
from arnstruct.core.sequence import Sequence
from arnstruct.core.structure import Structure


sg.theme("DarkTeal2")  # Add a touch of color
# All the stuff inside your window.
frame_seq1 = [
    [sg.Text("Importer un fichier"), sg.FileBrowse("Importer")],
    [sg.Text("Entrer manuellement sa séquence nucléotidique")],
    [sg.InputText(key="-SEQNT1-")],
    [sg.Button("Valider", key="-SUB_SEQ1-")],
    [sg.Text("ou", justification="center")],
    [sg.Text("Entrer manuellement sa structure secondaire")],
    [sg.InputText(key="STRUCT1")],
    [sg.Text("Structure 1")],
]

frame_seq2 = [
    [sg.Text("Importer un fichier"), sg.FileBrowse("Importer")],
    [sg.Text("Entrer manuellement sa séquence nucléotidique")],
    [sg.InputText(key="-SEQNT2-")],
    [sg.Button("Valider", key="-SUB_SEQ2-")],
    [sg.Text("ou", justification="center")],
    [sg.Text("Entrer manuellement sa structure secondaire")],
    [sg.InputText(key="STRUCT2")],
    [sg.Text("Structure 2")],
]

frame_motif = [
    [sg.Text("Quelle taille de motif voulez-vous ?"), sg.InputText(key="MOTIFSIZE")]
]

layout = [
    [
        sg.Frame("ARN 1", frame_seq1),
        sg.VerticalSeparator(),
        sg.Frame("ARN 2", frame_seq2),
    ],
    [sg.Frame("Recherche de motifs communs", frame_motif)],
    [sg.Button("Comparer", key="-COMPARE-")],
]
# Create the Window
window = sg.Window("Comparaison de deux séquences ARN", layout, size=(710, 800))
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:  # if user closes window or clicks cancel
        break

    if event == "-COMPARE-":
        seq1 = Sequence(values["-SEQNT1-"])
        seq2 = Sequence(values["-SEQNT2-"])

        struct1 = Structure(values("STRUCT1"))
        struct2 = Structure(values("STRUCT2"))

        try:
            th_str = values["MOTIFSIZE"]
            th = int(th_str)
            motifs_seq = seq1.motifSearch(seq2._sequence, th)
            print("Motifs communs de taille %d" % th, motifs_seq)

            motifs_struct = struct1.motif_search_struct(struct2._struct)

        except ValueError as e:
            print(f"Nan mais on a dit une taille !")

    if event == "-SUB_SEQ2-":
        print("submit2")
        # Quand on clique sur 'Comparer'
        # maintenant tu peux deja faire :
        # my_seq = Sequence(string)


window.close()