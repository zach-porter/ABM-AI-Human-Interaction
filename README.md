
# **Agent-Based Model with Generative AI and Social Interactions**

This agent-based model (ABM) simulates how individual agents interact with each other and with a generative AI agent. The model focuses on:
- **Belief formation** and **knowledge acquisition** based on interactions.
- The influence of **AI-generated content** and **bias** on agents' beliefs and knowledge.
- **Emotional states** of agents, which influence their behavior and interactions.
- A **multilayer network** structure where agents can interact both online and offline.

The model supports **batch runs** for testing multiple parameter configurations and analyzing the results.

## **Features**

- **Agent Behavior**:
  - Agents update their beliefs, knowledge, and emotional state through interactions with AI and other agents.
  - The **AI agent** generates biased content and adjusts its bias over time based on agents' average beliefs.
  
- **Multilayer Network**:
  - Agents are connected via **offline** and **online** networks.
  - Different network structures can be chosen (e.g., **Random**, **Small World**, **Scale-Free**).

- **Adjustable Parameters**:
  - Number of agents.
  - AI accuracy and bias.
  - Network type (Random, Small World, or Scale-Free).
  
- **Data Collection**:
  - Tracks model-level outcomes like **average belief**, **AI bias**, **average knowledge**, and **average emotional state**.

## **Project Structure**

- `model.py`: Defines the agent and model classes. This is where the behavior of individual agents and the generative AI agent is implemented.
- `visualization.py`: Sets up the network visualization and chart modules using **Mesa**'s **ModularServer**. This file allows for interactive visualization of the simulation in a web browser.
- `batch_run.py`: Allows for batch running the model to test multiple parameter configurations. The data is collected at the model level and saved in a CSV file for analysis.

## **Installation**

### **Requirements**

- Python 3.7 or higher
- Required Python packages:
  - `mesa`
  - `numpy`
  - `pandas`
  - `matplotlib`

Install the required packages using `pip`:

```bash
pip install mesa numpy pandas matplotlib
```

## **How to Run the Model**

### **1. Interactive Visualization**

You can run the model interactively using **Mesa's** **ModularServer** to visualize agent behavior and network dynamics in real time.

To start the interactive visualization:

1. Open a terminal or command prompt.
2. Run the following command:

   ```bash
   python visualization.py
   ```

3. Open your web browser and navigate to `http://127.0.0.1:8521`.
4. Use the sliders and dropdown menu to adjust the parameters (e.g., number of agents, AI accuracy, AI bias, network type).
5. Press "Run" to start the simulation and observe how agents' beliefs, knowledge, and emotional states evolve.

### **2. Batch Running for Parameter Testing**

You can also run batch simulations with multiple parameter combinations and collect model-level data.

To perform a batch run:

1. Open a terminal or command prompt.
2. Run the following command:

   ```bash
   python batch_run.py
   ```

3. The batch run will test various combinations of parameters (e.g., number of agents, AI accuracy, AI bias, and network type) and save the results in a CSV file (`batch_run_results.csv`).

4. You can open this CSV file in any data analysis tool (such as Excel, Jupyter Notebook, or Python) to analyze the results.

## **Parameter Descriptions**

### **Adjustable Parameters in Visualization**

- **Number of Agents** (`num_agents`): Defines how many agents will participate in the simulation. Default range is 10 to 200.
- **AI Accuracy** (`ai_accuracy`): The accuracy of the AI agent in generating unbiased content. A value between 0.5 (low accuracy) and 1.0 (high accuracy).
- **AI Bias** (`ai_bias`): The initial bias level of the AI agent in the content it generates. A value between 0 (no bias) and 1 (high bias).
- **Network Type** (`network_type`): Defines the structure of the agent interaction network. Options include:
  - **Random**: Agents are connected randomly.
  - **Small World**: Agents have short paths between each other with some clustering.
  - **Scale-Free**: A network where a few agents are highly connected, while most agents have fewer connections.

### **Batch Run Parameters**

In `batch_run.py`, the following parameters are tested across multiple runs:

- **Number of Agents** (`num_agents`): [50, 100, 150]
- **AI Accuracy** (`ai_accuracy`): [0.7, 0.85, 0.95]
- **AI Bias** (`ai_bias`): [0.0, 0.2, 0.5]
- **Network Type** (`network_type`): ["Random", "Small World", "Scale-Free"]

The results of each run are saved in the `batch_run_results.csv` file.

## **Data Collected**

For each simulation, the following model-level data is collected at each step:

- **Average Belief**: The average belief across all agents in the simulation.
- **AI Bias**: The current bias level of the AI agent.
- **Average Knowledge**: The average knowledge level across all agents.
- **Average Emotional State**: The average emotional state across all agents.

## **Contributing**

If you'd like to contribute to this project, feel free to fork the repository, create new branches, and submit pull requests. You can also open issues for bugs or feature requests.

## **Contact**

For any questions or issues, please reach out



 
