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
