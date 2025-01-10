from flask import Flask, render_template, request

app = Flask(__name__)

# Conditions and their symptoms
conditions = {
    "Flu": ["fever", "cough", "body ache", "fatigue", "headache", "chills"],
    "Covid-19": ["fever", "cough", "fatigue", "shortness of breath", "loss of taste", "loss of smell"],
    "Viral Infection": ["fatigue", "fever", "headache", "body ache", "cough", "sore throat"],
    "Allergy": ["sneezing", "runny nose", "itchy eyes", "skin rash"],
    "Stomach Bug": ["nausea", "vomiting", "diarrhea", "abdominal pain"],
}

# Implementing a basic Stack and Queue
class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop() if self.items else None

    def is_empty(self):
        return len(self.items) == 0


class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        return self.items.pop(0) if self.items else None

    def is_empty(self):
        return len(self.items) == 0


@app.route('/')
def index():
    # Pass all symptoms to the index.html template
    all_symptoms = list({symptom for symptoms in conditions.values() for symptom in symptoms})
    return render_template('index.html', symptoms=all_symptoms)


@app.route('/diagnose', methods=['POST'])
def diagnose():
    # Get the symptoms selected by the user
    user_symptoms = set(request.form.getlist('symptoms-selector'))

    # Using Queue for symptoms processing and Stack for conditions
    symptom_queue = Queue()
    for symptom in user_symptoms:
        symptom_queue.enqueue(symptom)

    condition_stack = Stack()
    condition_matches = {}

    # Process symptoms using Queue
    while not symptom_queue.is_empty():
        symptom = symptom_queue.dequeue()
        for condition_name, condition_symptoms in conditions.items():
            if symptom in condition_symptoms:
                if condition_name not in condition_matches:
                    condition_stack.push(condition_name)
                    condition_matches[condition_name] = 0
                condition_matches[condition_name] += 1

    # Determine the most likely condition using Stack
    most_likely_condition = None
    max_matches = 0
    while not condition_stack.is_empty():
        condition_name = condition_stack.pop()
        if condition_matches[condition_name] > max_matches:
            most_likely_condition = condition_name
            max_matches = condition_matches[condition_name]

    # Diagnosis result
    if most_likely_condition:
        diagnosis = f"The most likely condition is: {most_likely_condition}"
        condition_info = {
            "Flu": {
                "precautions": ["Get plenty of rest 🛌", "Stay hydrated 💧"],
                "medicines": ["Paracetamol", "Ibuprofen"]
            },
            "Covid-19": {
                "precautions": ["Stay home 🏠", "Wear a mask 😷", "Avoid crowds"],
                "medicines": ["Paracetamol", "Vitamin C"]
            },
            "Viral Infection": {
                "precautions": ["Stay hydrated 💧", "Rest well 🛌"],
                "medicines": ["Ibuprofen", "Antiviral medications"]
            },
            "Allergy": {
                "precautions": ["Avoid allergens 🚫", "Use antihistamines"],
                "medicines": ["Cetirizine", "Loratadine"]
            },
            "Stomach Bug": {
                "precautions": ["Stay hydrated 💧", "Eat bland foods 🍞"],
                "medicines": ["Oral rehydration salts (ORS)", "Antidiarrheal medication"]
            },
        }
        precautions = condition_info.get(most_likely_condition, {}).get("precautions", [])
        medicines = condition_info.get(most_likely_condition, {}).get("medicines", [])
    else:
        diagnosis = "Unable to determine a condition based on the symptoms provided."
        precautions = []
        medicines = []

    return render_template('result.html', diagnosis=diagnosis, precautions=precautions, medicines=medicines)


if __name__ == '__main__':
    app.run(debug=True)
