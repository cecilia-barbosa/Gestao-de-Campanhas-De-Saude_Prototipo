CREATE TABLE Usuario (
	id_user SERIAL PRIMARY KEY,
	p_nome varchar (100) NOT NULL,
	sobrenome varchar (100) NOT NULL,
	email varchar (100) NOT NULL,
	senha varchar (100) NOT NULL
);

CREATE TABLE Gestor (
	id_gestor int PRIMARY KEY,
	cargo Varchar (100) NOT NULL,
	FOREIGN KEY (id_gestor) REFERENCES Usuario(id_user)
);

CREATE TABLE Voluntario (
	id_voluntario int PRIMARY KEY,
	inscricao int NOT NULL,
	FOREIGN KEY (id_voluntario) REFERENCES Usuario(id_user)
);

CREATE TABLE Agente_de_saude (
	id_agente int PRIMARY KEY,
	dispositivo_id int NOT NULL,
	area_de_atuacao Varchar (100) NOT NULL,	
	FOREIGN KEY (id_agente) REFERENCES Usuario(id_user)
);

CREATE TABLE Notificacao(
	id_notificacao SERIAL PRIMARY KEY,
	canal varchar (100) NOT NULL,
	conteudo varchar (100) NOT NULL,
	id_destinatario int NOT NULL,
	FOREIGN KEY (id_destinatario) REFERENCES Usuario(id_user)
);

CREATE TABLE Campanha (
	id_campanha SERIAL PRIMARY KEY,
	nome varchar (100) NOT NULL,
	objetivo varchar (100) NOT NULL,
	data_inicio date NOT NULL,
	data_fim date NOT NULL,
	id_gestor int NOT NULL,
	FOREIGN KEY (id_gestor) REFERENCES Gestor(id_gestor)
);

CREATE TABLE Evento (
	id_evento SERIAL PRIMARY KEY,
	tipo varchar (100) NOT NULL,
	local varchar (100) NOT NULL,
	data date NOT NULL,
	hora time NOT NULL,
	id_campanha int NOT NULL,
	FOREIGN KEY (id_campanha) REFERENCES Campanha(id_campanha) ON DELETE CASCADE
);

CREATE TABLE Equipe (
	id_equipe SERIAL PRIMARY KEY,
	nome_equipe varchar (100) NOT NULL,
	id_campanha int NOT NULL,
	FOREIGN KEY (id_campanha) REFERENCES Campanha(id_campanha) ON DELETE CASCADE
);

--Relaçao Voluntario participa de Equipe 
CREATE TABLE Equipe_voluntaria (
	id_equipe int PRIMARY KEY,
	id_voluntario int NOT NULL,
	FOREIGN KEY (id_voluntario) REFERENCES Voluntario(id_voluntario),
	FOREIGN KEY (id_equipe) REFERENCES Equipe(id_equipe)
);

--Relacao Agente participa de Equipe
CREATE TABLE Equipe_de_agentes (
	id_equipe int PRIMARY KEY,
	id_agente int NOT NULL,
	FOREIGN KEY (id_agente) REFERENCES Agente_de_saude(id_agente),
	FOREIGN KEY (id_equipe) REFERENCES Equipe(id_equipe) 
);

CREATE TABLE Paciente (
	CNS varchar(20) PRIMARY KEY,
	data_de_nascimento date NOT NULL,
	sexo varchar(100) NOT NULL,
	longitude float NOT NULL,
	latitude float NOT NULL,
	rua varchar(100) NOT NULL,
	bairro varchar (100) NOT NULL,
	numero int NOT NULL
);

CREATE TABLE Feedback (
	id_feedback SERIAL PRIMARY KEY,
	nota int NOT NULL,
	comentario varchar (100),
	CNS_paciente varchar (20) NOT NULL,
	FOREIGN KEY (CNS_paciente) REFERENCES Paciente(CNS)
);

