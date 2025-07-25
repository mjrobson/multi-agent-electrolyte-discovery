# Multi-Agent Electrolyte Discovery

**Supporting code for:**  
**_Multi-agent-network-based idea generator for zinc-ion battery electrolyte discovery: A case study on zinc tetrafluoroborate hydrate-based deep eutectic electrolytes_**

This repository contains an LLM-driven, multi-agent framework for electrolyte composition discovery, focused on deep eutectic electrolytes (DEEs) for zinc-ion batteries. The system combines:

- Autonomous literature analysis  
- Multi-agent reasoning and tool use  
- Retrieval-augmented generation (RAG) pipelines

While this implementation targets DEEs based on zinc tetrafluoroborate hydrate, the architecture is fully modular and adaptable to other materials discovery problems with modification to prompts, agent messages, and input data.

---

## 🛠 Installation Instructions

> ⚠️ **Important:** This project relies on specific versions of `langchain`, `langgraph`, and related packages. These ecosystems have evolved rapidly since the original study, and **newer versions are likely to break functionality or alter model behavior**.

To ensure reproducibility with the published results:

- Start from a **clean Conda environment**.
- Install dependencies using the exact versions provided.

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/multi-agent-electrolyte-discovery
cd multi-agent-electrolyte-discovery
```

### 2. Create and Activate the Environment

```bash
conda create -n electrolyte-discovery python=3.11
conda activate electrolyte-discovery
```

### 3. Install Required Dependencies


Using `pip`:

```bash
pip install -r pip_environment.txt
```

---

## 📚 Preparing the Vector Databases

### 1. Gather Research Papers

- Collect all relevant publications in **PDF** format.
- Place them in the `input/papers_pdf/` directory.

> ℹ️ **Note:** This folder — along with other intentionally empty directories in the repository — contains a `.gitkeep` file to ensure it is tracked by GitHub. You can safely leave it in place or delete it after adding your own files.

### 2. Perform One-Time Setup

Launch and follow the instructions in the `one-time-setup.ipynb` Jupyter notebook.  
This will guide you through:

- Extracting text from the PDFs  
- Cleaning and normalizing the output `.txt` files  
- Automatically summarizing the papers using GPT-4  
- Building Chroma vector databases for papers and summaries

---

## 🚀 Running the Model

Once setup is complete, open and run the `run_model.ipynb` notebook.  
This notebook will:

- Load the vector databases for RAG
- Set up retriever tools and agent system prompts
- Define a two-agent decision graph (Scientist + Principal Investigator)
- Execute the workflow and stream results to the console and to the `results/` folder

You can re-run the model as many times as you'd like to generate additional electrolyte compositions.

---

## 🔁 Reproducibility

The code in this repository is functionally identical to the version used in the original study, aside from minor formatting and documentation updates.  

While the project *can* be made to run using newer versions of the dependencies (with appropriate syntax adjustments), output behavior may differ.


---

## ⚠️ Disclaimer

This software is provided *"as is"*, without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and noninfringement.

In no event shall the authors or copyright holders be liable for any claim, damages, or other liability arising from use of the software.

This repository is maintained in a **static state** to match the published study.  **No future updates or support are planned.**

> Use this software entirely at your own risk. Updates to dependencies such as `langchain`, `langgraph`, or `chroma` may break functionality.


