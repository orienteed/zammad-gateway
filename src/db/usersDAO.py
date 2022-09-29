from datetime import datetime
from fastapi import Query
from .agent import Agent
from logs.setup import logger


class usersDAO:
    def get_user_data_by_token(token):
        agent = Agent()
        query = f"SELECT username, token, last_use_date, id FROM users WHERE token = '{token}'"
        try:
            return agent.read(query)
        except Exception as e:
            logger.info("ERROR_DB   - [" + str(datetime.now()) + "]: " + "get_user_data_by_token", exc_info=1)

    def get_user_data_by_username(username):
        agent = Agent()
        query = f"SELECT username,token, last_use_date FROM users WHERE username = '{username}'"
        try:
            return agent.read(query)
        except Exception as e:
            logger.info("ERROR_DB   - [" + str(datetime.now()) + "]: " + "get_user_data_by_username", exc_info=1)

    def get_user_data_by_username_and_token(username, token):
        agent = Agent()
        query = f"SELECT username,token, last_use_date FROM users WHERE username = '{username}' OR token = '{token}'"
        try:
            return agent.read(query)
        except Exception as e:
            logger.info("ERROR_DB   - [" + str(datetime.now()) + "]: " + "get_user_data_by_username_and_token", exc_info=1)

    def update_user_data(username, token):
        agent = Agent()
        query = f"UPDATE users SET token = '{token}', last_use_date = '{datetime.now()}' WHERE username = '{username}'"
        try:
            return agent.update(query)
        except Exception as e:
            logger.info("ERROR_DB   - [" + str(datetime.now()) + "]: " + "update_user_data", exc_info=1)

    def update_token_date(token):
        agent = Agent()
        query = f"UPDATE users SET last_use_date = '{datetime.now()}' WHERE token = '{token}'"
        try:
            return agent.update(query)
        except Exception as e:
            logger.info("ERROR_DB   - [" + str(datetime.now()) + "]: " + "update_token_date", exc_info=1)

    def create_user(username, token, zammad_id):
        agent = Agent()
        query = f"INSERT INTO users (id, username, token, last_use_date) VALUES ('{zammad_id}','{username}', '{token}', '{datetime.now()}')"
        try:
            return agent.create(query)
        except Exception as e:
            logger.info("ERROR_DB   - [" + str(datetime.now()) + "]: " + "create_user", exc_info=1)

    def remove_token_by_token(token):
        agent = Agent()
        query = f"UPDATE users SET token = '' WHERE token = '{token}'"
        try:
            return agent.update(query)
        except Exception as e:
            logger.info("ERROR_DB   - [" + str(datetime.now()) + "]: " + "remove_token_by_token", exc_info=1)
