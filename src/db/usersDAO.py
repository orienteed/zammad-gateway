from .agent import Agent
from datetime import datetime
from logs.setup import logger
import threading

lock = threading.Lock()


class usersDAO:
    def get_user_data_by_token(token):
        try:
            lock.acquire(True)
            agent = Agent()
            query = f"SELECT username, token, last_use_date, id FROM users WHERE token = '{token}'"
            try:
                return agent.read(query)
            except Exception:
                logger.info("ERROR_DB   - [" + str(datetime.now()) + "]: " + "get_user_data_by_token", exc_info=1)
        finally:
            lock.release()

    def get_user_data_by_username(username):
        try:
            lock.acquire(True)
            agent = Agent()
            query = f"SELECT username,token, last_use_date FROM users WHERE username = '{username}'"
            try:
                return agent.read(query)
            except Exception:
                logger.info("ERROR_DB   - [" + str(datetime.now()) + "]: " + "get_user_data_by_username", exc_info=1)
        finally:
            lock.release()

    def update_user_data(username, token):
        try:
            lock.acquire(True)
            agent = Agent()
            query = f"UPDATE users SET token = '{token}', last_use_date = '{datetime.now()}' WHERE username = '{username}'"
            try:
                return agent.update(query)
            except Exception:
                logger.info("ERROR_DB   - [" + str(datetime.now()) + "]: " + "update_user_data", exc_info=1)
        finally:
            lock.release()

    def update_token_date(token):
        try:
            lock.acquire(True)
            agent = Agent()
            query = f"UPDATE users SET last_use_date = '{datetime.now()}' WHERE token = '{token}'"
            try:
                return agent.update(query)
            except Exception:
                logger.info("ERROR_DB   - [" + str(datetime.now()) + "]: " + "update_token_date", exc_info=1)
        finally:
            lock.release()

    def create_user(username, token, zammad_id):
        try:
            lock.acquire(True)
            agent = Agent()
            query = (
                f"INSERT INTO users (id, username, token, last_use_date) VALUES ('{zammad_id}','{username}', '{token}', '{datetime.now()}')"
            )
            try:
                return agent.create(query)
            except Exception:
                logger.info("ERROR_DB   - [" + str(datetime.now()) + "]: " + "create_user", exc_info=1)
        finally:
            lock.release()

    def remove_token_by_token(token):
        try:
            lock.acquire(True)
            agent = Agent()
            query = f"UPDATE users SET token = '' WHERE token = '{token}'"
            try:
                return agent.update(query)
            except Exception:
                logger.info("ERROR_DB   - [" + str(datetime.now()) + "]: " + "remove_token_by_token", exc_info=1)
        finally:
            lock.release()
