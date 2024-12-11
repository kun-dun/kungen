#-------------------------------------------------------------------------------
# Name:        dash
# Purpose:     ARVORE GENEALOGICA COM DASH - FUNCIONANDO
#
# Author:      ylalo
#
# Created:     27-11-2024
# Copyright:   (c) ylalo 2024
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import subprocess
from dash import Dash, html,Input,Output,callback
from dash import dcc
import dash_cytoscape as cyto
import os
import json
import sys
from tkinter import *
from PIL import Image, ImageTk
import webbrowser
from delphivcl import *
from Unit8 import Form8
from PySide6.QtWidgets import QApplication, QLabel
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTreeView, QFileSystemModel,QListWidget
from PyQt5.QtGui import QPalette, QColor,QFont,QPixmap
from PyQt5.QtCore import Qt,QModelIndex

from PyQt5.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDateTimeEdit,
    QDial,
    QDoubleSpinBox,
    QFontComboBox,
    QLabel,
    QLCDNumber,
    QLineEdit,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QSlider,
    QSpinBox,
    QTimeEdit,
    QVBoxLayout,
    QWidget
)




class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        #self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        #self.setGeometry(0, 0, 400, 300)
        self.setWindowTitle("GENEALOGIE")
        self.setFixedSize(600, 300)


    def lstclicked(self, clickedItem):
        print (clickedItem.text() + " got clicked")
        subprocess.run(["powershell", clickedItem.text()], shell=True)

###############################################################"




def qt5(adata):

    appqt5 = QApplication(sys.argv)


    window = MainWindow()

    window.list1 = QLabel('Documents Annexes', window)
    window.list1.setFont(QFont("Verdana",12))
    window.list1.setGeometry(0,150,500,20)
    window.list1.setStyleSheet('color:blue;font-weight:bold')


    path = "d:\\"
    files = os.listdir(path)

    window.listWidget = QListWidget(window)
    window.listWidget.setGeometry(0,170,400,100)
    window.listWidget.setFont(QFont("Verdana",12))
    window.listWidget.setStyleSheet('color:green;')
    window.listWidget.itemClicked.connect(window.lstclicked)


    # Print the files
    for file in files:
       window.listWidget.addItem(file)



###########################################################
    window.label1 = QLabel(adata['nom']+ ' '+ adata['prenoms']+ ' - Sexe : ' + adata['sexe'], window)
    window.label1.setFont(QFont("Verdana",14))
    window.label1.setGeometry(0,0,500,20)
    window.label1.setStyleSheet('color:blue;font-weight:bold')
    window.label1.setAlignment(Qt.AlignLeft | Qt.AlignTop)

    window.label2 = QLabel('(Né(e) en : '+adata['naissance'], window)
    window.label2.setFont(QFont("Verdana",12))
    window.label2.setGeometry(0,20,500,20)
    window.label2.setStyleSheet('color:blue;font-weight:bold')
    window.label2.setAlignment(Qt.AlignLeft | Qt.AlignTop)

    window.label3 = QLabel(adata['villenaiss']+ '-' +adata['paysnaiss'], window)
    window.label3.setFont(QFont("Verdana",12))
    window.label3.setGeometry(0,40,500,20)
    window.label3.setStyleSheet('color:blue;font-weight:bold')
    window.label3.setAlignment(Qt.AlignLeft | Qt.AlignTop)
    if adata['sexe']=="F":
        window.label4 = QLabel('Nom de Jeune Fille : : '+adata["nomjeunefille"], window)
        window.label4.setFont(QFont("Verdana",12))
        window.label4.setGeometry(0,60,500,20)
        window.label4.setStyleSheet('color:blue;font-weight:bold')
        window.label4.setAlignment(Qt.AlignLeft | Qt.AlignTop)

    window.label4 = QLabel('Marié le '+ '-' +adata['marie'], window)
    window.label4.setFont(QFont("Verdana",12))
    window.label4.setGeometry(0,80,500,20)
    window.label4.setStyleSheet('color:blue;font-weight:bold')
    window.label4.setAlignment(Qt.AlignLeft | Qt.AlignTop)

    window.label5 = QLabel('Profession : '+adata['profession'], window)
    window.label5.setFont(QFont("Verdana",12))
    window.label5.setGeometry(0,100,500,20)
    window.label5.setStyleSheet('color:blue;font-weight:bold')
    window.label5.setAlignment(Qt.AlignLeft | Qt.AlignTop)

    if not(adata['deces']==''):
        window.label6 = QLabel('Décédé en : '+adata['deces']+ ' à '+adata['lieudeces'], window)
        window.label6.setFont(QFont("Verdana",12))
        window.label6.setGeometry(0,120,500,20)
        window.label6.setStyleSheet('color:blue;font-weight:bold')
        window.label6.setAlignment(Qt.AlignLeft | Qt.AlignTop)

    if not(adata['inhume']==''):
        window.label6 = QLabel('Inhumé en : '+adata['inhume'], window)
        window.label6.setFont(QFont("Verdana",12))
        window.label6.setGeometry(0,140,500,20)
        window.label6.setStyleSheet('color:blue;font-weight:bold')
        window.label6.setAlignment(Qt.AlignLeft | Qt.AlignTop)

    window.labelpic =QLabel(window)
    window.labelpic.setGeometry(400,0,150,150)
    pixmap=QPixmap('annick.jpg')
    window.labelpic.setPixmap(pixmap)
    window.labelpic.setScaledContents(True)



