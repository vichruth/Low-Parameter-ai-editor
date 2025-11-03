# ============================================================
# test_my_model.py
# Run inference on the fine-tuned Low-Parameter AI Bug Detector
# ============================================================

from transformers import RobertaTokenizer, T5ForConditionalGeneration
import torch, os

# --- 1. Load model ---
model_path = "/home/vichruth/ml_projects/bug_recommender/lowparam-bugfixer-model1"
if not os.path.exists(model_path):
    raise FileNotFoundError(f"❌ Model path not found: {model_path}")

print(f"Loading fine-tuned model from: {model_path}")
tokenizer = RobertaTokenizer.from_pretrained(model_path)
model = T5ForConditionalGeneration.from_pretrained(model_path)
print("✅ Model loaded!")

# --- 2. Buggy code sample ---
buggy_code = """
def bitcount(n):
    count = 0
    while n:
        n ^= n - 1  # <-- Bug is here (should be &=)
        count += 1
    return count
"""

# --- 3. Prepare input ---
input_text = "fix bug: " + buggy_code
inputs = tokenizer(input_text, return_tensors="pt", truncation=True, padding=True)

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)
inputs = {k: v.to(device) for k, v in inputs.items()}
print(f"Running on {device.upper()}")

# --- 4. Generate fix ---
with torch.no_grad():
    generated_ids = model.generate(
    **inputs,
    max_length=256,
    num_beams=8,
    do_sample=False,
    early_stopping=True
)

fixed_code = tokenizer.decode(generated_ids[0], skip_special_tokens=True)

# --- 5. Show results ---
print("\n--- Output (Fixed Code) ---")
print(fixed_code)

if "n &= n - 1" in fixed_code.replace(" ", ""):
    print("\n✅ Fix appears correct!")
else:
    print("\n⚠️ Fix might not be correct; check output manually.")
