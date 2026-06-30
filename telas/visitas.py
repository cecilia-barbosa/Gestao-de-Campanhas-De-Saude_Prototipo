import psycopg2
import pandas as pd
import panel as pn
from sqlalchemy import create_engine, text
from datetime import date

pn.extension()

# conexão com o banco
engine = create_engine("postgresql+psycopg2://postgres:1203@localhost:5432/trabalho_FBD")

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="trabalho_FBD",
    user="postgres",
    password="1203"
)

# função para listar todas as visitas
def listar_visitas():
    with engine.connect() as c:
        resultado = c.execute(text("SELECT * FROM Visita ORDER BY id_visita"))
        colunas = list(resultado.keys())
        dados = resultado.fetchall()
    df = pd.DataFrame(dados, columns=colunas)
    df['horario'] = df['horario'].apply(lambda x: str(x)[:5])
    df['data'] = pd.to_datetime(df['data']).dt.date
    return df

# função para adicionar uma visita
def inserir_visita(horario, data, sincronizacao, id_agente, cns_paciente):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Visita (horario, data, sincronizacao_do_agente, id_agente, cns_paciente) VALUES (%s, %s, %s, %s, %s)",
        (horario, data, sincronizacao, id_agente, cns_paciente)
    )
    conn.commit()
    cursor.close()

# função para editar uma visita
def editar_visita(id_visita, horario, data, sincronizacao, id_agente, cns_paciente):
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE Visita SET horario = %s, data = %s, sincronizacao_do_agente = %s, id_agente = %s, cns_paciente = %s WHERE id_visita = %s",
        (horario, data, sincronizacao, id_agente, cns_paciente, id_visita)
    )
    conn.commit()
    cursor.close()

# função para remover uma visita
def excluir_visita(id_visita):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Visita WHERE id_visita = %s", (id_visita,))
    conn.commit()
    cursor.close()

# tabela de visitas
visitas_table = pn.widgets.Tabulator(
    value=pd.DataFrame(),
    pagination='remote',
    page_size=10,
    show_index=False,
    height=300,
    sizing_mode='stretch_width',
    visible=False,
)
# campos do formulario
id_inputc= pn.widgets.IntInput(name='ID da Visita (para Editar/Remover)', width=260)
horario_input = pn.widgets.TextInput(name='Horário (HH:MM)', placeholder='09:00', width=260)
data_input = pn.widgets.DatePicker(name='Data', value=date.today(), width=260)
sync_input = pn.widgets.Select(name='Sincronização do Agente', options={'Sim': True, 'Não': False}, width=260)
agente_input = pn.widgets.IntInput(name='ID do Agente', value=21, width=260)
cns_input = pn.widgets.TextInput(name='CNS do Paciente', placeholder='CNS001', width=260)

# botoes
btn_adicionar = pn.widgets.Button(name='Adicionar', button_type='default', width=130)
btn_editar    = pn.widgets.Button(name='Editar', button_type='default', width=130)
btn_remover   = pn.widgets.Button(name='Remover', button_type='default', width=130)
btn_listar    = pn.widgets.Button(name='Listar', button_type='default', width=130)
 
status_msg   = pn.pane.Markdown('', styles={'font-weight': 'bold'})
titulo_lista = pn.pane.Markdown('### Lista de Visitas', visible=False)

# limpa os campos do formulario
def limpar_formulario():
    id_input.value      = None
    horario_input.value = ''
    data_input.value    = date.today()
    sync_input.value    = True
    agente_input.value  = 21
    cns_input.value     = ''
 
def on_adicionar(event):
    if horario_input.value == '' or data_input.value == None or cns_input.value == '':
        status_msg.object = 'Preencha todos os campos obrigatórios.'
        return
    try:
        inserir_visita(horario_input.value, data_input.value, sync_input.value, agente_input.value, cns_input.value)
        status_msg.object = 'Visita adicionada com sucesso!'
        limpar_formulario()
        visitas_table.value = listar_visitas()
    except Exception as e:
        status_msg.object = f'Erro ao adicionar: {e}'
        conn.rollback()
 
def on_editar(event):
    if id_input.value == None:
        status_msg.object = 'Informe o ID da visita para editar.'
        return
    try:
        editar_visita(id_input.value, horario_input.value, data_input.value, sync_input.value, agente_input.value, cns_input.value)
        status_msg.object = 'Visita atualizada com sucesso.'
        limpar_formulario()
        visitas_table.value = listar_visitas()
    except Exception as e:
        status_msg.object = f'Erro ao editar: {e}'
        conn.rollback()

def on_listar(event):
    if visitas_table.visible == True:
        visitas_table.visible = False
        titulo_lista.visible  = False
        status_msg.object = 'Tabela oculta.'
        return
    visitas_table.value = listar_visitas()
    visitas_table.visible = True
    titulo_lista.visible  = True
    status_msg.object = 'Tabela exibida.'
 
btn_adicionar.on_click(on_adicionar)
btn_editar.on_click(on_editar)
btn_remover.on_click(on_remover)
btn_listar.on_click(on_listar)