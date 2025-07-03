document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const taskForm = document.getElementById('task-form');
    const tasksContainer = document.getElementById('tasks-container');
    
    // Loading indicator
    const loadingIndicator = document.createElement('div');
    loadingIndicator.className = 'loading-indicator';
    loadingIndicator.innerHTML = '<div class="spinner"></div>';
    document.body.appendChild(loadingIndicator);
    
    // Add CSS for loading indicator
    const loadingStyles = document.createElement('style');
    loadingStyles.textContent = `
        .loading-indicator {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.5);
            z-index: 1000;
            justify-content: center;
            align-items: center;
        }
        .spinner {
            width: 50px;
            height: 50px;
            border: 5px solid #f3f3f3;
            border-top: 5px solid #3498db;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        #alerts-container {
            position: fixed;
            bottom: 20px;
            left: 20px;
            z-index: 1000;
            display: flex;
            flex-direction: column;
            gap: 10px;
            max-width: 300px;
        }
        .alert {
            padding: 15px;
            border-radius: 5px;
            text-align: left;
            box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2);
            animation: slideIn 0.3s ease-out forwards;
        }
        @keyframes slideIn {
            from {
                transform: translateX(-100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        .alert-success {
            background-color: #d4edda;
            color: #155724;
            border-left: 4px solid #28a745;
        }
        .alert-error {
            background-color: #f8d7da;
            color: #721c24;
            border-left: 4px solid #dc3545;
        }

        .loading-message {
            text-align: center;
            padding: 20px;
            color: #6c757d;
        }
        .error-message {
            text-align: center;
            padding: 30px;
            background-color: #f8d7da;
            color: #721c24;
            border-radius: 8px;
            width: 100%;
        }
        .modal-container {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.5);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 2000;
            animation: fadeIn 0.3s ease-out forwards;
        }
        @keyframes fadeIn {
            from {
                opacity: 0;
            }
            to {
                opacity: 1;
            }
        }
        .modal-content {
            background-color: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
            max-width: 400px;
            width: 90%;
            text-align: center;
            animation: scaleIn 0.3s ease-out forwards;
        }
        @keyframes scaleIn {
            from {
                transform: scale(0.8);
                opacity: 0;
            }
            to {
                transform: scale(1);
                opacity: 1;
            }
        }
        .modal-content p {
            font-size: 18px;
            margin-bottom: 25px;
            color: #333;
        }
        .modal-buttons {
            display: flex;
            justify-content: center;
            gap: 15px;
        }
        .modal-btn {
            padding: 10px 25px;
            border-radius: 4px;
            font-size: 16px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s ease;
            border: none;
        }
        .cancel-btn {
            background-color: #f8f9fa;
            border: 1px solid #6c757d;
            color: #6c757d;
        }
        .cancel-btn:hover {
            background-color: #e9ecef;
        }
        .confirm-btn {
            background-color: #dc3545;
            color: white;
        }
        .confirm-btn:hover {
            background-color: #c82333;
        }
    `;
    document.head.appendChild(loadingStyles);
    
    // Function to show/hide loading indicator
    function showLoading() {
        loadingIndicator.style.display = 'flex';
    }
    
    function hideLoading() {
        loadingIndicator.style.display = 'none';
    }
    
    // Function to show alert messages
    function showAlert(message, type = 'success') {
        // Create alert element
        const alertElement = document.createElement('div');
        alertElement.className = `alert alert-${type}`;
        alertElement.textContent = message;
        
        // Create alerts container if it doesn't exist
        let alertsContainer = document.getElementById('alerts-container');
        if (!alertsContainer) {
            alertsContainer = document.createElement('div');
            alertsContainer.id = 'alerts-container';
            document.body.appendChild(alertsContainer);
        }
        
        // Add to alerts container
        alertsContainer.appendChild(alertElement);
        
        // Remove after 3 seconds
        setTimeout(() => {
            alertElement.remove();
            // Remove container if empty
            if (alertsContainer.children.length === 0) {
                alertsContainer.remove();
            }
        }, 3000);
    }
    
    // Function to show a confirmation modal
    function showConfirmationModal(message, confirmCallback) {
        // Create modal container
        const modalContainer = document.createElement('div');
        modalContainer.className = 'modal-container';
        
        // Create modal content
        const modalContent = document.createElement('div');
        modalContent.className = 'modal-content';
        
        // Create message
        const messageElement = document.createElement('p');
        messageElement.textContent = message;
        modalContent.appendChild(messageElement);
        
        // Create buttons container
        const buttonsContainer = document.createElement('div');
        buttonsContainer.className = 'modal-buttons';
        
        // Function to close modal
        const closeModal = () => {
            document.body.removeChild(modalContainer);
        };
        
        // Create confirm button
        const confirmButton = document.createElement('button');
        confirmButton.className = 'modal-btn confirm-btn';
        confirmButton.textContent = 'Confirm';
        confirmButton.addEventListener('click', () => {
            closeModal();
            confirmCallback();
        });
        
        // Create cancel button
        const cancelButton = document.createElement('button');
        cancelButton.className = 'modal-btn cancel-btn';
        cancelButton.textContent = 'Cancel';
        cancelButton.addEventListener('click', closeModal);
        
        // Add buttons to container
        buttonsContainer.appendChild(cancelButton);
        buttonsContainer.appendChild(confirmButton);
        modalContent.appendChild(buttonsContainer);
        
        // Add modal content to container
        modalContainer.appendChild(modalContent);
        
        // Click outside to close
        modalContainer.addEventListener('click', (e) => {
            if (e.target === modalContainer) {
                closeModal();
            }
        });
        
        // Keyboard support
        const handleKeyDown = (e) => {
            if (e.key === 'Escape') {
                closeModal();
            } else if (e.key === 'Enter') {
                closeModal();
                confirmCallback();
            }
        };
        
        document.addEventListener('keydown', handleKeyDown);
        
        // Clean up event listener when modal is closed
        const removeEventListener = () => {
            document.removeEventListener('keydown', handleKeyDown);
            modalContainer.removeEventListener('transitionend', removeEventListener);
        };
        
        modalContainer.addEventListener('transitionend', removeEventListener);
        
        // Add modal to body
        document.body.appendChild(modalContainer);
        
        // Focus confirm button
        confirmButton.focus();
    }
    
    // API base URL
    const API_BASE_URL = 'http://localhost:3000';
    
    // Fetch all tasks from the server
    function fetchTasks() {
        showLoading();
        
        fetch(`${API_BASE_URL}/api/tasks`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(tasks => {
                hideLoading();
                renderTasks(tasks);
            })
            .catch(error => {
                hideLoading();
                console.error('Error fetching tasks:', error);
                tasksContainer.innerHTML = `
                    <div class="error-message">
                        <p>Failed to load tasks. Please try again later.</p>
                    </div>
                `;
            });
    }
    
    // Render tasks in the DOM
    function renderTasks(tasks) {
        tasksContainer.innerHTML = '';
        
        if (tasks.length === 0) {
            tasksContainer.innerHTML = `
                <div class="loading-message">
                    <p>No tasks found. Add a new task to get started.</p>
                </div>
            `;
            return;
        }
        
        tasks.forEach(task => {
            const taskElement = document.createElement('div');
            taskElement.className = `task-item ${task.completed ? 'completed' : ''}`;
            taskElement.dataset.id = task.id;
            
            taskElement.innerHTML = `
                <div class="task-content">
                    <h3>${task.title}</h3>
                    <p>${task.description}</p>
                </div>
                <div class="task-actions">
                    <button class="done-btn">${task.completed ? 'Undo' : 'Done'}</button>
                    <button class="delete-btn">Delete</button>
                </div>
            `;
            
            // Add event listener to the done button
            const doneButton = taskElement.querySelector('.done-btn');
            doneButton.addEventListener('click', () => {
                toggleTaskCompletion(task.id, !task.completed);
            });
            
            // Add event listener to the delete button
            const deleteButton = taskElement.querySelector('.delete-btn');
            deleteButton.addEventListener('click', () => {
                showConfirmationModal('Are you sure you want to delete this task?', () => {
                    deleteTask(task.id);
                });
            });
            
            tasksContainer.appendChild(taskElement);
        });
    }
    
    // Toggle task completion status
    function toggleTaskCompletion(taskId, completed) {
        showLoading();
        
        fetch(`${API_BASE_URL}/api/tasks/${taskId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ completed })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            hideLoading();
            if (data.success) {
                // Refresh tasks
                fetchTasks();
            } else {
                showAlert(data.message || 'Failed to update task', 'error');
            }
        })
        .catch(error => {
            hideLoading();
            console.error('Error updating task:', error);
            showAlert('An error occurred while updating the task', 'error');
        });
    }
    
    // Add new task
    function addTask(title, description) {
        showLoading();
        
        fetch(`${API_BASE_URL}/api/tasks`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ title, description })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            hideLoading();
            if (data.success) {
                // Reset form
                taskForm.reset();
                
                // Show success message
                showAlert(data.message, 'success');
                
                // Refresh tasks
                fetchTasks();
            } else {
                showAlert(data.message || 'Failed to add task', 'error');
            }
        })
        .catch(error => {
            hideLoading();
            console.error('Error adding task:', error);
            showAlert('An error occurred while adding the task', 'error');
        });
    }
    
    // Event listener for form submission
    if (taskForm) {
        taskForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Get form values
            const title = document.getElementById('title').value.trim();
            const description = document.getElementById('description').value.trim();
            
            // Simple validation
            if (!title || !description) {
                showAlert('Please fill in all fields', 'error');
                return;
            }
            
            // Add task
            addTask(title, description);
        });
    }
    
    // Delete task
    function deleteTask(taskId) {
        showLoading();
        
        fetch(`${API_BASE_URL}/api/tasks/${taskId}`, {
            method: 'DELETE'
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            hideLoading();
            if (data.success) {
                // Show success message
                showAlert(data.message, 'success');
                // Refresh tasks
                fetchTasks();
            } else {
                showAlert(data.message || 'Failed to delete task', 'error');
            }
        })
        .catch(error => {
            hideLoading();
            console.error('Error deleting task:', error);
            showAlert('An error occurred while deleting the task', 'error');
        });
    }
    
    // Initial load of tasks
    fetchTasks();
}); 