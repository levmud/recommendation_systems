import base64
import io
import dash
from dash import dash_table
import pandas as pd
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import algorithms

app = dash.Dash(__name__)

courses_np = None
users_np = None
ratings_np = None

# Определение макета страницы загрузки файлов
upload_layout = html.Div([
    # html.H1("Загрузка CSV файлов", style={'text-align': 'center'}),
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

# Определение макета страницы "О приложении"
about_layout = html.Div([
    # html.H1("О приложении", style={'text-align': 'center'}),
    html.P("Это веб-приложение для загрузки и отображения CSV файлов."),
    html.P("Вы можете загрузить файлы курсов, пользователей и рейтингов, и они будут отображены в виде таблиц на странице 'Отображение CSV файлов'."),
    html.P("Автор: Иван Иванов")
])

algo1_layout = html.Div([
    # html.H1("О приложении", style={'text-align': 'center'}),
    html.P("Демонстрация алгоритма 'User-based Collaborative filtering'"),
    html.Div(id='output-ratings1'),
    html.Div(id='output-predicted-ratings_1')
])

algo2_layout = html.Div([
    html.P("Демонстрация алгоритма 'Item-based Collaborative filtering'"),
    html.Div(id='output-ratings2'),
    html.Div(id='output-predicted-ratings_2')

])

# Определение макета приложения
app.layout = html.Div([
    dcc.Tabs(id='tabs', value='upload', children=[
        dcc.Tab(label='Загрузка файлов', value='upload', children=[upload_layout]),
        dcc.Tab(label='Алгоритм 1', value='alg1', children=[algo1_layout]),
        dcc.Tab(label='Алгоритм 2', value='alg2', children=[algo2_layout]),
        dcc.Tab(label='О приложении', value='about', children=[about_layout])
    ]),
    html.Div(id='page-content')
])


# Функции обработки загрузки файлов и сохранения их в переменные
def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Загрузить содержимое файла в DataFrame
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), sep=';')
            # Преобразовать DataFrame в numpy массив
            np_array = df.to_numpy()

            # Сохранить массив в соответствующую переменную
            if 'courses' in filename:
                global courses_np
                courses_np = np_array
            elif 'users' in filename:
                global users_np
                users_np = np_array
            elif 'rat' in filename:
                global ratings_np
                ratings_np = np_array

            print('courses=', courses_np)
            print('users=', users_np)
            print('ratings=', ratings_np)



            # Отобразить DataFrame в виде таблицы
            return html.Div([
                html.H5(filename),
                dash_table.DataTable(
                    data=df.to_dict('records'),
                    columns=[{'name': i, 'id': i} for i in df.columns],
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


# Функция обработки загрузки файла рейтингов и расчета предсказанных рейтингов
@app.callback(Output('output-predicted-ratings_1', 'children'),
              Input('upload-ratings', 'contents'),
              State('upload-ratings', 'filename'))
def update_output_predicted_ratings(content, filename):
    if ratings_np is not None:
        predicted_ratings = algorithms.user.predict_ratings(ratings_np, 3)
        table = []
        for i, user in enumerate(predicted_ratings):
            table.append(f'Predicted ratings for User{i + 1}: {user}')
        print('Вызов предикта')
        # Отобразить предсказанные рейтинги в виде таблицы
        return html.Div([
            html.H5('Предсказанные рейтинги'),
            html.Div([
                html.P(s) for s in table])
        ])
    else:
        return None

@app.callback(Output('output-predicted-ratings_2', 'children'),
              Input('upload-ratings', 'contents'),
              State('upload-ratings', 'filename'))
def update_output_predicted_ratings(content, filename):
    if ratings_np is not None:
        predicted_ratings = algorithms.item.predict_ratings_item(ratings_np, 3)
        table = []
        for i, user in enumerate(predicted_ratings):
            table.append(f'Predicted ratings for User{i + 1}: {user}')
        print('Вызов предикта')
        # Отобразить предсказанные рейтинги в виде таблицы
        return html.Div([
            html.H5('Предсказанные рейтинги'),
            html.Div([
                html.P(s) for s in table])
        ])
    else:
        return None


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

@app.callback(Output('output-ratings1', 'children'),
              Input('upload-ratings', 'contents'),
              State('upload-ratings', 'filename'))
def update_output_ratings2(content, filename):
    if content is not None:
        return parse_contents(content, filename)
    else:
        return None

@app.callback(Output('output-ratings2', 'children'),
              Input('upload-ratings', 'contents'),
              State('upload-ratings', 'filename'))
def update_output_ratings2(content, filename):
    if content is not None:
        return parse_contents(content, filename)
    else:
        return None


if __name__ == '__main__':
    app.run_server(debug=True)
