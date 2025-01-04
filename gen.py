#-------------------------------------------------------------------------------
# Name:        GEN
# Purpose:     ARVORE GENEALOGICA COM DASH - FUNCIONANDO
#              Usadso dashboard.render4.com para expor na WB
#              Vide video YOUTUBE : https://www.youtube.com/watch?v=H16dZMYmvqo
#
# Author:      ylalo
# Version      1.2
#
# Created:     27-11-2024
# Copyright:   (c) ylalo 2024
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import subprocess
import dash_core_components as dcc
from dash import Dash, html, Input, Output, callback, dash_table
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash_cytoscape as cyto
import os
import json
import webbrowser
import base64
import platform

adir = os.getcwd()
afile = adir + '\\js.txt'
aNodes = []
with open(afile, "r") as meu_json:
    aNodes = json.load(meu_json)

gen = Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}])
server = gen.server

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    },
    'cab': {
        "font-size": "6",
        'line-height': '2'

    }

}

my_stylesheet = [
    {
        'selector': 'node',
        'style': {
            'content': 'data(label)'
        }
    },
    {
        'selector': '.pink',
        'style': {
            'background-color': 'pink',
            'line-color': 'pink',
            "font-size": "6",
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
            "font-size": "6",
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
            "font-size": "6",
            "text-wrap": "wrap",
            "text-max-width": 40
        }
    }
]

def _from_rgb(rgb):
    return "#%02x%02x%02x" % rgb

aphoto = 'photos/homme.jpg'

def bimage(image_filename):
    with open(image_filename, 'rb') as f:
        image = f.read()
    return 'data:image/png;base64,' + base64.b64encode(image).decode('utf-8')

gen.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
           html.Img(id='imagem-dinamica', src=bimage(aphoto), style={
            'position': 'absolute',
            'top': '30px',
            'left': '10px'})
        ])
    ]),
    dbc.Row([
        dbc.Col(html.H1("GÉNÉALOGIE",
                        className='text-center fs-1'),width=12)
    ]),

    dbc.Row([
        dbc.Col(html.H1("(Zoom :Rouler la souris)",
                        className='text-center fs-6'),  # fs-6 = font size : maior o numero, menor a font
                width=12)
    ]),
    dbc.Row(
        dbc.Col(html.H1("Cliquer sur la Personne pour voir les Détails",
                        className='text-center fs-6'),
                width=12)
    ),
    dbc.Row([html.H1()]),
    dbc.Row([html.H1()]),
    dbc.Row([html.H1()]),
    dbc.Row([html.H1()]),

     dbc.Row([
        dbc.Col(html.Button('Ouvrir', id='submit-func', n_clicks=0),md=1),
        dbc.Col([dcc.Dropdown(id='my-dpdn', multi=False, placeholder='Choisir un Document',
                         className='text-center text-primary'),
        html.Div(id='dd-output-container'),
        dcc.Store(id='current-node-data')],md=4)]),



    dbc.Row([
        dbc.Col([ html.Label('Rechercher un Nom', id='lab-rech', n_clicks=0)],width=1),
        dbc.Col([ html.Div(dcc.Input(id='input-on-rech', type='text'))]),

    dbc.Row([
        dbc.Col([cyto.Cytoscape(
        id='cytoscape-event-callbacks-1',
        minZoom=0.5,
        maxZoom=6,
        zoom=6,
        pan={'x': 200, 'y': 200},


        zoomingEnabled=True,

        layout={'name': 'preset'},
        style={'width': '100%', 'height': '800px'},
        stylesheet=my_stylesheet,
        elements=aNodes),# Componente para exibir os dados do nó clicado
        html.Div(id='cytoscape-tapNodeData-json')],width=12),
        dbc.Col([html.Div(id='container-button-func', children='resultat')]
        ),
    ])
    ])
],fluid= True)


############# CALLBACK SEARCH

@callback(
    Output('cytoscape-event-callbacks-1', 'stylesheet'),
    Input('input-on-rech', 'value'),
    State('cytoscape-event-callbacks-1', 'stylesheet')
)
def update_search(search_text, stylesheet):
    if not search_text:
        return my_stylesheet

    stylesheet = list(my_stylesheet)
    stylesheet.append({
        'selector': f'node[label *= "{search_text}"]',
        'style': {
            'background-color': 'yellow',
        }
    })
    return stylesheet

######################## CALLBACK DROPDOWN
@callback(
    Output('my-dpdn', 'options'),
    Output('my-dpdn', 'value'),
    Input('current-node-data', 'data')
)
def update_dropdown(data):
    if data is None:
        return [], None

    person_dir = os.path.join(adir, str(data['personneid']))
    if not os.path.exists(person_dir):
        return [], None

    files = os.listdir(person_dir)
    options = [{'label': f, 'value': os.path.join(person_dir, f)} for f in files]
    return options, None


###################  CALLBACK ABRE ARQUIVO DROPDOWN
@callback(
    Output('container-button-func', 'children'),
    Input('submit-func', 'n_clicks'),
    State('my-dpdn', 'value'),
    prevent_initial_call=True
)
def execute_file(n_clicks, file_path):
    if not file_path:
        return ''

    system = platform.system()
    if system == "Windows":
        os.startfile(file_path)
    elif system == "Darwin":
        subprocess.run(['open', file_path])
    else:
        subprocess.run(['xdg-open', file_path])
    return ''

#######################  CALLBACK PHOTO
@callback(
    Output('current-node-data', 'data'),
    [Input('cytoscape-event-callbacks-1', 'tapNodeData')]
)
def update_stored_node_data(data):
    return data
@callback(
    Output('imagem-dinamica', 'src'),
    [Input('current-node-data', 'data')]
)

def update_image(data):
    if data is None:
        return bimage('photos/homme.jpg')

    photo_path = f"photos/{data['personneid']}.jpg"
    if os.path.exists(photo_path):
        return bimage(photo_path)
    return bimage('photos/homme.jpg')


######################## CALLBACK INFO PESSOA
@callback(
    Output('cytoscape-tapNodeData-json', 'children'),
    [Input('current-node-data', 'data')]
)
def display_tap_node_data(data):
    if data is None:
        return ''

    details = [
        f"{data['nom']},{data['prenoms']}",
        f"Né le : {data['naissance']}",
        f"à {data['villenaiss']} {data['paysnaiss']}"
    ]

    if data['baptise']:
        details.append(f"Baptisé le {data['baptise']}")

    if data['sexe'] == 'F' and data['nomjeunefille']:
        details.append(data['nomjeunefille'])

    details.extend([
        f"Marié le : {data['marie']}",
        f"Profession {data['profession']}"
    ])

    if data['deces']:
        details.append(f"Décédé le {data['deces']}")

    details.append(f"à {data['lieudeces']}")

    if data['inhume']:
        details.append(f"Inhumé le {data['inhume']}")

    return html.Pre(
        '\n'.join(details),
        style={
            'position': 'absolute',
            'border': '1px solid',
            'top': '25px',
            'left': '100px',
            'background-color': '#F57F17',
            'line-color': 'yellow',
            "font-size": "6",
            'line-height': '1',
            "text-max-width": 40
        }
    )

if __name__ == '__main__':
    webbrowser.open_new(url='http://127.0.0.1:8050')
    gen.run(debug=False)