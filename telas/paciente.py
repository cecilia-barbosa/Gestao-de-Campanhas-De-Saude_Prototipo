import psycopg2
import pandas as pd
import panel as pn
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError
from datetime import date

pn.extension()

# conexao com o banco
engine = create_engine(
    "postgresql+psycopg2://postgres:0808@localhost:5432/trabalho_FBD"
)

#funcao listar
def listar_pacientes():
    with engine.connect() as conn:
        resultado = conn.execute(text("SELECT * FROM Paciente ORDER BY cns"))
        colunas = list(resultado.keys())
        dados = resultado.fetchall()
    df = pd.DataFrame(dados, columns=colunas)
    if not df.empty:
        df['data_de_nascimento'] = pd.to_datetime(df['data_de_nascimento']).dt.date
    return df
