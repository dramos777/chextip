from models import db, Branch, Condominium
from utils import update_asset_status, get_asset_uptime, get_system_uptime
from dash import dcc, html, Input, Output, State
import plotly.express as px
import dash_daq as daq
import pandas as pd
import dash

def monitoring(app):
    dash_app = dash.Dash(__name__, server=app, url_base_pathname='/monitoring/')

    dash_app.layout = html.Div([
        html.H1("Dashboard de Ativos", style={"textAlign": "center"}),

        dcc.Store(id='visibility-store', data={}),  # Armazena visibilidade de cada ativo

        html.Div([
            dcc.Input(id='search-box', type='text', placeholder='Buscar ativo...', style={'width': '50%', 'marginBottom': '20px'}),

            dcc.Dropdown(
                id='status-filter',
                options=[
                    {'label': 'Todos', 'value': None},
                    {'label': 'Online', 'value': 'online'},
                    {'label': 'Offline', 'value': 'offline'}
                ],
                value=None,
                placeholder="Exibição",
                style={'width': '25%', 'marginBottom': '10px', 'display': 'inline-block'}
            ),
        ], style={"textAlign": "right"}),

        html.Div([
            dcc.Graph(id='asset-status-pie', style={"marginTop": "20px"}),
        ], style={'width': '45%', 'display': 'inline-block', 'verticalAlign': 'top'}),

        html.Div([
            html.H3("Tabela de Ativos", style={"textAlign": "center"}),
            html.Div(id="asset-table", style={"marginTop": "30px"}),
        ], style={'width': '45%', 'display': 'inline-block', 'marginLeft': '10px'}),

        html.Div([
            html.H4(f"Uptime do Sistema: {get_system_uptime()}", style={"textAlign": "center", "marginTop": "20px"}),
        ]),

        # Intervalo de atualização automática
        dcc.Interval(
            id="interval-component",
            interval=60 * 1000,  # Atualiza a cada 60 segundos (em milissegundos)
            n_intervals=0
        ),
    ])

    @dash_app.callback(
        [
            Output('asset-status-pie', 'figure'),
            Output('asset-table', 'children'),
            Output('visibility-store', 'data')
        ],
        [
            Input('search-box', 'value'),
            Input('status-filter', 'value'),
            Input('interval-component', 'n_intervals'),  # Adicionado para atualização periódica
            Input({'type': 'toggle-visibility', 'index': dash.ALL}, 'n_clicks')  # Escuta todos os botões de visibilidade
        ],
        State('visibility-store', 'data')
    )
    def update_dashboard(search_value, status_filter, n_intervals, toggle_clicks, visibility_store):
        visibility_store = visibility_store or {}  # Inicializa o estado de visibilidade
        ctx = dash.callback_context
        if ctx.triggered:
            # Identifica qual botão foi clicado
            triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
            if triggered_id.startswith("{"):  # Se for um botão dinâmico
                triggered_id = eval(triggered_id)  # Converte de string para dict
                asset_id = triggered_id['index']
                visibility_store[asset_id] = not visibility_store.get(asset_id, True)

        with app.app_context():
            # Atualiza status dos ativos
            # update_asset_status()  # Descomente se precisar atualizar status
            assets_query = Branch.query.join(Condominium).add_columns(
                Branch.location, Branch.branch_number, Branch.ip_address, Branch.status,
                Branch.visible, Branch.id, Condominium.name.label("condominium_name")
            )

            if search_value:
                assets_query = assets_query.filter(Branch.location.ilike(f'%{search_value}%'))
            if status_filter:
                assets_query = assets_query.filter(Branch.status == status_filter)
            assets = assets_query.all()

        data = pd.DataFrame([{
            "Condominium": a.condominium_name,
            "Name": a.location,
            "IP": a.ip_address,
            "Status": a.status,
            "Uptime": get_asset_uptime(a.ip_address),
            "Visible": a.visible,
            "Branch_Number": a.branch_number,
            "ID": a.id,
        } for a in assets])

        pie_fig = px.pie(
            data, names='Status', title="Distribuição dos Ativos por Status",
            color='Status', color_discrete_map={'online': 'green', 'offline': 'red'}
        )

        table_header = html.Tr([html.Th("Condominio"), html.Th("Local"), html.Th("Uptime"), html.Th("Visibilidade")])
        table_rows = [
            html.Tr(
                id=f"row-{a.id}",
                children=[
                    html.Td(
                        a.condominium_name,
                        style={"color": "black"}
                    ),
                    html.Td(
                        a.location,
                        style={"color": "green" if a.status == "online" else "red", "fontWeight": "bold"}
                    ),
                    html.Td(get_asset_uptime(a.branch_number)),
                    html.Td(html.Button(
                        "Ocultar" if visibility_store.get(a.id, True) else "Exibir",
                        id={'type': 'toggle-visibility', 'index': a.id},
                        n_clicks=0,
                        style={'color': 'white', 'background-color': 'gray'}
                    ))
                ],
                style={"display": "table-row" if visibility_store.get(a.id, True) else "none"}
            ) for a in assets
        ]

        table = html.Table([table_header] + table_rows, style={"width": "100%", "margin": "0 auto", "textAlign": "center"})
        return pie_fig, table, visibility_store

