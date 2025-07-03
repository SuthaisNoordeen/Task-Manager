# Task-Manager

A modern task management application built with Python and MySQL.

## Features

- Add new tasks with title and description
- Mark tasks as completed
- Delete tasks
- Modern and responsive UI
- Real-time updates
- Local MySQL database storage

## Tech Stack

- **Backend**: Python 3.10+
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: MySQL
- **UI Framework**: Custom CSS with Poppins font

## Prerequisites

1. Python 3.10 or higher
2. MySQL Server
3. Required Python packages:
   - mysql-connector-python
   - requests
   - protobuf

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/SuthaisNoordeen/Task-Manager.git
   cd Task-Manager
   ```

2. Install Python dependencies:
   ```bash
   pip install -r server/requirements.txt
   ```

3. Set up MySQL:
   - Install MySQL Server
   - Create a database named 'task_manager'
   - Ensure MySQL is running on default port (3306)

4. Start the application:
   ```bash
   cd server
   python server.py
   ```

5. Open your browser and navigate to:
   http://localhost:3000

## Usage

1. Add a new task:
   - Fill in the title and description
   - Click "Add Task"

2. Mark a task as completed:
   - Click the "Done" button next to a task
   - Click "Undo" to mark it as incomplete

3. Delete a task:
   - Click the "Delete" button
   - Confirm deletion in the popup

## Project Structure

```
Task-Manager/
├── client/
│   ├── css/
│   │   └── styles.css
│   ├── js/
│   │   └── script.js
│   └── index.html
└── server/
    ├── server.py
    ├── requirements.txt
    └── db_test.py
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Thanks to the Python and MySQL communities
- Special thanks to the developers of the Poppins font
- Inspired by modern task management applications
