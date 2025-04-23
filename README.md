# Smart Car Diagnosis 🔧

This project is a web application for diagnosing car faults based on user-reported symptoms. It uses a combination of a rule-based expert system and a machine learning model to identify potential car issues and provide repair guidance.

## Features

- User-friendly web interface to select symptoms.
- Rule-based diagnosis using the Experta knowledge engine.
- Machine learning model trained with decision trees for fault prediction.
- Fault database with repair steps, difficulty, cost estimates, and diagrams.
- SQLite database backend with Flask-SQLAlchemy.
- CLI command to initialize the database with sample fault data.

## Technologies Used

- Python
- Flask
- Flask-SQLAlchemy
- Experta (Expert system framework)
- Pandas
- Scikit-learn
- Joblib

## Setup Instructions

1. Clone the repository.

2. Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

4. Initialize the database with sample data:

```bash
flask init-db
```

5. Run the Flask application:

```bash
python app.py
```

6. Open your browser and navigate to `http://localhost:5000` to use the app.

## Project Structure

- `app.py`: Main Flask application and routes.
- `car_knowledge.py`: Expert system logic using Experta.
- `Models.py`: Database models using Flask-SQLAlchemy.
- `train_model.py`: Script to train the machine learning model.
- `trained_model.pkl`: Serialized trained model.
- `static/`: Static assets like CSS, images, and diagrams.
- `templates/`: HTML templates for the web interface.
- `instance/faults.db`: SQLite database file.

## Contributors

- Greg Tizhe Zirra  
  ID: VUG/SEN/22/8044  
  Email: gregzirra2005@gmail.com  
  GitHub: [Gregzirra-2005](https://github.com/Gregzirra-2005)

- Beno Stephanie Limaro  
  ID: VUG/SEN/22/7328  
  Email: benostephanie16@gmail.com  
  GitHub: [Faro123-sudo](https://github.com/Faro123-sudo)

- Azzuwut Jason Martin  
  ID: VUG/SEN/22/7244  
  Email: martinajason77@gmail.com  
  GitHub: [JasonMartin123](https://github.com/JasonMartin123)

## License

This project is licensed under the MIT License.
