import sqlite3

class OpenTableDB:
    def __init__(self):
        self.connection = sqlite3.connect("quiz.sql")
    
    def add_user(self, username):
        cursor = self.connection.cursor()
        sql_query_zero_id = "SELECT user_id FROM Users WHERE user_id = 0"
        sql_query = "INSERT INTO Users (user_id, username) VALUES (?, ?)"
        cursor.execute(sql_query_zero_id)
        res_zero_id = cursor.fetchall()
        if len(res_zero_id) == 0:
            cursor.execute(sql_query, (0, username))
            self.connection.commit()
        else:
            sql_query_id = "SELECT MAX(user_id) FROM Users"
            cursor.execute(sql_query_id)
            res_id = cursor.fetchall()
            new_id = int(str(res_id)[2:-3:]) + 1
            cursor.execute(sql_query, (new_id, username))
            self.connection.commit()
        cursor.close()

    def user_in_db(self, username):
        cursor = self.connection.cursor()
        sql_user_query = f"SELECT username FROM Users WHERE username = '{username}'"
        cursor.execute(sql_user_query)
        res_user = cursor.fetchall()
        cursor.close()
        if len(res_user) != 0:
            return True
        return False
    
    def user_id(self, username):
        cursor = self.connection.cursor()
        sql_query_id = f"SELECT user_id FROM Users WHERE username = '{username}'"
        cursor.execute(sql_query_id)
        res = cursor.fetchall()
        id = int(str(res)[2:-3])
        cursor.close()
        return id
    
    
    def add_theme_in_base(self, name, user_id):
        cursor = self.connection.cursor()
        sql_query_zero_id = "SELECT card_id FROM Cards WHERE card_id = 0"
        sql_query = "INSERT INTO Cards (card_id, user_id, card_name) VALUES (?, ?, ?)"
        cursor.execute(sql_query_zero_id)
        res_zero_id = cursor.fetchall()
        if len(res_zero_id) == 0:
            cursor.execute(sql_query, (0, user_id, name))
        else:
            sql_query_id = "SELECT MAX(card_id) FROM Cards"
            cursor.execute(sql_query_id)
            res_id = cursor.fetchall()
            new_id = int(str(res_id)[2:-3:]) + 1
            cursor.execute(sql_query, (new_id, user_id, name))
        self.connection.commit()
        cursor.close()

    def add_que_in_base(self, card_id, que, ans):
        cursor = self.connection.cursor()
        sql_query_zero_id = "SELECT que_id FROM Ques WHERE que_id = 0"
        sql_query = "INSERT INTO Ques (que_id, card_id, que, ans) VALUES (?, ?, ?, ?)"
        cursor.execute(sql_query_zero_id)
        res_zero_id = cursor.fetchall()
        if len(res_zero_id) == 0:
            cursor.execute(sql_query, (0, card_id, que, ans))
        else:
            sql_query_id = "SELECT MAX(que_id) FROM Ques"
            cursor.execute(sql_query_id)
            res_id = cursor.fetchall()
            new_id = int(str(res_id)[2:-3:]) + 1
            cursor.execute(sql_query, (new_id, card_id, que, ans))
        self.connection.commit()
        cursor.close()

    def theme_in_db(self, name, user_id):
        cursor = self.connection.cursor()
        sql_user_query = f"SELECT card_name FROM Cards WHERE card_name = '{name}' AND user_id = {user_id}"
        cursor.execute(sql_user_query)
        res = cursor.fetchall()
        cursor.close()
        if len(res) == 0:
            return True
        return False
    
    def que_in_db(self, que, card_id):
        cursor = self.connection.cursor()
        sql_user_query = f"SELECT que FROM Ques WHERE que = '{que}' AND card_id = {card_id}"
        cursor.execute(sql_user_query)
        res = cursor.fetchall()
        cursor.close()
        if len(res) == 0:
            return True
        return False
    
    def card_id(self, name, user_id):
        cursor = self.connection.cursor()
        sql_query = f"SELECT card_id FROM Cards WHERE card_name = '{name}' AND user_id = {user_id}"
        cursor.execute(sql_query)
        res = cursor.fetchall()
        id = int(str(res)[2:-3:])
        cursor.close()
        return id
    
    def select_user_cards(self, user_id):
        cursor = self.connection.cursor()
        sql_query = f"SELECT card_id, card_name FROM Cards WHERE user_id = {user_id}"
        cursor.execute(sql_query)
        res = cursor.fetchall()
        return res
    
    def select_que(self, card_id):
        cursor = self.connection.cursor()
        sql_query = f"SELECT que, ans FROM Ques WHERE card_id = {card_id}"
        cursor.execute(sql_query)
        res = cursor.fetchall()
        return res
    
    def card_name(self, id):
        cursor = self.connection.cursor()
        sql_query = f"SELECT card_name FROM Cards WHERE card_id = {id}"
        cursor.execute(sql_query)
        res = cursor.fetchall()
        return res
