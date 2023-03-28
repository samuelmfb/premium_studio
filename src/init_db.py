import sqlite3
import os.path
from werkzeug.security import check_password_hash,generate_password_hash
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "premium.db")
connection = sqlite3.connect(db_path, check_same_thread=False)

def init_db():
    users  = [
            ("teste", "teste@teste.com", "senhateste", "2"),
            ("samuel", "samuel@teste.com", "senhateste", "1"),
            ("glauber", "glauber@teste.com", "senhateste", "1"),
        ]

    roles  = [
        ("Gerente"),
        ("Funcionário"),
        ("Produtor"),
        ("Cliente"),
    ]

    customers  = [
            ("Kylie Minogue", "kylie@teste.com", "000555333"),
            ("Vereador Paulinho", "vp@teste.com", "999333000"),
            ("ACDC", "acdc@teste.com", "987654321"),
        ]

    producers  = [
            ("Mark Ronson", "Gravação"),
            ("Pharrell Williams", "Afinação"),
            ("Will.I.Am", "Produção Musical"),
        ]

    projects  = [
            ("Álbum Kylie Minogue", "120000.00", "1", "1", 'Kylie on Acid'),
            ("Jingle de Campanha", "15000.00", "2", "2", 'Caixa 2 do Partido'),
            ("Remix de Thunderstorm", "20000.00", "3", "3", 'Trovão do amor'),
        ]

    tasks = [ 
            ("Afinar voz", "2023-04-03", "Cuidado com o refrão", 1),
            ("Preparar beat", "2023-04-03", "Deixar o groove bem animado", 1),
            ("Gravar solo de guitarra", "2023-04-03", "Usar bastante distorção", 1),
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
            cur.execute(f"INSERT INTO user_role (user_role_name) VALUES ('{data}')")
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
