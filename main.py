import base64
import io

import dash
from dash import dash_table
import pandas as pd
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State


app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Загрузка и отображение CSV файлов", style={'text-align': 'center'}),
    html.Div([
        dcc.Upload(
            id='upload-courses',
            children=html.Div([
                'Загрузить файл курсов'
            ]),
            style={
                'width': '400px',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px',
                'display': 'inline-block'
            },
            multiple=False
        ),
        dcc.Upload(
            id='upload-users',
            children=html.Div([
                'Загрузить файл пользователей'
            ]),
            style={
                'width': '400px',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px',
                'display': 'inline-block'
            },
            multiple=False
        ),
        dcc.Upload(
            id='upload-ratings',
            children=html.Div([
                'Загрузить файл рейтингов'
            ]),
            style={
                'width': '400px',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px',
                'display': 'inline-block'
            },
            multiple=False
        )
    ],
        style={'display': 'flex',
               'flex-direction': 'row',
               'flex-wrap': 'nowrap',
               'justify-content': 'space-around'
               }),

    html.Div(id='output-courses'),
    html.Div(id='output-users'),
    html.Div(id='output-ratings')
])

# Функции обработки загрузки файлов и сохранения их в переменные
def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Загрузить содержимое файла в DataFrame
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), sep=';')
            # Отсортировать DataFrame по столбцам
            df_sorted = df.sort_values(by=df.columns[0])

            # Отобразить DataFrame в виде таблицы
            return html.Div([
                html.H5(filename),
                dash_table.DataTable(
                    data=df_sorted.to_dict('records'),
                    columns=[{'name': i, 'id': i} for i in df_sorted.columns],
                    sort_action='native',
                    sort_mode='multi',
                    filter_action='native',
                    page_action='native',
                    page_current=0,
                    page_size=10
                )
            ])
        else:
            return html.Div([
                'Формат файла не поддерживается. Пожалуйста, выберите файл CSV.'
            ])
    except Exception as e:
        return html.Div([
            'Произошла ошибка при обработке файла.'
        ])

# Обработчики событий загрузки файлов
@app.callback(Output('output-courses', 'children'),
              Input('upload-courses', 'contents'),
              State('upload-courses', 'filename'))
def update_output_courses(content, filename):
    if content is not None:
        return parse_contents(content, filename)
    else:
        return None

@app.callback(Output('output-users', 'children'),
              Input('upload-users', 'contents'),
              State('upload-users', 'filename'))
def update_output_users(content, filename):
    if content is not None:
        return parse_contents(content, filename)
    else:
        return None

@app.callback(Output('output-ratings', 'children'),
              Input('upload-ratings', 'contents'),
              State('upload-ratings', 'filename'))
def update_output_ratings(content, filename):
    if content is not None:
        return parse_contents(content, filename)
    else:
        return None

if __name__ == '__main__':
    app.run_server(debug=True)