CREATE TABLE Visita (
    id_visita SERIAL PRIMARY KEY,
    horario time NOT NULL,
    data date NOT NULL,
    sincronizacao_do_agente boolean NOT NULL,
    id_agente int NOT NULL,
    cns_paciente varchar(20) NOT NULL,
    FOREIGN KEY (id_agente) REFERENCES Agente_de_saude(id_agente),
    FOREIGN KEY (cns_paciente) REFERENCES Paciente(cns)
);

-- Atributo sintomas multivalorado
CREATE TABLE Visita_Sintomas (
    id_visita int NOT NULL,
    descricao_sintoma varchar(100) NOT NULL,
	PRIMARY KEY(id_visita, descricao_sintoma),
    FOREIGN KEY (id_visita) REFERENCES Visita(id_visita)
);

CREATE TABLE Insumo (
	id_insumo int PRIMARY KEY,
	data_reposicao date NOT NULL,
	tipo varchar (100) NOT NULL,
	nome varchar (100) NOT NULL,
	validade date NOT NULL
); 

CREATE TABLE Procedimento (
	id_procedimento int PRIMARY KEY,
	dose_aplicada varchar(100) NOT NULL,
	local varchar (100) NOT NULL,
	data date NOT NULL,
	hora time NOT NULL, 
	sincronizacao_do_agente boolean NOT NULL,
	id_agente int NOT NULL,
    cns_paciente varchar(20) NOT NULL,
	id_insumo int NOT NULL,
    baixa_estoque boolean, 
	FOREIGN KEY (id_agente) REFERENCES Agente_de_saude(id_agente),
    FOREIGN KEY (cns_paciente) REFERENCES Paciente(cns),
    FOREIGN KEY (id_agente) REFERENCES Agente_de_saude(id_agente),
    FOREIGN KEY (cns_paciente) REFERENCES Paciente(CNS),
    FOREIGN KEY (id_insumo) REFERENCES Insumo(id_insumo)
);

-- Iserção das tuplas
-- 1. Inserir 30 Usuários (1-10 Gestores, 11-20 Voluntários, 21-30 Agentes)
INSERT INTO Usuario (p_nome, sobrenome, email, senha) VALUES
('Ana', 'Silva', 'ana@email.com', 'senha123'), ('Bruno', 'Costa', 'bruno@email.com', 'senha123'),
('Carlos', 'Mendes', 'carlos@email.com', 'senha123'), ('Daniela', 'Rocha', 'daniela@email.com', 'senha123'),
('Eduardo', 'Lima', 'eduardo@email.com', 'senha123'), ('Fernanda', 'Gomes', 'fernanda@email.com', 'senha123'),
('Gabriel', 'Martins', 'gabriel@email.com', 'senha123'), ('Helena', 'Ribeiro', 'helena@email.com', 'senha123'),
('Igor', 'Fernandes', 'igor@email.com', 'senha123'), ('Julia', 'Carvalho', 'julia@email.com', 'senha123'),
('Lucas', 'Almeida', 'lucas@email.com', 'senha123'), ('Mariana', 'Pinto', 'mariana@email.com', 'senha123'),
('Nicolas', 'Teixeira', 'nicolas@email.com', 'senha123'), ('Olivia', 'Souza', 'olivia@email.com', 'senha123'),
('Pedro', 'Oliveira', 'pedro@email.com', 'senha123'), ('Quintino', 'Araujo', 'quintino@email.com', 'senha123'),
('Rafaela', 'Monteiro', 'rafaela@email.com', 'senha123'), ('Samuel', 'Correia', 'samuel@email.com', 'senha123'),
('Tatiana', 'Moraes', 'tatiana@email.com', 'senha123'), ('Ursula', 'Farias', 'ursula@email.com', 'senha123'),
('Vinicius', 'Nunes', 'vinicius@email.com', 'senha123'), ('Wagner', 'Vieira', 'wagner@email.com', 'senha123'),
('Xuxa', 'Meneghel', 'xuxa@email.com', 'senha123'), ('Yago', 'Campos', 'yago@email.com', 'senha123'),
('Zelia', 'Cardoso', 'zelia@email.com', 'senha123'), ('Alice', 'Batista', 'alice@email.com', 'senha123'),
('Beto', 'Dias', 'beto@email.com', 'senha123'), ('Carla', 'Freitas', 'carla@email.com', 'senha123'),
('Diego', 'Macedo', 'diego@email.com', 'senha123'), ('Elisa', 'Pires', 'elisa@email.com', 'senha123');

