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