# Multi-agent electrolyte discovery
Supporting code for: "Multi-agent-network-based idea generator for zinc-ion battery electrolyte discovery: A case study on zinc tetrafluoroborate hydrate-based deep eutectic electrolytes"

This repository contains an LLM-driven multi-agent framework for collaborative discovery of advanced electrolytes. The system combines:

- Autonomous literature analysis
- Multi-agent decision workflows

Though initially demonstrated for zinc-ion battery electrolytes in our paper, the modular architecture can be adapted to other materials discovery domains through configuration of prompts, agent messages, and input literature.

For specific details about our zinc-based DEE case study and experimental validation, see the published paper.

# User Guide

## Installation Instructions
1) Install relevant packages

## Installation

```bash
git clone https://github.com/yourusername/multi-agent-electrolyte-discovery
cd multi-agent-electrolyte-discovery
conda env create -f environment.yml
conda activate multi-agent-electrolyte-discovery
```
3) 

## Preparing the Vector Databases

### 1. Extract Papers
    Gather Research Papers

        Collect all relevant publications in PDF format

        Store them in a dedicated papers/ directory

    Run Extraction Workflow

        Execute the extract_papers.ipynb Jupyter notebook

        Follow the step-by-step instructions contained in the notebook to process documents


## Running the Model

# Disclaimer

This software is provided "as is", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and noninfringement. In no event shall the authors or copyright holders be liable for any claim, damages, or other liability, whether in an action of contract, tort, or otherwise, arising from, out of, or in connection with the software or the use or other dealings in the software.

This repository is maintained in a static state to closely match the code used in the original publication. No updates or bug fixes are planned. Users should be aware that future updates to underlying dependencies (including but not limited to langchain, langgraph, chroma, or other packages) may break functionality.

Use of this software is entirely at your own risk.