-- 4. Inserir 10 Gestores (Usando IDs de Usuário 1 a 10)
INSERT INTO Gestor (id_gestor, cargo) VALUES
(1, 'Coordenador Geral'), (2, 'Supervisor de Área'), (3, 'Diretor de Saúde'), 
(4, 'Gerente de Logística'), (5, 'Coordenador de Equipe'), (6, 'Chefe de Plantão'), 
(7, 'Diretor Administrativo'), (8, 'Supervisor de Insumos'), (9, 'Gerente de RH'), 
(10, 'Coordenador de TI');

-- 5. Inserir 10 Voluntários (Usando IDs de Usuário 11 a 20)
INSERT INTO Voluntario (id_voluntario, inscricao) VALUES
(11, 1001), (12, 1002), (13, 1003), (14, 1004), (15, 1005), 
(16, 1006), (17, 1007), (18, 1008), (19, 1009), (20, 1010);

-- 6. Inserir 10 Agentes de Saúde (Usando IDs de Usuário 21 a 30)
INSERT INTO Agente_de_saude (id_agente, dispositivo_id, area_de_atuacao) VALUES
(21, 501, 'Zona Norte'), (22, 502, 'Zona Sul'), (23, 503, 'Zona Leste'), 
(24, 504, 'Zona Oeste'), (25, 505, 'Centro'), (26, 506, 'Bairro A'), 
(27, 507, 'Bairro B'), (28, 508, 'Bairro C'), (29, 509, 'Rural 1'), 
(30, 510, 'Rural 2');

-- 2. Inserir 10 Pacientes
INSERT INTO Paciente (CNS, data_de_nascimento, sexo, longitude, latitude, rua, bairro, numero) VALUES
('CNS001', '1990-05-15', 'Feminino', -38.5, -3.7, 'Rua A', 'Centro', 10),
('CNS002', '1985-08-20', 'Masculino', -38.6, -3.8, 'Rua B', 'Aldeota', 20),
('CNS003', '2000-01-10', 'Feminino', -38.4, -3.9, 'Rua C', 'Meireles', 30),
('CNS004', '1975-11-30', 'Masculino', -38.7, -3.6, 'Rua D', 'Cocó', 40),
('CNS005', '2010-04-25', 'Feminino', -38.5, -3.7, 'Rua E', 'Papicu', 50),
('CNS006', '1960-12-05', 'Masculino', -38.6, -3.8, 'Rua F', 'Messejana', 60),
('CNS007', '1995-07-14', 'Feminino', -38.4, -3.9, 'Rua G', 'Parangaba', 70),
('CNS008', '1988-02-28', 'Masculino', -38.7, -3.6, 'Rua H', 'Fátima', 80),
('CNS009', '2005-09-18', 'Feminino', -38.5, -3.7, 'Rua I', 'Benfica', 90),
('CNS010', '1992-03-22', 'Masculino', -38.6, -3.8, 'Rua J', 'Montese', 100);

-- 3. Inserir 10 Insumos (Obrigatório antes de Procedimento)
INSERT INTO Insumo (id_insumo, data_reposicao, tipo, nome, validade) VALUES
(1, '2023-10-01', 'Vacina', 'Pfizer', '2024-10-01'),
(2, '2023-10-02', 'Vacina', 'Coronavac', '2024-10-02'),
(3, '2023-10-03', 'Medicamento', 'Paracetamol', '2025-10-03'),
(4, '2023-10-04', 'Material', 'Seringa 5ml', '2028-10-04'),
(5, '2023-10-05', 'Material', 'Agulha', '2028-10-05'),
(6, '2023-10-06', 'Medicamento', 'Ibuprofeno', '2025-10-06'),
(7, '2023-10-07', 'Vacina', 'AstraZeneca', '2024-10-07'),
(8, '2023-10-08', 'Material', 'Gaze', '2026-10-08'),
(9, '2023-10-09', 'Material', 'Álcool 70%', '2025-10-09'),
(10, '2023-10-10', 'Medicamento', 'Dipirona', '2025-10-10');

