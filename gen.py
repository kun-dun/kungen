#-------------------------------------------------------------------------------
# Name:        GEN
# Purpose:     ARVORE GENEALOGICA COM DASH - FUNCIONANDO
#              Usadso dashboard.render4.com para expor na WB
#              Vide video YOUTUBE : https://www.youtube.com/watch?v=H16dZMYmvqo
#
# Author:      ylalo
#
# Created:     27-11-2024
# Copyright:   (c) ylalo 2024
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#import subprocess
from dash import Dash, html,Input,Output,callback
from dash import dcc
import dash_cytoscape as cyto
import os
import json
import sys
import webbrowser
import dearpygui.dearpygui as dpg
#import dearpygui.demo as demo

def showgui():
    dpg.create_context()
    dpg.create_viewport(title='Custom Title', width=600, height=300)

    with dpg.window(label="Example Window"):
        dpg.add_text("Hello, world")
        dpg.add_button(label="Save")
        dpg.add_input_text(label="string", default_value="Quick brown fox")
        dpg.add_slider_float(label="float", default_value=0.273, max_value=1)

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

#print(os.__version__)

adir = os.getcwd()


#afile =adir+"\\data\\js.txt"
afile = "js.txt"
aNodes=[]
with open(afile, "r",) as meu_json:
    personnes = json.load(meu_json)

gen = Dash(__name__)
server = gen.server  # for deploy dash tools

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
        #print(aNodes)

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

def _from_rgb(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    return "#%02x%02x%02x" % rgb


gen.layout = html.Div([
    cyto.Cytoscape(
        id='cytoscape-event-callbacks-1',
        layout={'name': 'preset'},
        style={'width': '100%', 'height': '400px'},
        stylesheet=my_stylesheet,
        elements=aNodes

    ), html.Pre(id='cytoscape-tapNodeData-json', style=styles['pre']),
       html.Pre(id='cytoscape-mouseoverNodeData-json', style=styles['pre'])
])


@callback(Output('cytoscape-tapNodeData-json', 'children'),
          Input('cytoscape-event-callbacks-1', 'tapNodeData'))


def displayTapNodeData(data):
    if data:
      #qt5(data)
      #showwnd()
      #print(data)
      showgui()
      return ""
"""
      with open('data.json', 'w') as outfile:
        str_ = json.dumps(data,ensure_ascii=False)

        outfile.write(str_)
      os.startfile('perso.exe')

      return ""#qt5(data)
"""

if __name__ == '__main__':
    webbrowser.open_new(url='http://127.0.0.1:8050')
    gen.run(debug=False)
