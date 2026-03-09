# Flask Calculator

A modern **web-based calculator** built using **Flask, HTML, CSS, and JavaScript**.
The application supports basic arithmetic operations and provides an interactive user experience with features such as keyboard input, calculation history, and dynamic UI behavior.

## Features

- Basic arithmetic operations: addition, subtraction, multiplication, and division
- Keyboard input support
- Dynamic font resizing for long expressions
- AJAX-based calculations (no page reload)
- Calculation history panel
- Clickable history items to reuse previous results
- Clear history option
- Responsive calculator layout
- Operator input validation
- Prevention of invalid decimal numbers
- Secure expression evaluation in the backend

## Tech Stack

Frontend:

- HTML
- CSS
- JavaScript (AJAX, DOM manipulation)

Backend:

- Python
- Flask

Deployment:

- Vercel

## Project Structure

```
flask-calculator/
│
├── app.py
├── requirements.txt
├── vercel.json
│
├── templates/
│   └── index.html
│
└── static/
    └── style.css
```

## Installation

Clone the repository:

```
git clone https://github.com/YOUR_USERNAME/flask-calculator.git
```

Navigate to the project folder:

```
cd flask-calculator
```

Create a virtual environment:

```
python -m venv venv
```

Activate the environment:

Windows

```
venv\Scripts\activate
```

Mac/Linux

```
source venv/bin/activate
```

Install dependencies:

```
pip install -r requirements.txt
```

## Run the Application

Start the Flask server:

```
python app.py
```

Open your browser and go to:

```
http://127.0.0.1:5000
```

## Deployment

This project can be deployed on **Vercel**.

Steps:

1. Push the repository to GitHub.
2. Import the repository in Vercel.
3. Vercel will automatically build and deploy the application.

## Future Improvements

- Scientific calculator functions
- Persistent history using localStorage or database
- Dark/light theme toggle
- Mobile-first UI optimization
- Advanced mathematical operations

## Author

Narendhara Prasath

## License

This project is for educational purposes.