-- 7. Inserir 10 Notificações
INSERT INTO Notificacao (canal, conteudo, id_destinatario) VALUES
('SMS', 'Sua visita foi agendada.', 21), ('Email', 'Reunião de equipe amanhã.', 1),
('App', 'Alerta de nova campanha.', 11), ('SMS', 'Paciente aguardando.', 22),
('Email', 'Relatório mensal.', 2), ('App', 'Falta de insumos detectada.', 3),
('SMS', 'Atualização do sistema.', 25), ('Email', 'Cadastro aprovado.', 15),
('App', 'Lembrete de vacinação.', 5), ('SMS', 'Novo procedimento adicionado.', 28);

-- 8. Inserir 10 Campanhas
INSERT INTO Campanha (nome, objetivo, data_inicio, data_fim, id_gestor) VALUES
('Campanha Inverno', 'Prevenção da Gripe', '2024-05-01', '2024-07-30', 1),
('Vacina Brasil', 'Aumentar imunização', '2024-01-10', '2024-12-31', 2),
('Saúde na Escola', 'Avaliação infantil', '2024-03-01', '2024-03-31', 3),
('Mutirão Dengue', 'Combate a focos', '2024-02-15', '2024-04-15', 4),
('Outubro Rosa', 'Prevenção Câncer de Mama', '2024-10-01', '2024-10-31', 5),
('Novembro Azul', 'Saúde do Homem', '2024-11-01', '2024-11-30', 6),
('Saúde no Campo', 'Atendimento Rural', '2024-06-01', '2024-06-15', 7),
('Odonto Solidária', 'Saúde Bucal', '2024-08-01', '2024-08-20', 8),
('Dia V', 'Vacinação em massa', '2024-09-10', '2024-09-10', 9),
('Dezembro Vermelho', 'Conscientização HIV', '2024-12-01', '2024-12-31', 10);

-- 9. Inserir 10 Eventos
INSERT INTO Evento (tipo, local, data, hora, id_campanha) VALUES
('Palestra', 'Posto Central', '2024-05-10', '09:00', 1),
('Aplicação', 'Praça da Sé', '2024-02-20', '08:00', 2),
('Triagem', 'Escola Municipal', '2024-03-05', '10:00', 3),
('Vistoria', 'Bairro A', '2024-02-16', '14:00', 4),
('Exame', 'Clínica da Mulher', '2024-10-15', '08:00', 5),
('Consulta', 'Posto Sul', '2024-11-10', '09:00', 6),
('Mutirão', 'Sítio Pica-Pau', '2024-06-05', '07:00', 7),
('Avaliação', 'Centro Comunitário', '2024-08-10', '13:00', 8),
('Vacinação', 'Ginásio', '2024-09-10', '08:00', 9),
('Ação Social', 'Praça Central', '2024-12-15', '18:00', 10);

-- 10. Inserir 10 Equipes
INSERT INTO Equipe (nome_equipe, id_campanha) VALUES
('Equipe Alfa', 1), ('Equipe Beta', 2), ('Equipe Gama', 3),
('Equipe Delta', 4), ('Equipe Eco', 5), ('Equipe Fox', 6),
('Equipe Golf', 7), ('Equipe Hotel', 8), ('Equipe India', 9),
('Equipe Juliet', 10);

-- 11. Inserir 10 Equipe_voluntaria 
INSERT INTO Equipe_voluntaria (id_equipe, id_voluntario) VALUES
(1, 11), (2, 12), (3, 13), (4, 14), (5, 15),
(6, 16), (7, 17), (8, 18), (9, 19), (10, 20);

