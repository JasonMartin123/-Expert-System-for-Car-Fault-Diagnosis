from experta import *
import joblib
import pandas as pd

class CarFaultHybrid(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.certainty_factors = {}
        self.feature_names = [
            'engine_cranks', 'lights_dim', 'warning_light',
            'oil_leak', 'smoke_exhaust'
        ]
        self.dt_model = joblib.load("trained_model.pkl")
        
        self.repair_db = {
            "Dead Battery": {
                "symptoms": ["Engine doesn't crank", "Dim headlights"],
                "repair": "Replace battery",
                "difficulty": "Easy",
                "cost": "$100-$200",
                "diagram": "battery.png"
            },
            "Faulty Alternator": {
                "symptoms": ["Battery warning light", "Dim lights while driving"],
                "repair": "Replace alternator",
                "difficulty": "Medium",
                "cost": "$300-$500",
                "diagram": "alternator.png"
            },
            "Oil Leak": {
                "symptoms": ["Visible oil puddle", "Low oil level"],
                "repair": "Fix gasket/seal",
                "difficulty": "Hard",
                "cost": "$200-$800",
                "diagram": "oil-leak.png"
            }
        }

    def dt_predict(self, symptoms):
        input_data = [1 if symptom in symptoms else 0 
                      for symptom in self.feature_names]
        df = pd.DataFrame([input_data], columns=self.feature_names)
        return self.dt_model.predict(df)[0], self.dt_model.predict_proba(df)[0].max()

    @DefFacts()
    def _initial_facts(self):
        yield Fact(action="diagnose")

    @Rule(Fact(action='diagnose'), salience=1)
    def hybrid_diagnosis(self):
        active_symptoms = [
            list(fact.keys())[0] 
            for fact in self.facts.values() 
            if isinstance(fact, Fact) and 'action' not in fact
        ]
        dt_fault, dt_prob = self.dt_predict(active_symptoms)
        self.declare(Fact(dt_priority_fault=dt_fault))
        self.certainty_factors[dt_fault] = dt_prob

    # Rules for different faults
    @Rule(
        Fact(action='diagnose'),
        OR(
            Fact(dt_priority_fault='Dead Battery'),
            AND(
                Fact(engine_cranks=True),  # Changed to True
                Fact(lights_dim=True)
            )
        )
    )
    def dead_battery(self):
        self._declare_fault("Dead Battery")

    @Rule(
        Fact(action='diagnose'),
        OR(
            Fact(dt_priority_fault='Faulty Alternator'),
            AND(
                Fact(warning_light=True),
                Fact(lights_dim=True)
            )
        )
    )
    def alternator_fault(self):
        self._declare_fault("Faulty Alternator")

    @Rule(
        Fact(action='diagnose'),
        OR(
            Fact(dt_priority_fault='Oil Leak'),
            AND(
                Fact(oil_leak=True),
                Fact(smoke_exhaust=True)
            )
        )
    )
    def oil_leak(self):
        self._declare_fault("Oil Leak")

    def _declare_fault(self, fault_name):
        fault_data = self.repair_db[fault_name]
        self.declare(Fact(
            fault=fault_name,
            symptoms=fault_data["symptoms"],
            repair=fault_data["repair"],
            difficulty=fault_data["difficulty"],
            cost=fault_data["cost"],
            diagram=fault_data["diagram"]
        ))
        self.certainty_factors[fault_name] = min(
            1.0, self.certainty_factors.get(fault_name, 0) + 0.2
        )