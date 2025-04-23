from flask import Flask, render_template, request
from Models import db, Fault
from car_knowledge import CarFaultHybrid
from experta import Fact

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///faults.db'
db.init_app(app)

SYMPTOMS = [
    ('engine_cranks', "🚗 Engine doesn't crank"),
    ('lights_dim', "💡 Dim headlights"),
    ('warning_light', "⚠️ Battery warning light"),
    ('oil_leak', "🛢️ Visible oil leak"),
    ('smoke_exhaust', "💨 Exhaust smoke")
]

@app.route('/')
def index():
    return render_template('index.html', symptoms=SYMPTOMS)

@app.route('/diagnose', methods=['POST'])
def diagnose():
    selected_symptoms = list(request.form.keys())
    print("Selected Symptoms:", selected_symptoms)

    engine = CarFaultHybrid()
    engine.reset()

    for symptom in selected_symptoms:
        engine.declare(Fact(**{symptom: True}))
    engine.declare(Fact(action="diagnose"))
    engine.run()

    faults = []
    for fact in engine.facts.values():
        if isinstance(fact, Fact) and 'fault' in fact:
            fault_data = dict(fact)
            db_fault = Fault.query.filter_by(name=fault_data['fault']).first()
            if db_fault:
                fault_data.update({
                    'repair': db_fault.repair_steps,
                    'difficulty': db_fault.difficulty,
                    'cost': db_fault.cost_estimate,
                    'diagram': db_fault.diagram
                })
            faults.append(fault_data)

    return render_template('result.html', 
        results={
            'faults': faults,
            'certainty': engine.certainty_factors
        }
    )

@app.cli.command("init-db")
def init_db():
    with app.app_context():
        db.create_all()
        faults = [
            Fault(
                name="Dead Battery",
                symptoms=["Engine doesn't crank", "Dim headlights"],
                repair_steps="1. Disconnect terminals\n2. Remove battery\n3. Install new battery",
                difficulty="Easy",
                cost_estimate="₦40,000 - ₦120,000",
                diagram="battery.png"
            ),
            Fault(
                name="Faulty Alternator",
                symptoms=["Battery warning light", "Dim lights while driving"],
                repair_steps="1. Remove serpentine belt\n2. Unbolt alternator\n3. Install new unit",
                difficulty="Medium",
                cost_estimate="₦80,000 - ₦180,000",
                diagram="alternator.png"
            ),
            Fault(
                name="Oil Leak",
                symptoms=["Visible oil puddle", "Low oil level"],
                repair_steps="1. Locate leak source\n2. Replace gasket/seal\n3. Refill oil",
                difficulty="Hard",
                cost_estimate="₦15,000 - ₦40,000",
                diagram="oil-leak.png"
            )
        ]
        db.session.add_all(faults)
        db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)