## URL Shortener(Django) 
 A URL shortener web application built with Django. Authenticated users can create, manage, and track short URLs.


## Features

- User registration, login, logout
- Authenticated URL creation and management
- Automatic short URL generation
- Custom short URLs
- URL redirection
- Click count analytics
- Expiration time support
- QR code generation Features

## Tech Stack


- Python
- Django
- Postgresql
- HTML / Django Templates

## Setup Instructions

### 1. Clone the repository
  git clone https://github.com/suryasaud10/URL-Shortener.git
  cd URL-Shortener
  python -m venv myvenv
  ./myvenv/Scripts/activate    
  pip install Django
  python manage.py makemigrations
  python manage.py migrate
  python manage.py migrate

Open: http://127.0.0.1:8000/



## Usage

  Register or log in
  Create a short URL from a long URL
  Optionally create a custom short URL
  View, edit, or delete URLs from dashboard
  Track click count
  Generate QR codes
  Expired URLs automatically stop redirecting

## Project Structure
 
 URLSHORTENER/              
├── myvenv/                 
└── urlshortener/           
    ├── manage.py           
    ├── db.sqlite3          
    ├── README.md           
    ├── requirements.txt    
    ├── static/            
    ├── urlshortener/       
    │   ├── __init__.py
    │   ├── settings.py     
    │   ├── urls.py         
    │   └── wsgi.py         
    └── shortener/          
        ├── migrations/     
        ├── __init__.py
        ├── admin.py        
        ├── apps.py        
        ├── models.py       
        ├── tests.py        
        ├── urls.py         
        └── views.py        







