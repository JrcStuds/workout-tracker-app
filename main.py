import sqlite3

conn = sqlite3.connect('workouts.db')
c = conn.cursor()

# c.execute("""CREATE TABLE IF NOT EXISTS workouts (
#             workoutid integer,
#             date text
#           )""")

# c.execute("""CREATE TABLE IF NOT EXISTS exercises (
#             exerciseid integer,
#             workoutid integer,
#             exercisename text
#           )""")

# c.execute("""CREATE TABLE IF NOT EXISTS sets (
#             setid integer,
#             exerciseid integer,
#             setnumber integer,
#             weight real,
#             reps integer,
#             rir integer
#           )""")

# c.execute("INSERT INTO workouts VALUES (:workoutid, :date)", {
#     "workoutid": 1,
#     "date": "2025-04-14"
#     })
# c.execute("INSERT INTO exercises VALUES (:exerciseid, :workoutid, :exercisename)", {
#     "exerciseid": 1,
#     "workoutid": 1,
#     "exercisename": "bench-press"
#     })
# c.execute("INSERT INTO sets VALUES (:setid, :exerciseid, :setnumber, :weight, :reps, :rir)", {
#     "setid": 1,
#     "exerciseid": 1,
#     "setnumber": 1,
#     "weight": 60,
#     "reps": 8,
#     "rir": 2
#     })
# c.execute("INSERT INTO sets VALUES (:setid, :exerciseid, :setnumber, :weight, :reps, :rir)", {
#     "setid": 2,
#     "exerciseid": 1,
#     "setnumber": 2,
#     "weight": 60,
#     "reps": 7,
#     "rir": 1
#     })
# c.execute("INSERT INTO exercises VALUES (:exerciseid, :workoutid, :exercisename)", {
#     "exerciseid": 2,
#     "workoutid": 1,
#     "exercisename": "squat"
#     })
# c.execute("INSERT INTO sets VALUES (:setid, :exerciseid, :setnumber, :weight, :reps, :rir)", {
#     "setid": 3,
#     "exerciseid": 2,
#     "setnumber": 1,
#     "weight": 80,
#     "reps": 8,
#     "rir": 2
#     })
# c.execute("INSERT INTO sets VALUES (:setid, :exerciseid, :setnumber, :weight, :reps, :rir)", {
#     "setid": 4,
#     "exerciseid": 2,
#     "setnumber": 2,
#     "weight": 80,
#     "reps": 7,
#     "rir": 1
#     })

# conn.commit()

# c.execute("SELECT * FROM workouts")
# print(c.fetchall())

# c.execute("SELECT * FROM exercises")
# print(c.fetchall())

# c.execute("SELECT * FROM sets")
# print(c.fetchall())

# c.execute("SELECT reps FROM sets WHERE exerciseid=2 GROUP BY setnumber")
# print(c.fetchall())

c.execute("DELETE FROM workouts")
c.execute("DELETE FROM exercises")
c.execute("DELETE FROM sets")

conn.commit()

c.execute("SELECT * FROM workouts")
print(c.fetchall())

c.execute("SELECT * FROM exercises")
print(c.fetchall())

c.execute("SELECT * FROM sets")
print(c.fetchall())

conn.close()