###########################################################
    window.show()  # IMPORTANT!!!!! Windows are hidden by default.
    appqt5.exec()

def shopy():
  app = QApplication(sys.argv)
#########################################################################
  label = QLabel('Hello, PySide6!')

#######################################################################


  label.show()
  sys.exit(app.exec_())

def showf():
  fm=Form8(Application)
  fm.ShowModal()

root = Tk()  # create a root widget
swi = root.winfo_screenwidth()
she = root.winfo_screenheight()

cwd = os.getcwd()
personnes=[]
afile =cwd+"\\genjean.txt"
#afile = 'E:\develop\Python\Diagramas\Genealogie\genjean.txt'
aNodes=[]
with open(afile, "r",encoding='utf-8') as meu_json:
    personnes = json.load(meu_json)

app = Dash(__name__)
server = app.server

def criadash():
    try:
        tPos={}
        tdata={}
        tid={}
        tfrom={}
        tedge={}
        #i=1
        for n in personnes:
           anom=n["PRENOMS"]+" "+n["NOM"]
           tpos={
                  "x":n["x"],
                  "y":n["y"]
                }

           tid={
                    "id":str(n["PERSONNEID"]),
                    "label":anom,
                    "personneid":n["PERSONNEID"],
                    "familleid":n["FAMILLEID"],
                    "pere":n["PERE"],
                    "mere":n["MERE"],
                    "nom":n["NOM"],
                    "prenoms":n["PRENOMS"],
                    "naissance":n["NAISSANCE"],
                    "profession":n["PROFESSION"],
                    "nomjeunefille":n["NOMJEUNEFILLE"],
                    "deces":n["DECES"],
                    "lieudeces":n["LIEUDECES"],
                    "adresse":n["ADRESSE"],
                    "ville":n["VILLE"],
                    "pays":n["PAYS"],
                    "villenaiss":n["VILLENAISS"],
                    "paysnaiss":n["PAYSNAISS"],
                    "baptise":n["BAPTISE"],
                    "marie":n["MARIE"],
                    "inhume":n["INHUME"],
                    "sexe":n["SEXE"],
                    "observ":n["OBSERV"],
                    "observ1":n["OBSERV1"],
                    "conjoint":n["CONJOINT"],
                    "tel1":n["TEL1"],
                    "tel2":n["TEL2"],
                    "tel3":n["TEL3"],
                    "twitter":n["TWITTER"],
                    "mail":n["MAIL"],
                    "cep":n["CEP"],
                    "skype":n["SKYPE"],
                    "photo":n["PHOTO"],
                    "photoextension":n["PHOTOEXTENSION"],
                    "conjuge":n["CONJUGE"],
                    "x":n["x"],
                    "y":n["y"],
                    "color":n["COLOR"]

                  }
           if n["SEXE"] == "F":
                tdata= {"data":tid,
                 "position":tpos,
                 "classes":"pink"}

           else:
                tdata= {"data":tid,
                 "position":tpos,
                 "classes":"green",
                 "locked":True
                 }
           #print(tdata)


           aNodes.append(tdata)


        for n in personnes:
           if not n["PERE"] == 0:
            tfrom={
                    "source":str(n["PERSONNEID"]),
                    "target":str(n["PERE"])
                  }
            tedge={
                     "data":tfrom
                  }
           elif not n["CONJOINT"] == 0:
            tfrom={
                    "source":str(n["PERSONNEID"]),
                    "target":str(n["CONJOINT"]),
                  }
            tedge={
                     "data":tfrom
                  }

           aNodes.append(tedge)
        print(aNodes)

    except:
        print('Erro ID ----> ',n["PERSONNEID"])
        sys.exit(0)

