# MTLLM: OOPSLA 2025 Artifact : 359

**Meaning-Typed Programming: Language Abstraction and Runtime for Model-Integrated Applications**

## Introduction

Large Language Models (LLMs) have demonstrated remarkable capabilities across diverse tasks, yet integrating them into traditional programming languages remains challenging due to their probabilistic nature and lack of structured output guarantees. This artifact presents **MTLLM** (The implementation of Meaning-Typed Programming in open-sourced Jaseci ecosystem), a novel programming language abstraction that bridges the gap between the structured world of programming languages and the unstructured outputs of LLMs.

**Key Contributions:**

1. **Type-Safe LLM Integration**: MTLLM provides compile-time type checking for LLM-powered functions, ensuring that AI-generated outputs conform to expected data structures and types.

2. **Automatic Output Transformation**: A runtime system that automatically converts unstructured LLM outputs into typed programming language objects, handling parsing, validation, and error recovery.

3. **Semantic Type System**: An innovative approach to type annotations that captures both structural types (e.g., `int`, `str`) and semantic meaning, enabling more precise LLM guidance.

4. **Language-Integrated AI**: Native syntax support in the Jac programming language for defining AI-powered functions using the `by llm()` construct, making AI integration as natural as calling regular functions.

This repository contains the complete MTLLM implementation for the Jac programming language, as described in our OOPSLA 2025 paper. The full plugin is available as part of the [Jaseci ecosystem](https://www.jac-lang.org/learn/jac-mtllm/with_llm/) and is in continuous development.

## What this Artifact Contain

This artifact uses the PiPy of MTLLM which is locked to 0.3.8 and the commit on the original repository is lined in this repository. This repo contains the jac-language version and the jac-mtllm plugin as well as other parts of the ecosystem. Whithin this repo you can find benchmarks and scripts used for evaluation conducted for the paper.

## Setup Instructions

### Prerequisits

1. Requires python 3.12 or later : As mtllm is designed as a plugin for jaclang which depends on pyuthon 3.12 or later. (Not manda6tory with when running the docker container)
2. OpenAI API : The benchmark programs use OpenAI GPT models for evaluations.
3. Linux or Mac OS : Not supported on windows as of yet.

###

### Option 1: Direct Installation

In an existing environment with python 3.12 or later
```bash
# Clone the repository
git clone --recurse-submodules https://github.com/Jayanaka-98/mtllm-oopsla2025.git
cd mtllm-oopsla2025

# Install dependencies required for evaluation.
pip install "mtllm[openai, ollama, tools]==0.3.8"
pip install "eval/requirements.txt"

# Install Ollama for evaluation with llama models
curl -fsSL https://ollama.ai/install.sh
```

### Option 2: Using Docker (For Linux)

A environment with mtllm installed will be available using the provided docker container. Make sure docker is installed.

```bash
# Clone the repository
git --recurse-submodules clone https://github.com/Jayanaka-98/mtllm-oopsla2025.git
cd mtllm-oopsla2025

# Build and run the container
chmod +x setup.bash
./setup.bash
```
This will spool up the docker container and log you in as a root user.

_Please export your openai api key by_,
```bash
export OPENAI_API_KEY=<your-openai-api-key>
```

## Usage of MTLLM

### 1. Basic MTLLM Function

A basic MTLLM function in Jac allows you to define a function whose implementation is powered by an LLM, while maintaining type safety. The `by llm()` syntax delegates the function logic to the configured LLM, and the return type is enforced at runtime. This enables seamless integration of AI-generated logic into regular Jac code.

Create a file `func.jac` (Figure 8(a) in paper):
```jac
import from mtllm.llms {OpenAI}

# Initialize the LLM
glob llm = OpenAI(model_name="gpt-4o");

# Define an MTLLM function
def calculate_age(cur_year: int, dob: str) -> int by llm()

# Use it
with entry {
    age = calculate_age(cur_year = 2025, dob = 1998);
    print(age);
}
```

**Run it**: `jac run func.jac`

> Full documentation is available [here](https://www.jac-lang.org/learn/jac-mtllm/usage/#basic-functions)

### 2. MTLLM as object constructors

MTLLM can be used to automatically generate object fields using LLMs, ensuring that the generated values conform to the specified types. By leveraging the `by llm()` construct within object initializers, you can delegate the creation of certain attributes (such as a name or date of birth) to the LLM, while maintaining type safety and structure.

Create a file `object.jac` (Figure 8(b) in paper):
```jac
import from mtllm.llms {OpenAI}

# Initialize the LLM
glob llm = OpenAI(model_name="gpt-4o");

obj Person {
    has name: str;
    has dob: str;
}
with entry {
    einstien = Person(name="Einstien" by llm());
    print(f"{einstien.name} was born in {einstien.dob}");
}
```

**Run it**: `jac run object.jac`

> Full documentation is available [here](https://www.jac-lang.org/learn/jac-mtllm/usage)

### 3. MTLLM as methods of objects

MTLLM functions can also be defined as methods within objects, allowing LLM-powered logic to operate on object state. By annotating a method with `by llm()`, you enable the LLM to access the object's fields (such as `self`) and generate outputs that respect the method's return type. This pattern is useful for tasks like generating derived attributes or performing AI-driven computations specific to an object instance.

Create a file `method.jac` (Figure 8(c) in paper):
```jac
import from mtllm.llms {OpenAI}

# Initialize the LLM
glob llm = OpenAI(model_name="gpt-4o");

obj Person {
    has name : str;
    has dob : str;

    def calculate_age (cur_year: int) -> int by llm(incl_info=(self), temperature=0.7);
}

with entry {
    einstein = Person(name="Einstein", dob="March 14, 1879");
    print(einstein.calculate_age(2024));
}
```
**Run it**: `jac run method.jac`

> Full documentation is available [here](https://www.jac-lang.org/learn/jac-mtllm/usage)

## Importing and using models

All available models and how to integrate them are covered in the [docs](https://www.jac-lang.org/learn/jac-mtllm/model_declaration/).

## Running the full playable RPG game with LLM powered level genaration

The `examples/` directory contains:
- `basic/` - Simple MTLLM usage patterns
- `advanced/` - Complex applications (RAG, chatbots, etc.)
- `benchmarks/` - Performance comparisons

Run any example:
```bash
pip install pygame
cd jaseci/jac/examples/rpg_game/jac_impl/jac_impl_6
jac run main.jac
```

## Troubleshooting

**API Key Error**: Set your API keys as environment variables.

**Ollama Connection Error**: Ensure Ollama is running:
```bash
ollama serve
```