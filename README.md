# **SaleApp-E-commerce Web Application**

### Overview

SaleApp is a professional e-commerce platform built with Flask Python, SQLAlchemy, MySql database, and modern web technologies. This application provides comprehensive product management, shopping cart functionality, user authentication, and admin capabilities.

### Features
- User authentication and registration
- Product browsing and searching 
- Shopping cart and checkout process
- Admin dashboard for product and user management
- Responsive design for mobile and desktop users

### Tech Stack
- Backend: Flask(Python)
- Database: MySQL
- Frontend: HTML, CSS, JavaScript
- CSS Framework: Bootstrap 4
- Authentication: Flask-login

### Getting Started

#### Prerequisites
- Python 3.12+
- MySQL 5.7+
- pip

#### Installation
1. **Clone the repository** 
```bash
git clone https://github.com/conbopk/SaleApp.git
cd SaleApp
```
2.**Create and active virtual environment**
```bash
python -m venv .venv
# On Windowns
.venv\Scripts\activate
# On macOS/Linux
source .venv/bin/activate
```
3.**Install dependencies**
```bash
pip install -r requirements.txt
```
4.**Set up environment variables** Create a `.env` file in the project root with the following variables:
```text
FLASK_APP=SaleApp
FLASK_ENV=development
SECRET_KEY=your_secret_key
DATABASE_URI=//username:password@localhost/saleapp
API_KEY=your_api_key
```
5.**Initialize the database**
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```
6.**Run the application**
```bash
flask run
or 
python index.py
```
The application will be available at http://127.0.0.1:5000/

### Contributing 
1. Fork the repository
2. Create your feature branch 
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

### Licence
This project is licensed under the [MIT License](LICENSE)






