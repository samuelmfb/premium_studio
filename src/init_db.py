import sqlite3
import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "premium.db")
connection = sqlite3.connect(db_path)


users  = [
        ("teste", "teste@teste.com", "e0e17f7927ac6c5e4727f336f3a74171aa1162994a732f356cfe60ec7aeae902", "2"),
        ("samuel", "samuel@teste.com", "e0e17f7927ac6c5e4727f336f3a74171aa1162994a732f356cfe60ec7aeae902", "1"),
        ("glauber", "glauber@teste.com", "e0e17f7927ac6c5e4727f336f3a74171aa1162994a732f356cfe60ec7aeae902", "1"),
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
        ("Álbum Kylie Minogue", "120000.00", "1", "1"),
        ("Jingle de Campanha", "15000.00", "2", "2"),
        ("Remix de Thunderstorm", "20000.00", "3", "3"),
    ]

cur = connection.cursor()
cur.execute("delete from user_role")
cur.execute("delete from user")
cur.execute("delete from customer")
cur.execute("delete from producer")
cur.execute("delete from project")
for data in roles: 
    cur.execute(f"INSERT INTO user_role (user_role_name) VALUES ('{data}')")
for data in users: 
    cur.execute(f"INSERT INTO user (user_name, email, password, id_user_role) \
                VALUES ('{data[0]}','{data[1]}','{data[2]}',{data[3]})")
for data in producers: 
    cur.execute(f"INSERT INTO producer (name,area) \
                VALUES ('{data[0]}','{data[1]}')")
for data in customers: 
    cur.execute(f"INSERT INTO customer (name,email,phone_num) \
                VALUES ('{data[0]}','{data[1]}', '{data[2]}')")
for data in projects: 
    cur.execute(f"INSERT INTO project (description,full_value,id_customer,id_producer) \
                VALUES ('{data[0]}','{data[1]}', {data[2]}, {data[3]})")

connection.commit()
connection.close()
