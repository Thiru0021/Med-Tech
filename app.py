from flask import Flask, render_template, request

app = Flask(__name__)

# Dictionary of common OTC medicines
common_medicines = {
    "fever": "Paracetamol",
    "cough": "Cough Syrup (Dextromethorphan)",
    "cold": "Antihistamines (e.g., Chlorpheniramine)",
    "headache": "Ibuprofen or Acetaminophen",
    "stomach pain": "Antacids (e.g., Ranitidine)",
    "nausea": "Antiemetics (e.g., Dimenhydrinate)",
    "allergy": "Antihistamines (e.g., Loratadine or Cetirizine)",
    "body pain": "Aspirin or Ibuprofen",
    "sore throat": "Throat Lozenges (e.g., Benzocaine)",
    "diarrhea": "Oral Rehydration Solution (ORS)",
    "indigestion": "Digestive Enzymes (e.g., Pancreatin)",
    "constipation": "Laxatives (e.g., Bisacodyl or Psyllium Husk)",
    "acid reflux": "Proton Pump Inhibitors (e.g., Omeprazole)",
    "sinus congestion": "Decongestants (e.g., Pseudoephedrine)",
    "back pain": "Naproxen",
    "muscle pain": "Topical Pain Relievers (e.g., Menthol or Capsaicin Cream)",
    "rashes": "Hydrocortisone Cream",
    "eye irritation": "Artificial Tears or Eye Drops",
    "minor cuts and scrapes": "Antibiotic Ointment (e.g., Neosporin)",
    "motion sickness": "Dimenhydrinate (Dramamine)",
    "heartburn": "Antacids (e.g., Calcium Carbonate)",
    "toothache": "Benzocaine Gel or Ibuprofen",
    "sunburn": "Aloe Vera Gel or Hydrocortisone Cream"
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    age = request.form.get('age')  # Get age from form
    gender = request.form.get('gender')  # Get gender from form
    symptoms = request.form.get('symptom')  # Get symptoms from form
    fever_temp = request.form.get('fever_temp')  # Get fever temperature from form

    # Convert age to integer and check if it's 16 or older
    try:
        age = int(age)
    except ValueError:
        return render_template('index.html', warning="Please enter a valid age.")

    if age < 16:
        return render_template('index.html', warning="Sorry, this service is only available for users 16 years and older.")

    # Prepare recommendations based on symptoms
    recommendations = []
    medicine_found = False

    # Split symptoms into a list for easier checking
    symptoms_lower = symptoms.lower().split(',')

    # Loop through all symptoms to check for medicine recommendations
    for symptom in symptoms_lower:
        symptom = symptom.strip()  # Strip any extra spaces
        if symptom in common_medicines:
            recommendations.append(f"Recommended medicine for {symptom}: {common_medicines[symptom]}")
            medicine_found = True

    # If fever or cold is mentioned, show the temperature input
    if 'fever' in symptoms_lower or 'cold' in symptoms_lower:
        if fever_temp:
            recommendations.append(f"Your fever temperature is {fever_temp}°C. If it persists, consult a doctor.")
        elif not fever_temp:
            recommendations.append("You have a fever or cold. Please monitor your temperature and stay hydrated.")

    # If no specific medicine was found, show doctor recommendation
    if not medicine_found:
        recommendations.append("No specific OTC medicine found for the entered symptoms. Please consult a doctor.")

    return render_template('result.html', age=age, gender=gender, symptoms=symptoms, recommendations=recommendations, fever_temp=fever_temp)

if __name__ == '__main__':
    app.run(debug=True)
