# 🤖 Low-Parameter AI Bug Detector

This project is a lightweight, offline-first AI system designed to detect bugs in Python code and suggest fixes. It is based on the research paper "Low-Parameter AI Bug Detector: Offline Code Debugging and Complexity-Aware Optimization for Resource-Constrained Devices."

The core of the project is a `Salesforce/codet5-base` model fine-tuned on a 2000-example dataset of Python bug-fix pairs. The model is deployed in a simple local web application using Flask, allowing it to run entirely on a user's machine (laptop or smartphone) without an internet connection.

## ✨ Features

* **Offline First:** Runs 100% locally. No internet connection or cloud GPU is required for inference.
* **AI-Powered Bug Fixing:** Uses a fine-tuned CodeT5 model to analyze buggy code and generate a corrected version.
* **Lightweight:** By using a `base` model (and supporting LoRA), the system is designed to run on resource-constrained devices.
* **Simple Web Interface:** A basic Flask + HTML app provides an easy-to-use interface for pasting code and seeing results.

## 🔧 How It Works

1.  **Model Training:** A `codet5-base` model was fine-tuned in Google Colab on a `.jsonl` dataset containing 2,000 Python bug/fix pairs. The final trained model (adapters and tokenizer) is saved.
2.  **Backend:** A Flask server (`app.py`) loads the fine-tuned model into memory *once* when it starts.
3.  **Frontend:** A simple HTML page (`templates/index.html`) provides a textarea for user input.
4.  **Inference:** When the user submits their code, it is sent to a `/fix` route on the Flask server. The server runs the `get_model_fix()` function, which tokenizes the text, generates a fix using the model, and decodes the result.
5.  **Display:** The Flask server re-renders the `index.html` page, passing in the original code and the newly generated fixed code to be displayed.

## 🚀 Technology Stack

* **Model:** `Salesforce/codet5-base`
* **AI/ML:** PyTorch, Hugging Face Transformers, Datasets
* **Backend:** Flask
* **Frontend:** HTML5, CSS
* **Environment:** Conda

---

## ⚙️ Setup & Installation

Follow these steps to run the project on your local machine.

### 1. Prerequisites

* A Conda environment (like Miniconda or Anaconda).
* An NVIDIA GPU is recommended for faster inference, but it will fall back to CPU.
* The fine-tuned model files.

### 2. Clone/Download

Download or clone this project's files into a local directory (e.g., `~/ml_projects/bug_recommender`).

### 3. Get the Fine-Tuned Model

You must have the trained model files.
1.  Download the `lowparam-bugfixer-model.zip` file (the 5.4 GB file you trained).
2.  Unzip it. This will create a folder named `lowparam-bugfixer-model`.
3.  Place this folder inside the `bug_recommender` directory. Your file structure should look like this:

    ```
    bug_recommender/
    ├── lowparam-bugfixer-model/  <-- The unzipped model
    ├── templates/
    │   └── index.html
    ├── app.py
    └── test_my_model.py
    ```

### 4. Create Conda Environment & Install Dependencies

1.  Open your terminal and navigate to the project folder:
    ```bash
    cd ~/ml_projects/bug_recommender
    ```

2.  Activate your `torch_env` (which has the correct libraries):
    ```bash
    conda activate torch_env
    ```

3.  If you haven't installed Flask in this environment, do so:
    ```bash
    pip install flask
    ```

---

## ▶️ How to Run

There are two ways to use the model:

### 1. Run the Local Web App

This is the main way to use the tool.

1.  Ensure you are in the `(torch_env)` environment and in the `bug_recommender` directory.
2.  Run the Flask app:
    ```bash
    python app.py
    ```
3.  The terminal will load the model and show a line like:
    `* Running on http://127.0.0.1:5000`
4.  Open your web browser and go to **`http://127.0.0.1:5000`**.
5.  Paste your buggy Python code into the text box and click "Fix Code".

### 2. Run the Command-Line Test

You can also test the model directly from your terminal.

1.  Ensure you are in the `(torch_env)` environment.
2.  Make sure your `test_my_model.py` script is pointing to the correct model path (`model_path = "./lowparam-bugfixer-model"`).
3.  Run the script:
    ```bash
    python test_my_model.py
    ```
    This will run the built-in `bitcount` bug example and print the result directly to your terminal.

## 🔮 Future Work

As outlined in the report, future work includes:
* Integrating a true rule-based AST analysis module.
* Training on a dedicated dataset for **complexity-aware optimization**.
* Benchmarking performance on actual resource-constrained hardware (e.g., smartphones).
