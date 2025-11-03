# ============================================================
# app.py
# A simple Flask web server to host the AI Bug Detector
# ============================================================

from flask import Flask, request, render_template
from transformers import RobertaTokenizer, T5ForConditionalGeneration
import torch
import os

# --- 1. Initialize Flask App ---
app = Flask(__name__)

# --- 2. Load Model (Load ONCE on startup) ---

# --- THIS IS THE CORRECTED LINE ---
# Use the relative path from your 'ls' command: "my-bug-fixer-model"
model_path = "./my-bug-fixer-model" 
# --- END OF CORRECTION ---

if not os.path.exists(model_path):
    raise FileNotFoundError(f"❌ Cannot find model directory at {model_path}")

print(f"Loading fine-tuned model from: {model_path}")
tokenizer = RobertaTokenizer.from_pretrained(model_path)
model = T5ForConditionalGeneration.from_pretrained(model_path)
print("✅ Model loaded!")

# Determine device
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)
model.eval() # Set model to evaluation mode
print(f"Running on {device.upper()}")

# --- 3. Create the Model Inference Function ---
def get_model_fix(buggy_code):
    """
    Takes a string of buggy code and returns the model's fix.
    """
    try:
        # Prepare input
        input_text = "fix bug: " + buggy_code
        inputs = tokenizer(input_text, return_tensors="pt", truncation=True, padding=True)
        inputs = {k: v.to(device) for k, v in inputs.items()}

        # Generate fix
        with torch.no_grad():
            generated_ids = model.generate(
                **inputs,
                max_length=256,
                num_beams=8,
                do_sample=False,
                early_stopping=True
            )
        
        fixed_code = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
        return fixed_code
    
    except Exception as e:
        print(f"Error during inference: {e}")
        return "Error: Could not generate a fix."

# --- 4. Define Web Page Routes ---

@app.route('/', methods=['GET'])
def index():
    """
    Renders the main page (index.html) when the user first visits.
    """
    # Renders the HTML file from the 'templates' folder
    return render_template('index.html')

@app.route('/fix', methods=['POST'])
def fix_code():
    """
    Called when the user clicks the 'Fix Code' button (submits the form).
    """
    # Get the code from the form's textarea (named 'code_input')
    buggy_code = request.form['code_input']
    
    # Run our model on the code
    fixed_code = get_model_fix(buggy_code)
    
    # Send the results back to the *same* HTML page to be displayed
    return render_template('index.html', 
                           original_code=buggy_code, 
                           fixed_code=fixed_code)

# --- 5. Run the App ---
if __name__ == '__main__':
    # Runs the local web server
    app.run(debug=True, host='127.0.0.1', port=5000)