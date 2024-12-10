#-------------------------------------------------------------------------------
# Name:        module2
# Purpose:
#
# Author:      ylalo
#
# Created:     10-12-2024
# Copyright:   (c) ylalo 2024
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from dash import Dash, html,Input,Output,callback
from dash import dcc
import dash_cytoscape as cyto
import os
import json
import sys
import webbrowser
import unicorn


app = Dash(__name__)
app= app.server

if __name__ == '__main__':
   print('Hello world')
   app.rundebug=True
