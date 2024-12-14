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
import subprocess
from dash import Dash, html,Input,Output,callback, dash_table
from dash.dependencies import Input, Output, State
from dash import dcc
import dash_bootstrap_components as dbc
import dash_cytoscape as cyto
import os
import json
import sys
import webbrowser
#from PIL import Image, ImageTk


#print(os.__version__)

adir = os.getcwd()
DIRECTORY_PATH = 'E:\develop\Python\GENEALOGIE\RenderDeploy\d75'  # Substitua pelo caminho do seu diretório


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
pil_img=''

def _from_rgb(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    return "#%02x%02x%02x" % rgb

aphoto='asset\\homme.jpg'



gen.layout = html.Div([
    html.H4('GENEALOGIE',style= {
             "font-size":"18",
             "text-wrap": "wrap",
             'text-align':'center',
             'line-height': '1',
             "text-max-width": 40
                }),
    html.H4('Cliquer sur la Personne pour voir les Détails',style= {
             "font-size":"6",
             "text-wrap": "wrap",
             'text-align':'center',
             'line-height': '1',
             "text-max-width": 40
                }),
    #html.H1("Explorador de Arquivos"),



    cyto.Cytoscape(
        id='cytoscape-event-callbacks-1',
        layout={'name': 'preset'},
        style={'width': '100%', 'height': '400px'},
        stylesheet=my_stylesheet,
        elements=aNodes),


        html.Div([
        dcc.Store(id='current-node-data'),
        html.H4(''),
        html.Img(id='imagem-dinamica',src=aphoto,style={
             'position' :'absolute',
             'top' : '10px',
             'left':'250px'

                        }),

        # Componente para exibir os dados do nó clicado
        html.Div(id='cytoscape-tapNodeData-json')

    ])

])
# Callback to update the stored node data
@gen.callback(
    Output('current-node-data', 'data'),
    [Input('cytoscape-event-callbacks-1', 'tapNodeData')]
)


def update_stored_node_data(data):
    return data


# Callback to update image
@gen.callback(
    Output('imagem-dinamica', 'src'),
    [Input('current-node-data', 'data')]
)
def update_image(data):
    if data is None:
        return Image.open('asset\\homme.gif')
    # Criar um dicionário com os detalhes do nó de forma legível
    #node_details={data['nom'],data['prenoms']}
    a = data['nom']+','+data['prenoms']+"\n"+'Né le : '+data['naissance']+' à '+data['villenaiss']+ ' '+data['paysnaiss']+'\n'
    if not data['baptise']=='':
       a =a + 'Baptisé le  '+data['baptise'] +'\n'
    if data['sexe']=='F':
        if not data['nomjeunefille']=='':
            a = a+data['nomjeunefille']+'\n'
    a= a+ 'Marié le : '+data['marie']+'\n'
    a= a+'Profession '+data['profession']+'\n'
    if not data['deces']=='':
       a =a + 'Décédé le  '+data['deces'] + ' à '+data['lieudeces']+'\n'
    if not data['inhume']=='':
       a =a + 'Inhumé le  '+data['inhume']
    if os.path.exists('asset\\'+str(data['personneid'])+'.jpg'):
        aphoto='asset\\'+str(data['personneid'])+'.jpg'
    else:
        aphoto='asset\\homme.jpg'
    #files=get_files_info(DIRECTORY_PATH)
    return Image.open(aphoto)


# Callback to display node details
@gen.callback(
    Output('cytoscape-tapNodeData-json', 'children'),
    [Input('current-node-data', 'data')]
)


def display_tap_node_data(data):

    if data is None:
        return ''

    # Criar um dicionário com os detalhes do nó de forma legível
    #node_details={data['nom'],data['prenoms']}
    a = data['nom']+','+data['prenoms']+"\n"+'Né le : '+data['naissance']+'\n'
    a=a+'à '+data['villenaiss']+ ' '+data['paysnaiss']+'\n'
    if not data['baptise']=='':
       a =a + 'Baptisé le  '+data['baptise'] +'\n'
    if data['sexe']=='F':
        if not data['nomjeunefille']=='':
            a = a+data['nomjeunefille']+'\n'
    a= a+ 'Marié le : '+data['marie']+'\n'
    a= a+'Profession '+data['profession']+'\n'
    if not data['deces']=='':
       a =a + 'Décédé le  '+data['deces'] +'\n'
    a=a+'à '+data['lieudeces']+'\n'
    if not data['inhume']=='':
       a =a + 'Inhumé le  '+data['inhume']

    #aphoto='asset\\'+str(data['personneid'])+'.jpg'
    DIRECTORY_PATH='D75'
    #data=get_files_info(DIRECTORY_PATH),
    return html.Pre(
        a,
        style= {
            'position' :'absolute',
            'border':'1px solid',
            'top' : '10px',
            'background-color':'#F57F17',
            'line-color': 'yellow',
            "font-size":"6",
            'line-height': '1',
            "text-max-width": 40
            }

    )

############################################################

###########################################################


if __name__ == '__main__':
    webbrowser.open_new(url='http://127.0.0.1:8050')
    gen.run(debug=False)
