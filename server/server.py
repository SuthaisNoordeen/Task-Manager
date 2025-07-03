import http.server
import socketserver
import json
import mysql.connector
import urllib.parse
import os
import sys
import functools
from pathlib import Path
from datetime import datetime

# Custom JSON encoder to handle datetime objects
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Default phpMyAdmin password is empty
    'database': 'task_manager'
}

# Server port
PORT = 3000

# Create database and tables if they don't exist
def setup_database():
    try:
        # First connect without specifying database to create it if it doesn't exist
        conn = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        cursor = conn.cursor()
        
        # Create database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
        cursor.execute(f"USE {DB_CONFIG['database']}")
        
        # Create tasks table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(100) NOT NULL,
            description TEXT NOT NULL,
            completed BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Insert default tasks if the table is empty
        cursor.execute("SELECT COUNT(*) FROM tasks")
        count = cursor.fetchone()[0]
        
        if count == 0:
            default_tasks = [
                ('Buy books', 'Buy books for the next school year', False),
                ('Clean home', 'Need to clean the bed room', False),
                ('Takehome assignment', 'Finish the mid-term assignment', False),
                ('Play Cricket', 'Plan the soft ball cricket match on next Sunday', False),
                ('Help Saman', 'Saman need help with his software project', False)
            ]
            
            for task in default_tasks:
                cursor.execute("""
                INSERT INTO tasks (title, description, completed)
                VALUES (%s, %s, %s)
                """, task)
        
        conn.commit()
        print("Database and tables created successfully")
        return True
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

# Get database connection
def get_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return None

