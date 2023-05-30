import sqlite3
import os.path
from werkzeug.security import check_password_hash,generate_password_hash
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "premium.db")
connection = sqlite3.connect(db_path, check_same_thread=False)

def init_db():
    users  = [
            ("Professor", "professor@pucminas.com", "professorpucminas", "1"),
            ("Samuel", "samuel@teste.com", "senhateste", "1"),
            ("Glauber", "glauber@teste.com", "senhateste", "1"),
        ]

    roles  = [
        ("Gerente"),
        ("Funcionário"),
        ("Produtor"),
        ("Cliente"),
        ("Sem Perfil")
    ]

    customers  = [
            ("Hospital Saúde", "hospital@teste.com", "000555333"),
            ("Vereador Paulinho", "vp@teste.com", "999333000"),
            ("Gustavo Sertanejo", "sertanejo@teste.com", "987654321"),
            ("Motor Rock", "rock@teste.com", "987654322"),
        ]

    producers  = [
            ("Flávio Marcos", "Gravação"),
            ("Leonardo Lanny", "Mixagem"),
            ("Bernardo Oliveira", "Produção Musical"),
            ("Samuel Marques", "Afinação")
        ]

    projects  = [
            ("Música Tema de Fim de Ano", "12000.00", "1", "1", 'Fim de Ano Hospital'),
            ("Jingle de Campanha", "15000.00", "2", "2", 'Candidatura Vereador Paulinho'),
            ("Album Motor Rock", "25000.00", "3", "3", 'Album Motor Rock'),
            ("Novo Single de Gustavo Sertanejo", "10000.00", "4", "4", 'Single Gustavo'),
        ]

    tasks = [ 
            ("Escrever a letra", "2023-05-03", "Focar nas coisas boas do ano", 1),
            ("Preparar harmonia", "2023-05-09", "Preparar com um clima bem animado", 1),
            ("Gravar rascunho para apresentar", "2023-05-13", "Manter a guia da voz e o instrumental simples", 1),
            ("Preparar o beat", "2023-05-04", "Cliente solicitou no estilo Pisadinha", 2),
            ("Compor a letra", "2023-05-08", "Focar em *Paulinho 23456, agora é nossa vez*", 2),
            ("Gravar os trompetes", "2023-05-13", "Manter a melodia simples", 2),
            ("Gravar os instrumentos", "2023-05-13", "Deixar o estúdio preparado para a bateria", 3),
            ("Editar a gravação", "2023-05-20", "Atenção com a música 3", 3),
            ("Gravar solo de guitarra", "2023-05-22", "Usar bastante distorção", 3),
            ("Gravar o vocal", "2023-04-03", "Cuidado com o refrão", 4),
            ("Afinar a voz", "2023-04-03", "Atenção nas notas agudas", 4),
            ("Mixar e masterizar", "2023-04-03", "Manter a sanfona aparecendo bastante nas faixas", 4),
    ]

    try:
        cur = connection.cursor()
        cur.execute("delete from user_role")
        cur.execute("delete from user")
        cur.execute("delete from customer")
        cur.execute("delete from producer")
        cur.execute("delete from project")
        cur.execute("delete from task")
        for data in roles: 
            cur.execute(f"INSERT INTO user_role (user_role) VALUES ('{data}')")
        for data in users: 
            cur.execute(f"INSERT INTO user (user_name, email, password, id_user_role) \
                        VALUES ('{data[0]}','{data[1]}','{generate_password_hash(data[2])}',{data[3]})")
        for data in producers: 
            cur.execute(f"INSERT INTO producer (name,area) \
                        VALUES ('{data[0]}','{data[1]}')")
        for data in customers: 
            cur.execute(f"INSERT INTO customer (name,email,phone_num) \
                        VALUES ('{data[0]}','{data[1]}', '{data[2]}')")
        for data in projects: 
            cur.execute(f"INSERT INTO project (description,full_value,id_customer,id_producer, name) \
                        VALUES ('{data[0]}','{data[1]}', {data[2]}, {data[3]}, '{data[4]}')") 
        for data in tasks:
            cur.execute(f"INSERT INTO task (title,deadline,description,id_project) \
                        VALUES ('{data[0]}','{data[1]}', '{data[2]}', {data[3]})")

        connection.commit()
        connection.close()
        return "DB inicializado com sucesso!"
    except Exception as erro:
        return f"Erro inicializando o db: {erro}"
