import streamlit as st
import sqlite3
import pickle
from datetime import datetime

# ---------- Database Setup ----------
DB_NAME = "game_story_database.db"
#DB_NAME = "game_story_memory_temp1.db"

def init_db():
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS chats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_name TEXT UNIQUE,
                input_blob BLOB,
                output_blob BLOB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error while initializing DB: {e}")
    except Exception as e:
        print(f"Unexpected error while initializing DB: {e}")
    finally:
        try:
            conn.close()
        except:
            pass

def save_chat_to_db(chat_name, input_obj, output_obj):
    try:
        # Serialize the objects first
        try:
            input_blob = pickle.dumps(input_obj)
            output_blob = pickle.dumps(output_obj)
        except (pickle.PicklingError, TypeError) as e:
            print(f"Error pickling objects for chat '{chat_name}': {e}")
            return

        # Connect to DB and insert data
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute(
            "INSERT INTO chats (chat_name, input_blob, output_blob) VALUES (?, ?, ?)",
            (chat_name, input_blob, output_blob)
        )
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error while saving chat '{chat_name}': {e}")
    except Exception as e:
        print(f"Unexpected error while saving chat '{chat_name}': {e}")
    finally:
        try:
            conn.close()
        except:
            pass

def get_all_chats_from_db():
    try:
        # Use 'with' to ensure the connection is closed automatically
        with sqlite3.connect(DB_NAME) as conn:
            c = conn.cursor()
            c.execute("SELECT chat_name FROM chats ORDER BY created_at DESC")
            chats = [row[0] for row in c.fetchall()]  # List of chat names
        return chats
    except sqlite3.DatabaseError as e:
        # Log the error and handle it appropriately
        print(f"Database error: {e}")
        return []
    except Exception as e:
        # Log the generic error and handle it appropriately
        print(f"Error: {e}")
        return []

def load_chat_from_db(chat_name):
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT input_blob, output_blob FROM chats WHERE chat_name = ?", (chat_name,))
        row = c.fetchone()
        if row:
            try:
                input_data = pickle.loads(row[0])
                output_data = pickle.loads(row[1])
                return input_data, output_data
            except (pickle.UnpicklingError, EOFError) as e:
                print(f"Error unpickling data for chat '{chat_name}': {e}")
                return None, None
        return None, None
    except sqlite3.Error as e:
        print(f"Database error while loading chat '{chat_name}': {e}")
        return None, None
    except Exception as e:
        print(f"Unexpected error while loading chat '{chat_name}': {e}")
        return None, None
    finally:
        try:
            conn.close()
        except:
            pass