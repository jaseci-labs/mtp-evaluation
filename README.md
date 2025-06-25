# MTLLM: Meaning-Typed Large Language Models for Jac

**OOPSLA 2025 Artifact**

This repository contains the MTLLM (Meaning-Typed Large Language Model) implementation for the Jac programming language, as described in our OOPSLA 2025 paper.

## Quick Installation

### Option 1: Direct Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/mtllm-oopsla2025.git
cd mtllm-oopsla2025

# Install dependencies
pip install -r requirements.txt

# Install MTLLM
pip install -e .
```

### Option 2: Using Docker
```bash
# Build and run the container
docker build -t mtllm-artifact .
docker run -it mtllm-artifact
```

## Quick Start

### 1. Basic MTLLM Function

Create a file `hello.jac`:
```jac
import:py from mtllm.llms {OpenAI}

# Initialize the LLM
glob llm = OpenAI(model_name="gpt-4o-mini");

# Define an MTLLM function
can greet(name: str) -> str by llm();

# Use it
with entry {
    result = greet("OOPSLA reviewers");
    print(result);
}
```

Run it:
```bash
export OPENAI_API_KEY="your-api-key"
jac run hello.jac
```

### 2. Type-Safe AI Tasks

Create `tasks.jac`:
```jac
import:py from mtllm.llms {OpenAI}

glob llm = OpenAI();

obj Task {
    has description: str;
    has priority: 'Priority level 1-10': int;
    has estimated_hours: 'Time needed in hours': float;
}

def analyze_task(description: str) -> Task by llm();

with entry {
    task = analyze_task("Implement the MTLLM artifact for OOPSLA");
    print(f"Task: {task.description}");
    print(f"Priority: {task.priority}");
    print(f"Estimated hours: {task.estimated_hours}");
}
```

Run it:
```bash
jac run tasks.jac
```

### 3. Using Local Models (Ollama)

```jac
import:py from mtllm.llms {Ollama}

# Use local Ollama model
glob llm = Ollama(model_name="llama3.2:1b");

can summarize(text: str) -> 'Brief summary': str by llm();

with entry {
    summary = summarize("Large language models are transforming programming...");
    print(summary);
}
```

Setup Ollama:
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull a model
ollama pull llama3.2:1b

# Run the example
jac run summary.jac
```

## API Key Setup

### OpenAI
```bash
export OPENAI_API_KEY="sk-..."
```

### Anthropic
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

### Local Models (No API key needed)
```bash
# Just install and run Ollama
ollama serve
```

## Examples Directory

The `examples/` directory contains:
- `basic/` - Simple MTLLM usage patterns
- `advanced/` - Complex applications (RAG, chatbots, etc.)
- `benchmarks/` - Performance comparisons

Run any example:
```bash
cd examples/basic
jac run simple_chat.jac
```

## Troubleshooting

**Import Error**: Make sure `jaclang` is installed:
```bash
pip install jaclang
```

**API Key Error**: Set your API keys as environment variables.

**Ollama Connection Error**: Ensure Ollama is running:
```bash
ollama serve
```

## Paper Claims Validation

To validate the main claims from our paper:

1. **Run performance benchmarks**:
   ```bash
   cd benchmarks
   python run_performance.py
   ```

2. **Test type safety**:
   ```bash
   cd examples/type_safety
   jac run type_validation.jac
   ```

3. **Compare with baselines**:
   ```bash
   python compare_with_baseline.py
   ```

## License

MIT License - see [LICENSE](LICENSE) file.

## Citation

```bibtex
@inproceedings{yourname2025mtllm,
  title={MTLLM: Meaning-Typed Large Language Models as Programming Language Constructs},
  author={Your Name and Co-authors},
  booktitle={OOPSLA 2025},
  year={2025}
}
```

---

## Step 4: Create Simple Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /workspace

# Install system dependencies
RUN apt-get update && apt-get install -y git curl && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy source code
COPY . .
RUN pip install -e .

# Install Ollama for local models
RUN curl -fsSL https://ollama.ai/install.sh | sh

CMD ["bash"]
```

## Step 5: Create Simple Examples

### examples/basic/simple_chat.jac
```jac
import:py from mtllm.llms {OpenAI}

glob llm = OpenAI(model_name="gpt-4o-mini");

can chat(message: str, context: str = "") -> str by llm();

with entry {
    response = chat("Hello! How does MTLLM work?", "You are an AI assistant explaining MTLLM to researchers.");
    print(response);
}
```

### examples/advanced/data_analysis.jac
```jac
import:py from mtllm.llms {OpenAI}

glob llm = OpenAI();

obj Analysis {
    has insights: list[str];
    has recommendations: list[str];
    has confidence: 'Confidence level 0-1': float;
}

def analyze_data(data: str) -> Analysis by llm();

with entry {
    data = "Sales increased 25% in Q1, decreased 10% in Q2, stable in Q3";
    analysis = analyze_data(data);
    
    print("Insights:", analysis.insights);
    print("Recommendations:", analysis.recommendations);
    print(f"Confidence: {analysis.confidence}");
}
```

## Step 6: Push to GitHub

```bash
# Add all files
git add .
git commit -m "Initial MTLLM artifact for OOPSLA 2025"

# Create GitHub repo and push
git remote add origin https://github.com/yourusername/mtllm-oopsla2025.git
git push -u origin main
```

## Step 7: Create Release for Submission

1. Go to your GitHub repository
2. Click "Releases" → "Create a new release"
3. Tag: `v1.0.0-oopsla2025`
4. Title: "OOPSLA 2025 Artifact: MTLLM v1.0.0"
5. Description: Link to paper and brief overview
6. Publish release

## Final Repository Structure

```
mtllm-oopsla2025/
├── mtllm/                 # Core MTLLM code (copied from jaseci)
│   ├── __init__.py
│   ├── llms/
│   └── core/
├── examples/              # Simple demonstration examples
│   ├── basic/
│   └── advanced/
├── benchmarks/            # Performance validation (optional)
├── tests/                 # Basic tests (optional)
├── README.md              # Installation and quick start
├── requirements.txt       # Dependencies
├── setup.py              # Package setup
├── Dockerfile            # Docker support
├── LICENSE               # License file
└── .gitignore           # Git ignore rules
```

This approach is much simpler and gives reviewers exactly what they need: your MTLLM implementation with clear installation instructions and working examples. The README focuses on getting started quickly rather than extensive documentation.