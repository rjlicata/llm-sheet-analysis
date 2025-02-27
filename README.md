## LLM Sheet Analysis

This is a repository for utilizing an LLM to write and execute code related to spreadsheet analysis (CSVs and Excel files).

### Caution

This is a prototype. It is able to write and execute code which is an inherent risk. There are some basic safeguards in place which will be discussed [later](#potential-risks).

### Prerequisites

All LLM inference in this repository is currently handled by Ollama and OpenAI. This means you have to install Ollama and run a model (llama3.2 is recommended). Follow the instructions in [this blog](https://medium.com/@sridevi17j/step-by-step-guide-setting-up-and-running-ollama-in-windows-macos-linux-a00f21164bf3). We use the OpenAI Python API for easy communication in the container.

### Getting Started

This was originall developed in an anaconda environment but has been updated to operate in docker for safety. You can run the following code to get started:

```bash
make build
```

This will build the docker image and install a local Python package `sheet_analysis`.

### main.py

In the main level of the directory, there is a code ["main.py"](main.py). This can be accessed by running `make converse` in the terminal. If you provide a data path for a spreadsheet, it will initialize a conversation-style interaction with the agent. You can ask it questions about the data, and it will generate code, run it, and respond with the answer. An example of this is shown below. This is broken up, because the LLM generates markdown for the code.

```
Your session with the agent is beginning. To end, enter STOP or hit Ctrl + C
-----------------------------------------------------------------------
User Message: What city has the smallest house?
AI Response: The city with the smallest house is Lakewood.

Here is the code I generated to get that:
```

```python
import pandas as pd

def func(data):
    # Filter out non-numeric values from Square Footage column
    data['Square Footage'] = pd.to_numeric(data['Square Footage'])
    
    # Find the city with the smallest average square footage
    min_city = data.groupby('City')['Square Footage'].mean().idxmin()
    
    return f"The city with the smallest house is {min_city}."

```
```
-----------------------------------------------------------------------
User Message: Tell me about the smallest house in Arvada.
AI Response: The smallest house in Arvada has a square footage of 2834 and is located at 628 Elm Street, priced at $781,400.

Here is the code I generated to get that:
```
```python

import pandas as pd
import matplotlib.pyplot as plt

def func(data):
    # Filter the data for houses in Arvada
    arvada_houses = data[data['City'] == 'Arvada']
    
    # Find the smallest house
    smallest_house = arvada_houses.loc[arvada_houses['Square Footage'].idxmin()]
    
    return smallest_house

```
```
-----------------------------------------------------------------------
User Message: STOP
-----------------------------------------------------------------------
Your session has ended. Thank you!
```

### Example Notebook

There is an [example notebook](notebooks/housing-example.ipynb) for the housing data. It shows the minimal code required to communicate with the agent with three examples. Some example figures from this can be found [here](notebooks/figures/output.png) and [here](figures/output.png).

### Potential Risks and Safeguards

There are inherent risks with allowing a model to write code that is blindly executed. There are three basic safeguards currently in place.

1. This operates in a docker container under the user `nobody`. It should not have much access to do anything and is not exposed to files outside of the "llm-sheet-analysis" directory.

2. In the code generation prompt, we tell the model it only has access to `pandas`, `numpy`, `datetime`, `re`, `sklearn`, `matplotlib`, and `scipy`.
    - These packages should not have things that can necessarily be used nefariously by an LLM (to my knowledge).
    - Furthermore, it is unlikely that llama3.2 will generate nefarious code when prompted the way it is: analyze this DataFrame.

3. There are import checks conducted to ensure that the only imports come from these packages.

As previously mentioned, these are very basic safeguards. Use at your own risk.

### Next Steps

These are items that are planned to be added/updated.

1. Add configuration file to make it clear what file, model, etc. you want to use when running "main.py" or `make converse`.

2. Add better safeguards.
    - There are likely packages out there that can address some of the aforementioned concerns.

3. Create chat GUI to replace "main.py".

4. Implement other LLM communication methods.
    - This currently only handles Ollama-hosted models using OpenAI API.