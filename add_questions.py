import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

questions = [
    ("Who is the father of Rama?", "Dasharatha", "Krishna", "Shiva", "Brahma", "Dasharatha"),
    ("Who wrote Mahabharata?", "Valmiki", "Vyasa", "Tulsidas", "Kalidasa", "Vyasa"),
    ("Who is Hanuman devoted to?", "Rama", "Krishna", "Shiva", "Indra", "Rama"),
    ("Who is the god of water?", "Varuna", "Agni", "Vayu", "Surya", "Varuna"),
    ("Who is the god of death?", "Yama", "Agni", "Indra", "Varuna", "Yama"),
    ("Who lifted Govardhan Hill?", "Krishna", "Balarama", "Indra", "Shiva", "Krishna")
]

cursor.executemany("""
INSERT INTO questions (question, option1, option2, option3, option4, answer)
VALUES (?, ?, ?, ?, ?, ?)
""", questions)

conn.commit()
conn.close()

print("Questions added successfully!")
