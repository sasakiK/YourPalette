import datetime

import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

from PIL import Image, ImageDraw

# from flask import send_from_directory
# import os

app = dash.Dash()

app.scripts.config.serve_locally = True


app.layout = html.Div([
    # html.Link(
    #         rel='stylesheet',
    #         href='static/stylesheet.css'
    # ),

    html.H1(['Make your own palette'],
    style={'font-size': '6vw', 'margin-left': '11%', 'margin-bottom': '7%', 'margin-top': '10%'}),

    html.P(['Using this application, you can get color palette from your favorite (jpg/png) file.'],
    style={'font-size': '2.7vw',
           'margin-left': '11%',
           'margin-bottom': '7%',
           'margin-top': '5%',
           'width' : '65%'}),


    html.Div([
        dcc.Upload(
            id='upload-image',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
            style={
                'font-size': '3.4vw',
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '3px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'border-color': 'grey',
                'textAlign': 'center',
                'margin': '10px'
            },
            # Allow multiple files to be uploaded
            multiple=True
        ),
        html.Div(id='output-image-upload'),
    ],
    style={'width': '80%', 'position': 'auto', 'margin': 'auto'}),
],
style={'position': 'relative', 'width': '100%', 'font-family': 'Dosis'})


def parse_contents(contents, filename, date):

    # infile = [filename]
    # numcolors=10
    # swatchsize=20
    # resize=150
    #
    # image = Image.open(infile)
    # image = image.resize((resize, resize))
    # result = image.convert('P', palette=Image.ADAPTIVE, colors=numcolors)
    # result.putalpha(0)
    # colors = result.getcolors(resize*resize)
    #
    # # Save colors to file
    #
    # pal = Image.new('RGB', (swatchsize*numcolors, swatchsize))
    #
    # draw = ImageDraw.Draw(pal)
    #
    # posx = 0
    # for count, col in colors:
    #     draw.rectangle([posx, 0, posx+swatchsize, swatchsize], fill=col)
    #     posx = posx + swatchsize
    #
    # del draw
    # pal.save("output.png", "PNG")
    #
    # return pal

    return html.Div([
        html.H5([filename], style={'margin-top': '8%'}),
        html.H6(datetime.datetime.fromtimestamp(date)),

        # HTML images accept base64 encoded strings in the same format
        # that is supplied by the upload
        html.Img(src=contents),
        html.Hr(),
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        }),
        html.Img(src="output.png"),
        html.Hr(),
    ])


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


external_css = [
    # dash stylesheet
    'https://fonts.googleapis.com/css?family=Raleway',
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    'https://github.com/sasakiK/YourPalette/blob/master/app/static/stylesheet.css'
]
for css in external_css:
    app.css.append_css({'external_url': css})

# @app.server.route('/static/<path>')
# def static_file(path):
#     static_folder = os.path.join(os.getcwd(), 'static')
#     return send_from_directory(static_folder, path)


if __name__ == '__main__':
    app.run_server(debug=True, port=5000, host='0.0.0.0')
