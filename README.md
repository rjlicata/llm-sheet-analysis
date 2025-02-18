## LLM Sheet Analysis

This is a repository for utilizing an LLM to write and execute code related to spreadsheet analysis (CSVs and Excel files).

### Caution

This is a prototype. It is able to write and execute code which is an inherent risk. There are some basic safeguards in place which will be discussed later.

### Prerequisites

All LLM inference in this repository is currently handled by Ollama. This means you have to install Ollama and run a model (llama3.2 is recommended). Follow the instructions in [this blog](https://medium.com/@sridevi17j/step-by-step-guide-setting-up-and-running-ollama-in-windows-macos-linux-a00f21164bf3).

### Getting Started

This was developed in an anaconda environment. You can run the following code to get started:

```bash
conda create -n sheets
conda activate sheets
python -m pip install .
```

This will create a virtual environment in Anaconda and install a local Python package `sheet_analysis`. 