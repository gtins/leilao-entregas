import dash
from dash import dcc, html
import plotly.graph_objects as go
import time
from dash import Input, Output

def ler_conexoes(arquivo):
    conexoes = {}
    with open(arquivo, 'r') as f:
        for linha in f:
            origem, destino, tempo = linha.strip().split(',')
            if origem not in conexoes:
                conexoes[origem] = {}
            conexoes[origem][destino] = int(tempo)
            if destino not in conexoes:
                conexoes[destino] = {}
            conexoes[destino][origem] = int(tempo)
    return conexoes

def ler_entregas(arquivo):
    entregas = []
    with open(arquivo, 'r') as f:
        for linha in f:
            horario, destino, bonus = linha.strip().split(',')
            entregas.append((int(horario), destino, int(bonus)))
    return entregas

def leilao_basico(conexoes, entregas):
    lucro_total = 0
    sequencia_entregas = []
    tempo_atual = 0
    posicao_atual = 'A'

    for entrega in entregas:
        horario, destino, bonus = entrega
        if destino in conexoes[posicao_atual]:
            tempo_viagem = conexoes[posicao_atual][destino]
            if tempo_atual + tempo_viagem <= horario:
                lucro_total += bonus
                sequencia_entregas.append((horario, destino, bonus))
                tempo_atual += tempo_viagem * 2
                posicao_atual = 'A'

    return sequencia_entregas, lucro_total

def leilao_otimizado(conexoes, entregas):
    n = len(entregas)
    dp = [0] * (n + 1)

    for i in range(1, n + 1):
        horario, destino, bonus = entregas[i - 1]
        if destino in conexoes['A']:
            dp[i] = max(dp[i - 1], dp[i - 1] + bonus)
        else:
            dp[i] = dp[i - 1]

    sequencia_entregas = []
    lucro_total = dp[n]
    for i in range(n, 0, -1):
        if dp[i] != dp[i - 1]:
            sequencia_entregas.append(entregas[i - 1])

    sequencia_entregas.reverse()
    return sequencia_entregas, lucro_total

app = dash.Dash(__name__)

conexoes = ler_conexoes('conexoes.txt')
entregas = ler_entregas('entregas.txt')

inicio_basico = time.perf_counter()
sequencia_basico, lucro_basico = leilao_basico(conexoes, entregas)
tempo_basico = (time.perf_counter() - inicio_basico) * 1000

inicio_otimizado = time.perf_counter()
sequencia_otimizada, lucro_otimizado = leilao_otimizado(conexoes, entregas)
tempo_otimizado = (time.perf_counter() - inicio_otimizado) * 1000

fig = go.Figure()
fig.add_trace(go.Bar(x=['Básico', 'Otimizado'], y=[tempo_basico, tempo_otimizado], name='Tempo de Execução'))
fig.add_trace(go.Bar(x=['Básico', 'Otimizado'], y=[lucro_basico, lucro_otimizado], name='Lucro Obtido'))

app.layout = html.Div([
    html.H1("Comparação de Algoritmos de Leilão"),
    html.Div([
        html.H3("Sequência de Entregas (Básico):"),
        html.P(str(sequencia_basico)),
        html.H3(f"Lucro Obtido (Básico): {lucro_basico}"),
    ]),
    html.Div([
        html.H3("Sequência de Entregas (Otimizado):"),
        html.P(str(sequencia_otimizada)),
        html.H3(f"Lucro Obtido (Otimizado): {lucro_otimizado}"),
    ]),
    dcc.Graph(figure=fig),
    html.Div([
        html.H4("Comparação de Desempenho"),
        html.P(f"Tempo de execução (Básico): {tempo_basico:.6f} ms"),
        html.P(f"Tempo de execução (Otimizado): {tempo_otimizado:.6f} ms"),
        html.P(f"Lucro (Básico): {lucro_basico}"),
        html.P(f"Lucro (Otimizado): {lucro_otimizado}")
    ])
])

app.layout = html.Div([
    html.H1("Comparação de Algoritmos de Leilão"),
    html.Div([
        html.Label("Alterar Tempo de Viagem (de A a B):"),
        dcc.Input(id='input-tempo-viagem', type='number', value=10, debounce=True),
        html.Button('Atualizar Conexões', id='btn-atualizar-conexoes'),
    ]),
    html.Div([
        html.Label("Alterar Entrega (Horário, Destino, Bônus):"),
        dcc.Input(id='input-horario', type='number', value=5, debounce=True),
        dcc.Input(id='input-destino', type='text', value='B', debounce=True),
        dcc.Input(id='input-bonus', type='number', value=10, debounce=True),
        html.Button('Atualizar Entregas', id='btn-atualizar-entregas'),
    ]),
    html.Div([
        html.H3("Sequência de Entregas (Básico):"),
        html.P(id='sequencia-basico'),
        html.H3(id='lucro-basico'),
    ]),
    html.Div([
        html.H3("Sequência de Entregas (Otimizado):"),
        html.P(id='sequencia-otimizada'),
        html.H3(id='lucro-otimizado'),
    ]),
    dcc.Graph(id='grafico-comparacao')
])

@app.callback(
    Output('sequencia-basico', 'children'),
    Output('lucro-basico', 'children'),
    Output('sequencia-otimizada', 'children'),
    Output('lucro-otimizado', 'children'),
    Output('grafico-comparacao', 'figure'),
    [Input('input-tempo-viagem', 'value'),
     Input('btn-atualizar-conexoes', 'n_clicks'),
     Input('input-horario', 'value'),
     Input('input-destino', 'value'),
     Input('input-bonus', 'value'),
     Input('btn-atualizar-entregas', 'n_clicks')]
)
def atualizar_parametros(input_tempo_viagem, btn_conexoes, input_horario, input_destino, input_bonus, btn_entregas):
    conexoes = ler_conexoes('conexoes.txt')
    if btn_conexoes:
        conexoes['A']['B'] = input_tempo_viagem
        conexoes['B']['A'] = input_tempo_viagem
    
    entregas = ler_entregas('entregas.txt')
    if btn_entregas:
        entregas.append((input_horario, input_destino, input_bonus))
    
    sequencia_basico, lucro_basico = leilao_basico(conexoes, entregas)
    sequencia_otimizada, lucro_otimizado = leilao_otimizado(conexoes, entregas)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=['Básico', 'Otimizado'], y=[lucro_basico, lucro_otimizado], name='Lucro Obtido'))
    
    return (str(sequencia_basico), lucro_basico, str(sequencia_otimizada), lucro_otimizado, fig)

if __name__ == '__main__':
    app.run(debug=True)
