# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from streamlit.logger import get_logger
import sqlite3

LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="Hello",
        page_icon="👋",
    )

    # Create or connect to SQLite database
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()

    # Create table if not exists
    c.execute('''
          CREATE TABLE IF NOT EXISTS todo (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              task TEXT NOT NULL
          )
          ''')
    conn.commit()

    def add_task(task):
        c.execute('INSERT INTO todo (task) VALUES (?)', (task,))
        conn.commit()

    def get_tasks():
        c.execute('SELECT * FROM todo')
        tasks = c.fetchall()
        return tasks

    def edit_task(task_id, new_task):
        c.execute('UPDATE todo SET task=? WHERE id=?', (new_task, task_id))
        conn.commit()

    def del_task(task_id):
        c.execute('DELETE todo WHERE id=?', (task_id))
        conn.commit()

    # Streamlit app
    st.title('To-Do List App')

    # List tasks
    tasks = get_tasks()
    if tasks:
        st.write('### Current Tasks:')
        for task in tasks:
            st.write(f"{task[0]}. {task[1]}")

    
    # Add task
    new_task = st.text_input('Add a new task:')
    if st.button('Add Task'):
        if new_task:
            add_task(new_task)
            st.success('Task added successfully!')
        else:
            st.warning('Please enter a task.')



    # Edit task
    task_id_to_edit = st.text_input('Enter the task ID to edit:')
    new_task_content = st.text_input('Enter the new task content:')
    if st.button('Edit Task'):
        if task_id_to_edit and new_task_content:
            edit_task(int(task_id_to_edit), new_task_content)
            st.success('Task edited successfully!')
        else:
            st.warning('Please enter both task ID and new task content.')

    # Delete task
    task_id_to_delete = st.text_input('Enter the task ID to delete:')
    if st.button('Delete Task'):
        if task_id_to_delete:
            del_task(int(task_id_to_delete))
            st.success('Task deleted successfully!')
        else:
            st.warning('Please enter task ID to delete.')
    
    # Close the connection
    conn.close()

    #)


if __name__ == "__main__":
    run()
