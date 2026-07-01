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

#funcao inserir
def inserir_paciente(cns, data_nascimento, sexo, longitude, latitude, rua, bairro, numero):
    with engine.connect() as conn:
        conn.execute(text("""
            INSERT INTO Paciente (cns, data_de_nascimento, sexo, longitude, latitude, rua, bairro, numero)
            VALUES (:cns, :data_nasc, :sexo, :longitude, :latitude, :rua, :bairro, :numero)
        """), {"cns": cns, "data_nasc": data_nascimento, "sexo": sexo,
               "longitude": longitude, "latitude": latitude,
               "rua": rua, "bairro": bairro, "numero": numero})
        conn.commit()

#funcao editar
def editar_paciente(cns, data_nascimento, sexo, longitude, latitude, rua, bairro, numero):
    with engine.connect() as conn:
        conn.execute(text("""
            UPDATE Paciente
            SET data_de_nascimento = :data_nasc, sexo = :sexo,
                longitude = :longitude, latitude = :latitude,
                rua = :rua, bairro = :bairro, numero = :numero
            WHERE cns = :cns
        """), {"cns": cns, "data_nasc": data_nascimento, "sexo": sexo,
               "longitude": longitude, "latitude": latitude,
               "rua": rua, "bairro": bairro, "numero": numero})
        conn.commit()

#funcao excluir
def excluir_paciente(cns):
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM Paciente WHERE cns = :cns"), {"cns": cns})
        conn.commit()

# tabela de pacientes
pacientes_table = pn.widgets.Tabulator(
    value=pd.DataFrame(),
    pagination='remote',
    page_size=10,
    show_index=False,
    height=300,
    sizing_mode='stretch_width',
    visible=False,
)

#campos do formulario
cns_input        = pn.widgets.TextInput(name='CNS do Paciente (identificador)', placeholder='CNS001', width=260)
nascimento_input = pn.widgets.DatePicker(name='Data de Nascimento', value=date(2000, 1, 1), width=260)
sexo_input       = pn.widgets.Select(name='Sexo', options=['Feminino', 'Masculino', 'Outro'], width=260)
longitude_input  = pn.widgets.FloatInput(name='Longitude', value=-38.5, width=260)
latitude_input   = pn.widgets.FloatInput(name='Latitude', value=-3.7, width=260)
rua_input        = pn.widgets.TextInput(name='Rua', placeholder='Rua A', width=260)
bairro_input     = pn.widgets.TextInput(name='Bairro', placeholder='Centro', width=260)
numero_input     = pn.widgets.IntInput(name='Número', value=1, width=260)

# botoes
btn_adicionar = pn.widgets.Button(name='Adicionar', button_type='default', width=130)
btn_editar    = pn.widgets.Button(name='Editar', button_type='default', width=130)
btn_remover   = pn.widgets.Button(name='Remover', button_type='default', width=130)
btn_listar    = pn.widgets.Button(name='Listar', button_type='default', width=130)

status_msg   = pn.pane.Markdown('', styles={'font-weight': 'bold'})
titulo_lista = pn.pane.Markdown('### Lista de Pacientes', visible=False)


def atualizar_status(texto):
    status_msg.object = texto


def atualizar_tabela():
    pacientes_table.value = listar_pacientes()


#limpar formulario
def limpar_formulario():
    cns_input.value        = ''
    nascimento_input.value = date(2000, 1, 1)
    sexo_input.value       = 'Feminino'
    longitude_input.value  = -38.5
    latitude_input.value   = -3.7
    rua_input.value        = ''
    bairro_input.value     = ''
    numero_input.value     = 1

def on_adicionar(event):
    if not cns_input.value or not nascimento_input.value or not rua_input.value or not bairro_input.value:
        atualizar_status('Preencha todos os campos obrigatórios.')
        return
    try:
        inserir_paciente(cns_input.value, nascimento_input.value, sexo_input.value,
                          longitude_input.value, latitude_input.value,
                          rua_input.value, bairro_input.value, numero_input.value)
        atualizar_status('Paciente adicionado com sucesso.')
        limpar_formulario()
        atualizar_tabela()
    except IntegrityError:
        atualizar_status('Erro: CNS já cadastrado no banco.')
    except Exception as e:
        atualizar_status(f'Erro ao adicionar: {e}')

def on_editar(event):
    if not cns_input.value:
        atualizar_status('Informe o CNS do paciente para editar.')
        return
    try:
        editar_paciente(cns_input.value, nascimento_input.value, sexo_input.value,
                         longitude_input.value, latitude_input.value,
                         rua_input.value, bairro_input.value, numero_input.value)
        atualizar_status('Paciente atualizado com sucesso.')
        limpar_formulario()
        atualizar_tabela()
    except Exception as e:
        atualizar_status(f'Erro ao editar: {e}')

def on_remover(event):
    if not cns_input.value:
        atualizar_status('Informe o CNS do paciente para remover.')
        return
    try:
        excluir_paciente(cns_input.value)
        atualizar_status('Paciente removido com sucesso.')
        limpar_formulario()
        atualizar_tabela()
    except IntegrityError:
        atualizar_status('Erro: paciente possui registros vinculados (visitas, procedimentos ou feedback).')
    except Exception as e:
        atualizar_status(f'Erro ao remover: {e}')


def on_listar(event):
    if pacientes_table.visible:
        pacientes_table.visible = False
        titulo_lista.visible    = False
        atualizar_status('Tabela oculta.')
        return
    atualizar_tabela()
    pacientes_table.visible = True
    titulo_lista.visible    = True
    atualizar_status('Tabela exibida.')

btn_adicionar.on_click(on_adicionar)
btn_editar.on_click(on_editar)
btn_remover.on_click(on_remover)
btn_listar.on_click(on_listar)

# layout da pagina
cabecalho = pn.pane.HTML("""
    <div style="
        background-color: #9BE5AA;
        padding: 20px 32px;
        border-radius: 10px;
        margin-bottom: 20px;
    ">
        <h1 style="margin: 0; color: #1B5E20; font-size: 26px;">Registros de Pacientes</h1>
        <p style="margin: 6px 0 0 0; color: #2E7D32; font-size: 14px;">
            Preencha os campos com os dados necessários para registrar um paciente. Use o CNS para editar ou remover.
        </p>
    </div>
""", sizing_mode='stretch_width')

formulario = pn.Column(
    pn.Row(cns_input,       nascimento_input),
    pn.Row(sexo_input,      numero_input),
    pn.Row(longitude_input, latitude_input),
    pn.Row(rua_input,       bairro_input),
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
    pacientes_table,
    sizing_mode='stretch_width',
)

conteudo.servable(title='Registros de Pacientes')


