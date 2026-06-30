# ============================================================
# Arquivo: telas/campanhas.py
# Tela CRUD - Tabela: Campanha
# ============================================================

import pandas as pd
import panel as pn
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError
from datetime import date

pn.extension()

# ============================================================
# CONEXÃO COM O BANCO
# ============================================================

engine = create_engine("postgresql+psycopg2://postgres:1203@localhost:5432/trabalho_FBD")
# ============================================================
# FUNÇÕES CRUD
# ============================================================

def listar_campanhas():
    with engine.connect() as conn:
        resultado = conn.execute(text("SELECT * FROM Campanha ORDER BY id_campanha"))
        colunas = list(resultado.keys())
        dados = resultado.fetchall()

    df = pd.DataFrame(dados, columns=colunas)

    if not df.empty:
        df["data_inicio"] = pd.to_datetime(df["data_inicio"]).dt.date
        df["data_fim"] = pd.to_datetime(df["data_fim"]).dt.date

    return df


def inserir_campanha(nome, objetivo, data_inicio, data_fim, id_gestor):
    with engine.connect() as conn:
        conn.execute(text("""
            INSERT INTO Campanha (nome, objetivo, data_inicio, data_fim, id_gestor)
            VALUES (:nome, :objetivo, :data_inicio, :data_fim, :id_gestor)
        """), {
            "nome": nome,
            "objetivo": objetivo,
            "data_inicio": data_inicio,
            "data_fim": data_fim,
            "id_gestor": id_gestor
        })
        conn.commit()


def editar_campanha(id_campanha, nome, objetivo, data_inicio, data_fim, id_gestor):
    with engine.connect() as conn:
        conn.execute(text("""
            UPDATE Campanha
            SET nome = :nome,
                objetivo = :objetivo,
                data_inicio = :data_inicio,
                data_fim = :data_fim,
                id_gestor = :id_gestor
            WHERE id_campanha = :id_campanha
        """), {
            "id_campanha": id_campanha,
            "nome": nome,
            "objetivo": objetivo,
            "data_inicio": data_inicio,
            "data_fim": data_fim,
            "id_gestor": id_gestor
        })
        conn.commit()


def excluir_campanha(id_campanha):
    with engine.connect() as conn:
        conn.execute(
            text("DELETE FROM Campanha WHERE id_campanha = :id_campanha"),
            {"id_campanha": id_campanha}
        )
        conn.commit()

# ============================================================
# INTERFACE GRÁFICA
# ============================================================

campanhas_table = pn.widgets.Tabulator(
    value=pd.DataFrame(),
    pagination='remote',
    page_size=10,
    show_index=False,
    height=300,
    sizing_mode='stretch_width',
    visible=False,
)

# --- Campos ---
id_input          = pn.widgets.IntInput(name='ID da Campanha (Editar/Remover)', width=260)
nome_input        = pn.widgets.TextInput(name='Nome da Campanha', placeholder='Ex: Campanha Inverno', width=260)
objetivo_input    = pn.widgets.TextInput(name='Objetivo', placeholder='Ex: Prevenção da gripe', width=260)
data_inicio_input = pn.widgets.DatePicker(name='Data de Início', value=date.today(), width=260)
data_fim_input    = pn.widgets.DatePicker(name='Data de Fim', value=date.today(), width=260)
gestor_input      = pn.widgets.IntInput(name='ID do Gestor', value=1, width=260)

# --- Botões ---
btn_adicionar = pn.widgets.Button(name='Adicionar', button_type='default', width=130)
btn_editar    = pn.widgets.Button(name='Editar', button_type='default', width=130)
btn_remover   = pn.widgets.Button(name='Remover', button_type='default', width=130)
btn_listar    = pn.widgets.Button(name='Listar', button_type='default', width=130)

status_msg   = pn.pane.Markdown('', styles={'font-weight': 'bold'})
titulo_lista = pn.pane.Markdown('### Lista de Campanhas', visible=False)

# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def atualizar_status(texto):
    status_msg.object = texto


def atualizar_tabela():
    campanhas_table.value = listar_campanhas()


