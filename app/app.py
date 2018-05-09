import datetime

import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

from flask import send_from_directory
import os

from PIL import Image, ImageDraw

# --------------------- app option ---------------------

app = dash.Dash()
app.title='Your Palette'
app.scripts.config.serve_locally = True

# --------------------- app layout ---------------------

app.layout = html.Div([
    html.Link(
        rel='stylesheet',
        href='/static/st0.css'
    ),
    html.Div([
        html.Div([
            html.Div(["Your Palette"], id="header")
        ],id="header-bk")
    ],id="header-fixed"),

    html.H1(['Make your own palette'],
    style={'font-size': '6vw', 'margin-left': '11%', 'margin-bottom': '7%', 'margin-top': '150px'}),

    html.Div([
        dcc.Upload(
            id='upload-image',
            children=html.Div([
                'Drag  and  Drop  or  ',
                html.A('Select  Files')
            ]),
            style={
                'font-size': '3.4vw',
                'width': '100%',
                'height': '80px',
                'lineHeight': '60px',
                'borderWidth': '3px',
                'borderStyle': 'dashed',
                'borderRadius': '7px',
                'border-color': 'grey',
                'textAlign': 'center',
                'margin': '20px',
                'padding-top': '20px'
            },
            # Allow multiple files to be uploaded
            multiple=True
        ),
        html.Div(id='output-image-upload'),
    ],
    style={'width': '80%', 'position': 'auto', 'margin': 'auto'}),
],
id='wrapper',
style={'position': 'relative', 'width': '100%', 'font-family': 'Dosis'})


def parse_contents(contents, filename, date):

    return html.Div([
        html.H5([filename], style={'margin-top': '8%'}),
        html.H5(datetime.datetime.fromtimestamp(date)),

        # HTML images accept base64 encoded strings in the same format
        # that is supplied by the upload
        html.Img(src=contents),
        html.Hr(),
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        }),
        html.Hr(),
    ])

def get_colors(infile, numcolors=10, swatchsize=20, resize=150):

    image = Image.open("DASH.png")
    image = image.resize((resize, resize))
    result = image.convert('P', palette=Image.ADAPTIVE, colors=numcolors)
    result.putalpha(0)
    colors = result.getcolors(resize*resize)

    # Save colors to file
    pal = Image.new('RGB', (swatchsize*numcolors, swatchsize))

    return pal

# def head():
#     path = request.path
#     return html.Title(path)
#
# app.head = head


@app.callback(Output('output-image-upload', 'children'),
              [Input('upload-image', 'contents'),
               Input('upload-image', 'filename'),
               Input('upload-image', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children



@app.server.route('/static/<path>')
def static_file(path):
    static_folder = os.path.join(os.getcwd(), 'static')
    return send_from_directory(static_folder, path)

external_css = [
    # dash stylesheet
    'https://fonts.googleapis.com/css?family=Raleway',
    'https://codepen.io/chriddyp/pen/bWLwgP.css'
]
for css in external_css:
    app.css.append_css({'external_url': css})


if __name__ == '__main__':
    app.run_server(debug=True, port=5000, host='0.0.0.0')
