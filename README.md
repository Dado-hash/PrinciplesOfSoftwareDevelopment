
# FreshTrackProject

## Description

**FreshTrackProject** is a web application for managing users' pantry and shopping lists. It allows you to keep track of pantry items, create and manage shopping lists, and monitor expiration dates of food items.

## Features

- **Pantry Management**: Add, edit, and remove items in the pantry.
- **Shopping Lists**: Create and manage custom shopping lists.
- **Expiration Notifications**: Receive alerts for items nearing expiration.
- **Responsive Interface**: A modern, responsive user interface built with Tailwind CSS.

## Technologies Used

- **Backend**: Django
- **Frontend**: HTML, CSS (Tailwind CSS), JavaScript
- **Database**: SQLite
- **Package Management**: Node.js for frontend dependencies

## Requirements

- Python 3.x
- Django 3.x
- Node.js
- npm (Node Package Manager)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/freshtrackproject.git
   cd freshtrackproject
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Node.js dependencies:**
   ```bash
   cd frontend
   npm install
   cd ..
   ```

5. **Apply database migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

## Usage

1. **Access the application:**
   Open your browser and go to `http://127.0.0.1:8000`.

2. **Admin:**
   Access the Django admin site at `http://127.0.0.1:8000/admin` to manually manage items and lists.

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the project.
2. Create a new branch (`git checkout -b feature/new-feature`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature/new-feature`).
5. Open a Pull Request.
