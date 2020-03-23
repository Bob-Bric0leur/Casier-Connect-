import sqlite3
database_name = "database.db"

#def collation_no_accent():
    
#Initialisation Bdd
def ini_database():
    conn = sqlite3.connect(database_name)
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE If NOT EXISTS users(
        user_uid TEXT UNIQUE NOT NULL PRIMARY KEY,
        nom TEXT NOT NULL,
        prenom TEXT NOT NULL,
        num_etu INTEGER UNIQUE NOT NULL,
        max_locker INTEGER DEFAULT 1
    )    
    """)
    cursor.execute("""
    CREATE TABLE If NOT EXISTS casiers (
        casier_id INTEGER NOT NULL PRIMARY KEY,
        i2c_adr TEXT NOT NULL,
        in_pin INT NOT NULL,
        out_pin INT NOT NULL,
        owner_uid TEXT,
        FOREIGN KEY (owner_uid)
            REFERENCES users (user_uid)
                ON DELETE SET NULL
                ON UPDATE CASCADE

    )
    """)

    conn.commit()


#ajouter un casier à la base de donnée
def add_casier(casier_id, i2c_adr, in_pin, out_pin):
    conn = sqlite3.connect(database_name)
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()

    cursor.execute("""INSERT INTO casiers(casier_id, i2c_adr, in_pin, out_pin) VALUES(?,?,?,?)""", (casier_id, i2c_adr, in_pin, out_pin,))

    conn.commit()


#ajouter un utilisateur à la base de donnée
def add_user(user_uid, num_etu, nom, prenom): 
    conn = sqlite3.connect(database_name)
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()

    cursor.execute("""INSERT INTO users(user_uid, num_etu, nom, prenom) VALUES(?,?,?,?)""", (user_uid, num_etu, nom, prenom,))

    conn.commit()

def add_user_to_casier(casier_id, owner_uid):
    conn = sqlite3.connect(database_name)
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()  

    cursor.execute("""UPDATE casiers SET owner_uid = ? WHERE casier_id = ?""", (owner_uid, casier_id,))

    conn.commit()

def select_all_casier():
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor() 

    cursor.execute("""SELECT * FROM casiers""")

    return cursor.fetchall()

def select_casier_by_id(id):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor() 

    cursor.execute("""SELECT * FROM casiers WHERE casier_id = ?""", (id,))

    return cursor.fetchall()[0]



def select_user_by_uid(uid):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor() 
    
    cursor.execute("""SELECT nom, prenom, num_etu FROM users WHERE user_uid=?""", (uid,))

    return cursor.fetchall()[0]

def select_user():
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT nom, prenom, user_uid 
    FROM users
    ORDER BY nom COLLATE NOCASE ASC, prenom COLLATE NOCASE ASC
    """)

    return cursor.fetchall() 

def partial_select(str):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * 
    FROM users 
    WHERE UPPER(nom || ' ' || prenom)   GLOB UPPER(?) 
    OR UPPER(prenom || ' ' || nom)   GLOB UPPER(?)
     
    """, (str+"*", str+"*",))

    return cursor.fetchall()

def partial_select_num(num_etu):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM users
    WHERE CAST(num_etu AS TEXT)  LIKE ?
    """, (str(num_etu)+"%",))

    return cursor.fetchall()
    

def set_max_locker(id, max):
    conn = sqlite3.connect(database_name)
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()  

    cursor.execute("""UPDATE users SET max_locker = ? WHERE user_uid = ?""", (max, id,))

    conn.commit()    


def get_max_locker(uid):
    conn = sqlite3.connect(database_name)
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()

    cursor.execute("""SELECT max_locker FROM users WHERE user_uid=?""", (uid,))

    return cursor.fetchall()[0][0]





#test des fonctions

ini_database()






"""

for i in range (10, 50):
    add_user(i, "valentin", str(i))
"""

"""add_user("504565", 21902626, "gousset", "mda")
add_user("55", 21902626,"toto", "tata")
add_user("4744787", 21902626, "beta", "luc")


add_user("bgfdyuzgbqui", 21902626, "L'hermite", "Valentin")
add_user("154564664", 21902626, "l'hermite", "valentin")
add_user("1234", 21902626, "Bob", "Eponge")"""
#print(select_user()

#add_user("47456456", "bébé", "yoda")


#print(get_max_locker("47456456"))
#set_max_locker("47456456", 2)
#print(get_max_locker("47456456"))


#print(partial_select("v"))
#add_casier(1, "0x20", 1, 2)

print(select_all_casier())

print(partial_select_num(3))