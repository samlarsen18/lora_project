import sqlite3

conn = sqlite3.connect('test_db.sqlite')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS first_table (name VARCHAR, description VARCHAR)')
conn.commit()

while True:
    name = input("Give a name: ")
    desc = input("Give a description: ")

    if name == 'quit' or desc == 'quit':
        break
    
    cur.execute('INSERT INTO first_table (name, description) values ("{}", "{}")'.format(name,desc))
    conn.commit()
    print("Saved to DB\n")
    

conn.close()