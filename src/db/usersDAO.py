from datetime import datetime
from fastapi import Query
from .agent import Agent

class usersDAO:
    def get_user_data_by_token(token):
        agent = Agent()
        query = f"SELECT username,token, last_use_date FROM users WHERE token = '{token}'"
        try:
            result = agent.read(query)
            return result
        except Exception as e:
            print(e)

    def get_user_data_by_username(username):
        agent = Agent()
        query = f"SELECT username,token, last_use_date FROM users WHERE username = '{username}'"
        try:
            result = agent.read(query)
            return result
        except Exception as e:
            print(e)

    def get_user_data_by_username_and_token(username, token):
        agent = Agent()
        query = f"SELECT username,token, last_use_date FROM users WHERE username = '{username}' OR token = '{token}'"
        try:
            result = agent.read(query)
            return result
        except Exception as e:
            print(e)

    
    def update_user_data(username, token):
        agent = Agent()
        query = f"UPDATE users SET token = '{token}', last_use_date = '{datetime.now()}' WHERE username = '{username}'"
        try:
            result = agent.update(query)
            return result
        except Exception as e:
            print(e)

    def update_token_date(token):
        agent = Agent()
        query = f"UPDATE users SET last_use_date = '{datetime.now()}' WHERE token = '{token}'"
        try:
            result = agent.update(query)
            return result
        except Exception as e:
            print(e)

    def create_user(username, token):
        agent = Agent()
        query = f"""INSERT INTO users (username, token, last_use_date) VALUES ('{username}', '{token}', '{datetime.now()}')"""
        try:
            result = agent.create(query)
            return result
        except Exception as e:
            print(e)