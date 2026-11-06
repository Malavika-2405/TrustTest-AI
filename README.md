# 🛡️ TrustTest AI – LLM Quality & Reliability Testing Platform

**Test Smarter. Trust AI.**

TrustTest AI is a web-based platform designed to evaluate and monitor the quality and reliability of AI-generated responses. It provides semantic similarity evaluation, automated testing, prompt injection pattern detection, multi-turn consistency checks, regression testing, and evaluation reports through an interactive dashboard.

## 🌟 Key Features

### 1. 📊 Overview Dashboard
- Monitor total evaluation runs.
- View average evaluation scores.
- Track the latest evaluation status.
- Visualize evaluation score trends.
- Review recent evaluation history.

### 2. 📚 Golden Dataset Management
- Create and manage evaluation datasets.
- Store questions, expected answers, and reference context.
- Organize test cases by category.
- Maintain reusable test data for evaluations.

### 3. 🧪 Semantic Evaluation Engine
- Compare expected and AI-generated responses.
- Use Sentence Transformers for semantic similarity.
- Generate similarity scores.
- Classify results as PASS or REVIEW based on a configurable threshold.
- Store evaluation results in the database.

### 4. 🧰 Automated Test Runner
- Execute automated tests using Pytest.
- Display test execution results.
- Identify failed test cases.
- Run the test suite directly from the application.

### 5. 🔄 Automated Regression Testing
- Compare evaluation runs.
- Monitor changes in evaluation performance.
- Identify potential quality degradation.

### 6. 🛡️ AI Safety & Injection Testing
- Detect common prompt injection patterns.
- Identify instruction override attempts.
- Detect system prompt extraction patterns.
- Identify suspicious jailbreak-related phrases.

### 7. 💬 Multi-Turn Consistency Testing
- Maintain conversation testing sessions.
- Analyze responses across multiple turns.
- Detect selected contradiction patterns.
- Track consistency results and conversation history.

### 8. 📑 Quality Reports
- View evaluation summaries.
- Analyze metric-wise performance.
- Visualize individual test scores.
- Compare evaluation history.
- Download evaluation results in CSV format.

## 🛠️ Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Frontend | Streamlit |
| Data Processing | Pandas |
| Machine Learning / NLP | Sentence Transformers |
| Pretrained Model | all-MiniLM-L6-v2 |
| Similarity Calculation | Scikit-learn |
| Database | SQLite |
| Visualization | Plotly |
| Automated Testing | Pytest |
| Environment Management | Python Virtual Environment |

## 🏗️ Project Architecture

```text
TrustTest-AI/
│
├── app.py
│
├── database/
│   ├── db.py
│   └── schema.sql
│
├── modules/
│   ├── dashboard.py
│   ├── dataset_manager.py
│   ├── evaluation_engine.py
│   ├── semantic_evaluator.py
│   ├── automated_test_runner.py
│   ├── regression_testing.py
│   ├── safety_testing.py
│   ├── conversation_testing.py
│   └── reports.py
│
├── tests/
│   ├── test_semantic_evaluator.py
│   ├── test_safety_patterns.py
│   ├── test_conversation.py
│   └── test_dataset_manager.py
│
├── trusttest.db
├── requirements.txt
└── README.md
```

## ⚙️ Installation and Setup

### Prerequisites

- Python 3.10 or later
- Git
- Visual Studio Code (recommended)

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd TrustTest-AI
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your actual GitHub repository URL.

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the Application

```bash
python -m streamlit run app.py
```

Open the local URL displayed in your terminal.

## 🧪 Running Automated Tests

Execute the complete automated test suite:

```bash
python -m pytest tests -v
```

The test suite covers:

- Semantic similarity evaluation.
- Safe prompt identification.
- Prompt injection pattern detection.
- Multi-turn contradiction detection.
- Dataset creation and retrieval.
- Test case insertion, updating, and deletion.

**Current test status:** 20 automated tests passed.

## 📈 Evaluation Methodology

TrustTest AI uses the `all-MiniLM-L6-v2` Sentence Transformers model to generate sentence embeddings and calculates cosine similarity between expected and generated responses.

The current evaluation threshold is 70%:

- **PASS:** Similarity score is 70% or higher.
- **REVIEW:** Similarity score is below 70%.

Semantic similarity measures similarity in meaning. It does not independently establish factual correctness, detect every hallucination, or guarantee AI safety.

## 🎯 Project Objective

The objective of TrustTest AI is to provide a centralized environment for testing AI response quality and reliability through reusable datasets, automated test execution, semantic evaluation, safety pattern checks, and performance reporting.

## 👩‍💻 Developer

**Malavika P.**

B.E. Computer Science and Engineering | 2027

GitHub: [Malavika-2405](https://github.com/Malavika-2405)

---

*TrustTest AI – Test Smarter. Trust AI.*