criadash()
#print(aNodes)


#print(afile)
#########################################################

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

my_stylesheet = [
    # Group selectors
    {
        'selector': 'node',
        'style': {
            'content': 'data(label)'
        }
    },

    # Class selectors

    {
        'selector': '.pink',
        'style': {
            'background-color': 'pink',
            'line-color': 'pink',
            "font-size":"6",
            "text-wrap": "wrap",
            'line-height': '2',
            "text-max-width": 40,
            'text-halign': 'center',
                }
    },
     {
        'selector': '.yellow',
        'style': {
            'background-color': 'yellow',
            'line-color': 'yellow',
            "font-size":"6",
             "text-wrap": "wrap",
              'line-height': '2',
             "text-max-width": 40
                }
    },
    {
        'selector': '.green',
        'style': {
            'background-color': 'green',
            'line-color': 'green',
            "font-size":"6",
             "text-wrap": "wrap",
             "text-max-width": 40
        }
    }
]
#######################

def ShowFrame(adata):
    arow = 0
    root = Tk()  # create a root widget
    root.title("Données Personnelles")
    root.configure(background="white")
    root.minsize(300, 300)  # width, height
    #root.title("Frame Example")
    #root.config(bg="skyblue")
    root.config(bd="10")
    root.attributes('-topmost',True)

    root.mainloop()



def _from_rgb(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    return "#%02x%02x%02x" % rgb

class TodoApp(Form):

    def __init__(self, Owner):
        self.Caption =  "Données Personnelles"
        self.SetBounds(100, 100, 700, 500)


def ShowPerso():
    Application.Initialize()
    appForm = TodoApp(Application)

    appForm.Show()
    FreeConsole()
    Application.Run()
    appForm.destroy()


app.layout = html.Div([
    cyto.Cytoscape(
        id='cytoscape-event-callbacks-1',
        layout={'name': 'preset'},
        style={'width': '100%', 'height': '400px'},
        stylesheet=my_stylesheet,
        elements=aNodes

    ), html.Pre(id='cytoscape-tapNodeData-json', style=styles['pre']),
       html.Pre(id='cytoscape-mouseoverNodeData-json', style=styles['pre'])
])

def getPhoto(loc):

    return PIL.ImageTk.PhotoImage(PIL.Image.open(loc))

@callback(Output('cytoscape-tapNodeData-json', 'children'),
          Input('cytoscape-event-callbacks-1', 'tapNodeData'))


def displayTapNodeData(data):
    if data:
      qt5(data)
      return ""


if __name__ == '__main__':
    webbrowser.open_new(url='http://127.0.0.1:8050')

    app.run(debug=False)