-- 12. Inserir 10 Equipe_de_agentes
INSERT INTO Equipe_de_agentes (id_equipe, id_agente) VALUES
(1, 21), (2, 22), (3, 23), (4, 24), (5, 25),
(6, 26), (7, 27), (8, 28), (9, 29), (10, 30);

-- 13. Inserir 10 Feedbacks
INSERT INTO Feedback (nota, comentario, CNS_paciente) VALUES
(5, 'Ótimo atendimento', 'CNS001'), (4, 'Fui bem tratado', 'CNS002'),
(3, 'Muito demorado', 'CNS003'), (5, 'Agente muito atencioso', 'CNS004'),
(2, 'Faltou material', 'CNS005'), (5, 'Perfeito', 'CNS006'),
(4, 'Bom, mas pode melhorar', 'CNS007'), (5, 'Rápido e eficiente', 'CNS008'),
(1, 'Péssima experiência', 'CNS009'), (5, 'Gostei muito da campanha', 'CNS010');

-- 14. Inserir 10 Visitas
INSERT INTO Visita (horario, data, sincronizacao_do_agente, id_agente, cns_paciente) VALUES
('09:00', '2024-05-15', true, 21, 'CNS001'), ('10:30', '2024-05-16', true, 22, 'CNS002'),
('14:00', '2024-05-17', false, 23, 'CNS003'), ('15:45', '2024-05-18', true, 24, 'CNS004'),
('08:15', '2024-05-19', true, 25, 'CNS005'), ('11:00', '2024-05-20', false, 26, 'CNS006'),
('13:30', '2024-05-21', true, 27, 'CNS007'), ('16:00', '2024-05-22', true, 28, 'CNS008'),
('09:45', '2024-05-23', false, 29, 'CNS009'), ('14:20', '2024-05-24', true, 30, 'CNS010');

-- 15. Inserir 10 Sintomas para as Visitas (Atributo Multivalorado)
INSERT INTO Visita_Sintomas (id_visita, descricao_sintoma) VALUES
(1, 'Febre Alta'), (2, 'Tosse Seca'), (3, 'Dor de Cabeça'),
(4, 'Coriza'), (5, 'Dor no Corpo'), (6, 'Enjoo'),
(7, 'Falta de Ar'), (8, 'Garganta Inflamada'), (9, 'Calafrios'),
(10, 'Fraqueza');

-- 16. Inserir 10 Procedimentos
INSERT INTO Procedimento (id_procedimento, dose_aplicada, local, data, hora, sincronizacao_do_agente, id_agente, cns_paciente, id_insumo, baixa_estoque) VALUES
(1, '0.5ml', 'Braço Esquerdo', '2024-05-15', '09:15', true, 21, 'CNS001', 1, true),
(2, '0.5ml', 'Braço Direito', '2024-05-16', '10:45', true, 22, 'CNS002', 2, true),
(3, '1 Comprimido', 'Via Oral', '2024-05-17', '14:10', false, 23, 'CNS003', 3, true),
(4, 'N/A', 'Curativo Perna', '2024-05-18', '16:00', true, 24, 'CNS004', 8, true),
(5, '10 gotas', 'Via Oral', '2024-05-19', '08:30', true, 25, 'CNS005', 6, true),
(6, 'N/A', 'Aferição de Pressão', '2024-05-20', '11:10', false, 26, 'CNS006', 4, false),
(7, '0.5ml', 'Braço Esquerdo', '2024-05-21', '13:40', true, 27, 'CNS007', 7, true),
(8, 'N/A', 'Limpeza de Ferida', '2024-05-22', '16:15', true, 28, 'CNS008', 9, true),
(9, '1 Ampola', 'Glúteo', '2024-05-23', '10:00', false, 29, 'CNS009', 10, true),
(10, 'N/A', 'Triagem', '2024-05-24', '14:30', true, 30, 'CNS010', 5, false);