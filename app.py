import pickle
import numpy as np
from flask import Flask, request, render_template_string

app = Flask(__name__)

# Load the trained model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

# HTML Template with modern, responsive styling
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Loan Eligibility Prediction</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #4f46e5;
            --primary-hover: #4338ca;
            --bg-color: #f8fafc;
            --card-bg: #ffffff;
            --text-main: #1e293b;
            --text-muted: #64748b;
            --border: #cbd5e1;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Inter', sans-serif;
        }

        body {
            background-color: var(--bg-color);
            color: var(--text-main);
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            background: var(--card-bg);
            max-width: 700px;
            width: 100%;
            padding: 40px;
            border-radius: 16px;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.05);
        }

        h2 {
            font-size: 24px;
            font-weight: 700;
            color: var(--text-main);
            text-align: center;
            margin-bottom: 8px;
        }

        .subtitle {
            text-align: center;
            color: var(--text-muted);
            font-size: 14px;
            margin-bottom: 30px;
        }

        .form-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }

        .form-group {
            display: flex;
            flex-direction: column;
        }

        .form-group.full-width {
            grid-column: span 2;
        }

        label {
            font-size: 13px;
            font-weight: 600;
            margin-bottom: 8px;
            color: var(--text-main);
        }

        input, select {
            padding: 12px 14px;
            border: 1px solid var(--border);
            border-radius: 8px;
            font-size: 14px;
            outline: none;
            transition: all 0.2s ease;
            background-color: #fff;
        }

        input:focus, select:focus {
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.15);
        }

        button {
            grid-column: span 2;
            background-color: var(--primary);
            color: white;
            border: none;
            padding: 14px;
            font-size: 16px;
            font-weight: 600;
            border-radius: 8px;
            cursor: pointer;
            transition: background-color 0.2s;
            margin-top: 10px;
        }

        button:hover {
            background-color: var(--primary-hover);
        }

        .result-card {
            margin-top: 25px;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            font-size: 16px;
            font-weight: 600;
            animation: fadeIn 0.4s ease-in-out;
        }

        .approved {
            background-color: #dcfce7;
            color: #166534;
            border: 1px solid #bbf7d0;
        }

        .rejected {
            background-color: #fee2e2;
            color: #991b1b;
            border: 1px solid #fecaca;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(5px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @media (max-width: 600px) {
            .form-grid {
                grid-template-columns: 1fr;
            }
            .form-group.full-width {
                grid-column: span 1;
            }
            button {
                grid-column: span 1;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Loan Eligibility Checker</h2>
        <p class="subtitle">Fill in your details below to check your loan approval status.</p>
        
        <form method="POST">
            <div class="form-grid">
                <div class="form-group">
                    <label for="gender">Gender</label>
                    <select id="gender" name="gender" required>
                        <option value="1">Male</option>
                        <option value="0">Female</option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="married">Married</label>
                    <select id="married" name="married" required>
                        <option value="1">Yes</option>
                        <option value="0">No</option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="dependents">Dependents</label>
                    <select id="dependents" name="dependents" required>
                        <option value="0">0</option>
                        <option value="1">1</option>
                        <option value="2">2</option>
                        <option value="3">3+</option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="education">Education</label>
                    <select id="education" name="education" required>
                        <option value="0">Graduate</option>
                        <option value="1">Not Graduate</option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="self_employed">Self Employed</label>
                    <select id="self_employed" name="self_employed" required>
                        <option value="1">Yes</option>
                        <option value="0">No</option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="credit_history">Credit History</label>
                    <select id="credit_history" name="credit_history" required>
                        <option value="1.0">Yes (1.0)</option>
                        <option value="0.0">No (0.0)</option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="applicant_income">Applicant Income ($)</label>
                    <input type="number" id="applicant_income" name="applicant_income" placeholder="e.g. 5000" required>
                </div>

                <div class="form-group">
                    <label for="coapplicant_income">Coapplicant Income ($)</label>
                    <input type="number" id="coapplicant_income" name="coapplicant_income" placeholder="e.g. 2000" required>
                </div>

                <div class="form-group">
                    <label for="loan_amount">Loan Amount (in thousands)</label>
                    <input type="number" id="loan_amount" name="loan_amount" placeholder="e.g. 150" required>
                </div>

                <div class="form-group">
                    <label for="loan_amount_term">Loan Term (in months)</label>
                    <input type="number" id="loan_amount_term" name="loan_amount_term" placeholder="e.g. 360" required>
                </div>

                <div class="form-group full-width">
                    <label for="property_area">Property Area</label>
                    <select id="property_area" name="property_area" required>
                        <option value="2">Urban</option>
                        <option value="1">Semiurban</option>
                        <option value="0">Rural</option>
                    </select>
                </div>

                <button type="submit">Predict Eligibility</button>
            </div>
        </form>

        {% if prediction_text %}
            <div class="result-card {{ result_class }}">
                {{ prediction_text }}
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    prediction_text = ""
    result_class = ""
    
    if request.method == 'POST':
        try:
            # Extract form values in exact order of model features
            features = [
                float(request.form['gender']),
                float(request.form['married']),
                float(request.form['dependents']),
                float(request.form['education']),
                float(request.form['self_employed']),
                float(request.form['applicant_income']),
                float(request.form['coapplicant_income']),
                float(request.form['loan_amount']),
                float(request.form['loan_amount_term']),
                float(request.form['credit_history']),
                float(request.form['property_area'])
            ]
            
            # Reshape for prediction
            final_features = np.array([features])
            prediction = model.predict(final_features)
            
            # Interpret output (assuming 1 = Approved, 0 = Rejected)
            if prediction[0] == 1 or prediction[0] == 'Y':
                prediction_text = "Congratulations! Your Loan Application is Approved."
                result_class = "approved"
            else:
                prediction_text = "We're sorry. Your Loan Application is Rejected."
                result_class = "rejected"
                
        except Exception as e:
            prediction_text = f"Error in processing input: {str(e)}"
            result_class = "rejected"

    return render_template_string(HTML_TEMPLATE, prediction_text=prediction_text, result_class=result_class)

if __name__ == '__main__':
    app.run(debug=True)