# Custom request handler
class RequestHandler(http.server.SimpleHTTPRequestHandler):
    
    # Add CORS headers to all responses
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    # Handle GET requests
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        
        # API endpoints
        if path == '/api/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'status': 'OK', 'message': 'Server is running'}
            self.wfile.write(json.dumps(response, cls=DateTimeEncoder).encode())
            
        elif path == '/api/tasks':
            self.get_tasks()
            
        else:
            # Serve static files
            return http.server.SimpleHTTPRequestHandler.do_GET(self)
    
    # Handle POST requests
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        if self.path == '/api/tasks':
            try:
                data = json.loads(post_data.decode('utf-8'))
                self.add_task(data)
            except json.JSONDecodeError:
                self.send_error(400, 'Invalid JSON data')
        else:
            self.send_error(404, 'Endpoint not found')
    
    # Handle PUT requests
    def do_PUT(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        
        if path.startswith('/api/tasks/'):
            try:
                task_id = int(path.split('/')[-1])
                content_length = int(self.headers['Content-Length'])
                put_data = self.rfile.read(content_length)
                data = json.loads(put_data.decode('utf-8'))
                self.update_task(task_id, data)
            except (ValueError, json.JSONDecodeError):
                self.send_error(400, 'Invalid request')
        else:
            self.send_error(404, 'Endpoint not found')
    
    # Handle OPTIONS requests (for CORS preflight)
    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()
    
    # Handle DELETE requests
    def do_DELETE(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        
        if path.startswith('/api/tasks/'):
            try:
                task_id = int(path.split('/')[-1])
                self.delete_task(task_id)
            except ValueError:
                self.send_error(400, 'Invalid task ID')
        else:
            self.send_error(404, 'Endpoint not found')
    
    # Get all tasks
    def get_tasks(self):
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT * FROM tasks ORDER BY created_at DESC")
                tasks = cursor.fetchall()
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(tasks, cls=DateTimeEncoder).encode())
            except mysql.connector.Error as err:
                print(f"Database error: {err}")
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {'success': False, 'message': 'Database error'}
                self.wfile.write(json.dumps(response, cls=DateTimeEncoder).encode())
            finally:
                cursor.close()
                conn.close()
        else:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'success': False, 'message': 'Database connection error'}
            self.wfile.write(json.dumps(response, cls=DateTimeEncoder).encode())
    
    # Add a new task
    def add_task(self, data):
        title = data.get('title', '').strip()
        description = data.get('description', '').strip()
        
        # Basic validation
        if not title or not description:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'success': False, 'message': 'Title and description are required'}
            self.wfile.write(json.dumps(response, cls=DateTimeEncoder).encode())
            return
        
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                INSERT INTO tasks (title, description)
                VALUES (%s, %s)
                """, (title, description))
                conn.commit()
                
                # Get the inserted task with ID
                task_id = cursor.lastrowid
                cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
                task = cursor.fetchone()
                
                self.send_response(201)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                
                # Convert task tuple to dictionary
                task_dict = {
                    'id': task[0],
                    'title': task[1],
                    'description': task[2],
                    'completed': bool(task[3]),
                    'created_at': task[4]
                }
                
                response = {'success': True, 'message': 'Task added successfully', 'task': task_dict}
                self.wfile.write(json.dumps(response, cls=DateTimeEncoder).encode())
            except mysql.connector.Error as err:
                print(f"Database error: {err}")
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {'success': False, 'message': 'An error occurred while adding the task'}
                self.wfile.write(json.dumps(response, cls=DateTimeEncoder).encode())
            finally:
                cursor.close()
                conn.close()
        else:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'success': False, 'message': 'Database connection error'}
            self.wfile.write(json.dumps(response, cls=DateTimeEncoder).encode())
    
    # Update a task
    def update_task(self, task_id, data):
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                
                # Check if task exists
                cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
                task = cursor.fetchone()
                
                if not task:
                    self.send_response(404)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    response = {'success': False, 'message': 'Task not found'}
                    self.wfile.write(json.dumps(response, cls=DateTimeEncoder).encode())
                    return
                
                # Update the task
                updates = []
                params = []
                
                if 'title' in data:
                    updates.append("title = %s")
                    params.append(data['title'])
                
                if 'description' in data:
                    updates.append("description = %s")
                    params.append(data['description'])
                
                if 'completed' in data:
                    updates.append("completed = %s")
                    params.append(data['completed'])
                
                if not updates:
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    response = {'success': False, 'message': 'No fields to update'}
                    self.wfile.write(json.dumps(response, cls=DateTimeEncoder).encode())
                    return
                
                query = f"UPDATE tasks SET {', '.join(updates)} WHERE id = %s"
                params.append(task_id)
                
                cursor.execute(query, tuple(params))
                conn.commit()
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {'success': True, 'message': 'Task updated successfully'}
                self.wfile.write(json.dumps(response, cls=DateTimeEncoder).encode())
            except mysql.connector.Error as err:
                print(f"Database error: {err}")
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {'success': False, 'message': 'An error occurred while updating the task'}
                self.wfile.write(json.dumps(response, cls=DateTimeEncoder).encode())
            finally:
                cursor.close()
                conn.close()
        else:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'success': False, 'message': 'Database connection error'}
            self.wfile.write(json.dumps(response, cls=DateTimeEncoder).encode())
    
    # Delete a task
    def delete_task(self, task_id):
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                
                # Check if task exists
                cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
                task = cursor.fetchone()
                
                if not task:
                    self.send_response(404)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    response = {'success': False, 'message': 'Task not found'}
                    self.wfile.write(json.dumps(response, cls=DateTimeEncoder).encode())
                    return
                
                # Delete the task
                cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
                conn.commit()
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {'success': True, 'message': 'Task deleted successfully'}
                self.wfile.write(json.dumps(response, cls=DateTimeEncoder).encode())
            except mysql.connector.Error as err:
                print(f"Database error: {err}")
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {'success': False, 'message': 'An error occurred while deleting the task'}
                self.wfile.write(json.dumps(response, cls=DateTimeEncoder).encode())
            finally:
                cursor.close()
                conn.close()
        else:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {'success': False, 'message': 'Database connection error'}
            self.wfile.write(json.dumps(response, cls=DateTimeEncoder).encode())

def run_server():
    # Setup database first
    if not setup_database():
        print("Failed to set up database. Exiting...")
        sys.exit(1)
    
    # Create server
    current_dir = Path(__file__).parent.parent
    client_dir = os.path.join(current_dir, 'client')
    handler = functools.partial(RequestHandler, directory=client_dir)
    httpd = socketserver.TCPServer(("", PORT), handler)
    
    print(f"Server running at http://localhost:{PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print("Server stopped")

if __name__ == "__main__":
    run_server() 