def limpar_formulario():
    id_input.value = None
    nome_input.value = ''
    objetivo_input.value = ''
    data_inicio_input.value = date.today()
    data_fim_input.value = date.today()
    gestor_input.value = 1

# ============================================================
# EVENTOS DOS BOTÕES
# ============================================================

def on_adicionar(event):
    if not nome_input.value or not objetivo_input.value or not data_inicio_input.value or not data_fim_input.value:
        atualizar_status('⚠️ Preencha todos os campos obrigatórios.')
        return

    if data_fim_input.value < data_inicio_input.value:
        atualizar_status('⚠️ A data de fim não pode ser menor que a data de início.')
        return

    try:
        inserir_campanha(
            nome_input.value,
            objetivo_input.value,
            data_inicio_input.value,
            data_fim_input.value,
            gestor_input.value
        )
        atualizar_status('✅ Campanha adicionada com sucesso.')
        limpar_formulario()
        atualizar_tabela()
    except IntegrityError:
        atualizar_status('❌ Erro: o ID do gestor não existe no banco.')
    except Exception as e:
        atualizar_status(f'❌ Erro ao adicionar: {e}')


def on_editar(event):
    if id_input.value is None:
        atualizar_status('⚠️ Informe o ID da campanha para editar.')
        return

    if data_fim_input.value < data_inicio_input.value:
        atualizar_status('⚠️ A data de fim não pode ser menor que a data de início.')
        return

    try:
        editar_campanha(
            id_input.value,
            nome_input.value,
            objetivo_input.value,
            data_inicio_input.value,
            data_fim_input.value,
            gestor_input.value
        )
        atualizar_status('✅ Campanha atualizada com sucesso.')
        limpar_formulario()
        atualizar_tabela()
    except IntegrityError:
        atualizar_status('❌ Erro: o ID do gestor não existe no banco.')
    except Exception as e:
        atualizar_status(f'❌ Erro ao editar: {e}')


def on_remover(event):
    if id_input.value is None:
        atualizar_status('⚠️ Informe o ID da campanha para remover.')
        return

    try:
        excluir_campanha(id_input.value)
        atualizar_status('✅ Campanha removida com sucesso.')
        limpar_formulario()
        atualizar_tabela()
    except Exception as e:
        atualizar_status(f'❌ Erro ao remover: {e}')


def on_listar(event):
    if campanhas_table.visible:
        campanhas_table.visible = False
        titulo_lista.visible = False
        atualizar_status('Tabela oculta.')
        return

    atualizar_tabela()
    campanhas_table.visible = True
    titulo_lista.visible = True
    atualizar_status('Tabela exibida.')

btn_adicionar.on_click(on_adicionar)
btn_editar.on_click(on_editar)
btn_remover.on_click(on_remover)
btn_listar.on_click(on_listar)

# ============================================================
# LAYOUT
# ============================================================

cabecalho = pn.pane.HTML("""
    <div style="
        background-color: #9BE5AA;
        padding: 20px 32px;
        border-radius: 10px;
        margin-bottom: 20px;
    ">
        <h1 style="margin: 0; color: #1B5E20; font-size: 26px;">Registros de Campanhas</h1>
        <p style="margin: 6px 0 0 0; color: #2E7D32; font-size: 14px;">
            Preencha os campos com os dados necessários para cadastrar uma campanha.
        </p>
    </div>
""", sizing_mode='stretch_width')

formulario = pn.Column(
    pn.Row(id_input, gestor_input),
    pn.Row(nome_input, objetivo_input),
    pn.Row(data_inicio_input, data_fim_input),
    pn.Row(btn_adicionar, btn_editar, btn_remover, btn_listar),
    status_msg,
    styles={
        'background': '#F1FBF4',
        'border': '1.5px solid #9BE5AA',
        'border-radius': '10px',
        'padding': '24px',
    },
    sizing_mode='stretch_width',
)

conteudo = pn.Column(
    cabecalho,
    formulario,
    pn.Spacer(height=16),
    titulo_lista,
    campanhas_table,
    sizing_mode='stretch_width',
)

conteudo.servable(title='Registros de Campanhas')
