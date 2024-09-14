#model.py

import random
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import NetworkGrid
from mesa.datacollection import DataCollector
import networkx as nx
import numpy as np

# Define the Individual Agent class
class IndividualAgent(Agent):
    def __init__(self, unique_id, model, initial_belief, trust_level, susceptibility, ai_literacy):
        super().__init__(unique_id, model)
        self.belief = float(initial_belief)  # Belief on a scale from -1 to 1
        self.trust_level = float(trust_level)  # Trust in AI-generated content
        self.susceptibility = float(susceptibility)  # How easily beliefs can be changed
        self.ai_literacy = float(ai_literacy)  # Understanding of AI's capabilities
        self.interaction_propensity = float(random.random())  # Likelihood to interact
        self.knowledge = 0.0  # New knowledge attribute, starts at 0
        self.ES = float(np.random.uniform(-1, 1))  # Emotional State
        self.AIP_base = float(np.random.uniform(0, 1))  # Base AI Interaction Preference
        self.TL_base = float(np.random.uniform(0, 1))   # Base Trust Level as Python float
        self.CT = float(np.random.uniform(0, 1))   # Communication Threshold as Python float
        self.ISP_base = float(np.random.uniform(0, 1))  # Base Information Sharing Probability

    @property
    def AIP(self):
        # Adjust AIP based on Emotional State
        return np.clip(float(self.AIP_base + self.ES * 0.5), 0, 1)

    @property
    def TL(self):
        # Adjust TL based on Emotional State
        return np.clip(float(self.TL_base + self.ES * 0.5), 0, 1)

    @property
    def ISP(self):
        # Adjust Information Sharing Probability based on Emotional State
        return np.clip(float(self.ISP_base + self.ES * 0.5), 0, 1)

    def step(self):
        self.interact_with_ai()
        self.social_interaction()
        self.update_beliefs()

    def interact_with_ai(self):
        if random.random() < self.AIP:
            # Simulate AI providing information
            ai_agent = self.model.ai_agent
            ai_content, ai_knowledge = ai_agent.generate_content(self)
            # Update belief based on AI content, trust levels, and susceptibile they are
            influence = self.trust_level * self.susceptibility * ai_content
            self.belief += influence
            self.belief = np.clip(self.belief, -1, 1)

            # Receive knowledge from the AI
            self.knowledge += ai_knowledge
            self.knowledge = np.clip(self.knowledge, 0, 100)  # Keep knowledge within bounds

            # Update Emotional State based on interaction
            if ai_content > 0:
                self.ES = np.clip(self.ES + 0.1, -1, 1)
            else:
                self.ES = np.clip(self.ES - 0.1, -1, 1)

    def social_interaction(self):
        # Interact with neighbors in the network
        if random.random() < self.interaction_propensity:
            neighbors = self.model.grid.get_neighbors(self.pos, include_center=False)
            if neighbors:
                other_agent = self.model.random.choice(neighbors)
                # Get the trust (weight) between the current agent and the chosen neighbor
                trust = self.model.G[self.pos][other_agent.pos].get("weight", 0.5)  # default weight
                # Update belief based on trust and other agent's belief
                influence = trust * self.susceptibility * (other_agent.belief - self.belief)
                self.belief += influence
                self.belief = np.clip(self.belief, -1, 1)

                # Emotional Contagion: adopt some of the neighbor's emotional state
                self.ES = np.clip(self.ES + 0.1 * (other_agent.ES - self.ES), -1, 1)

    def update_beliefs(self):
        # In the future, this may be extended to include more complex belief dynamics
        # For now, this is a simple model where agents reinforce their beliefs
        # Belief is already being updated in interactions, but a more complex model could be added here
        pass 

# Define the Generative AI Agent class
class GenerativeAIAgent(Agent):
    def __init__(self, unique_id, model, bias_level=0.0):
        super().__init__(unique_id, model)
        self.bias_level = float(bias_level)  # Bias in the content generated by AI
        self.learning_rate = 0.05  # How fast the AI learns

    def generate_content(self, individual_agent):
        # Generate content influenced by AI's bias and some randomness
        content = self.bias_level + random.uniform(-0.1, 0.1)

        # Generate a piece of knowledge (can be influenced by AI's bias)
        knowledge = random.uniform(0, 10) + self.bias_level * 5

        return float(content), float(knowledge)

    def adjust_bias(self):
        """
        Adjust AI's bias based on how closely agents' average belief aligns with the AI's bias.
        This introduces a form of reinforcement learning where the AI attempts to maximize influence.
        This is interesting here, and does not necessarily reflect real-world AI behavior, but I imagine
        it could be already in use in some form, such as in social media around elections beliefs and opinions.
        """
        # Compute the average belief of all IndividualAgent agents (exclude the AI itself)
        agent_beliefs = [agent.belief for agent in self.model.schedule.agents if isinstance(agent, IndividualAgent)]

        if len(agent_beliefs) > 0:
            average_belief = np.mean(agent_beliefs)

            # Calculate reward based on how close the average belief is to the AI's current bias
            reward = -abs(self.bias_level - average_belief)

            # Adjust the bias level using the reward (basic reinforcement learning update rule)
            self.bias_level += self.learning_rate * reward

            # Clip the bias level to stay within the range [-1, 1]
            self.bias_level = np.clip(self.bias_level, -1, 1)

    def step(self):
        # Adjust the AI's bias every step
        self.adjust_bias()

# Define the Model class
class SocialModel(Model):
    def __init__(self, num_agents, ai_accuracy, ai_bias, network_type, width=10, height=10, seed=None):
        super().__init__()
        self.num_agents = int(num_agents)
        self.ai_accuracy = float(ai_accuracy)
        self.ai_bias = float(ai_bias)
        self.network_type = network_type
        self.width = int(width)
        self.height = int(height)
        self.seed = seed
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)

        self.schedule = RandomActivation(self)
        self.running = True

        # Create the selected network
        self.G = self.create_network(self.num_agents, self.network_type, self.seed)
        self.grid = NetworkGrid(self.G)

        # Assign random weights/trust levels to the edges between the agents, with layer info
        for u, v in self.G.edges():
            if self.G[u][v].get('layer') == 'offline':
                self.G[u][v]["color"] = "blue"  # Offline connections
            elif self.G[u][v].get('layer') == 'online':
                self.G[u][v]["color"] = "green"  # Online connections
            else:
                self.G[u][v]["color"] = "gray"  # Undefined layer
            self.G[u][v]["weight"] = float(random.uniform(0, 1))

        # Create agents and place them on the network grid
        # Each agent has an initial belief, trust level, susceptibility, and AI literacy 
        # that are all random and have a uniform distribution, but here is where you could
        # better reflect the real-world distribution of these values
        for i in self.G.nodes():
            initial_belief = float(random.uniform(-1, 1))
            trust_level = float(random.uniform(0, 1))
            susceptibility = float(random.uniform(0, 1))
            ai_literacy = float(random.uniform(0, 1))
            agent = IndividualAgent(i, self, initial_belief, trust_level, susceptibility, ai_literacy)
            self.schedule.add(agent)
            self.grid.place_agent(agent, i)  # Place the agent on the grid at the node

        # Create AI agent with an initial bias
        self.ai_agent = GenerativeAIAgent(self.num_agents + 1, self, bias_level=self.ai_bias)
        self.schedule.add(self.ai_agent)  # Add the AI agent to the schedule
        # AI agent is not placed on the grid
        # AI agent is not connected to the network, but maybe in a more complex model it could be
        # or the AI agent can be connected to a different network, idk, but I think this would be
        # an interesting way to better extend this model

        # Data collector to collect beliefs, knowledge, emotional states, and AI bias over time
        self.datacollector = DataCollector(
            model_reporters={
                "Average Belief": self.compute_average_belief,
                "AI Bias": self.compute_ai_bias,
                "Average Knowledge": self.compute_average_knowledge,
                "Average Emotional State": self.compute_average_es
            },
            #removing this just for the sake of the batch run, but it can/should be added back in
            # for the visualization file to work I think if you want to visualize the model as it runs
            #agent_reporters={
           #     "Belief": lambda agent: getattr(agent, "belief", None), 
           #     "Knowledge": lambda agent: getattr(agent, "knowledge", None),
           #     "Emotional State": lambda agent: getattr(agent, "ES", None)
           # }
        )
    
    # add a method to create a network
    def create_network(self, num_agents, network_type ,seed=None):
        """
        Create the desired network based on the selected network_type.
        Additionally, add layers (offline and online).
        I think one good way to extend this model would be to allow the user to specify
        the number of agents in each layer, and then the model could create the network
        with the specified number of agents in each layer. This would be more realistic.
        I also think it would be better to have the AI agent connected to the network in some way.
        Also, I think it would be good to specify different network types for both the offline and online networks.
        """
        if network_type == "Random":
            G_offline = nx.erdos_renyi_graph(n=num_agents, p=0.1, seed=seed)
        elif network_type == "Small World":
            G_offline = nx.watts_strogatz_graph(n=num_agents, k=6, p=0.1, seed=seed)
        elif network_type == "Scale-Free":
            G_offline = nx.barabasi_albert_graph(n=num_agents, m=3, seed=seed)
        else:
            raise ValueError(f"Unknown network type: {network_type}")

        # Create online network
        if network_type == "Random":
            G_online = nx.erdos_renyi_graph(n=num_agents, p=0.1, seed=seed+1 if seed else None)
        elif network_type == "Small World":
            G_online = nx.watts_strogatz_graph(n=num_agents, k=6, p=0.1, seed=seed+1 if seed else None)
        elif network_type == "Scale-Free":
            G_online = nx.barabasi_albert_graph(n=num_agents, m=3, seed=seed+1 if seed else None)
        else:
            raise ValueError(f"Unknown network type: {network_type}")

        # Add layer information
        for u, v in G_offline.edges():
            G_offline[u][v]['layer'] = 'offline'
        for u, v in G_online.edges():
            if G_offline.has_edge(u, v):
                # If edge exists in both, prefer offline
                continue
            G_online[u][v]['layer'] = 'online'

        # Combine both networks
        G_combined = nx.Graph()
        G_combined.add_nodes_from(G_offline.nodes(data=True))
        G_combined.add_edges_from(G_offline.edges(data=True))
        G_combined.add_edges_from(G_online.edges(data=True))

        return G_combined

    def compute_average_belief(self):
        # Calculate the average belief of all agents
        agent_beliefs = [agent.belief for agent in self.schedule.agents if isinstance(agent, IndividualAgent)]
        return float(np.mean(agent_beliefs)) if agent_beliefs else 0.0

    def compute_average_knowledge(self):
        # Calculate the average knowledge of all agents
        agent_knowledge = [agent.knowledge for agent in self.schedule.agents if isinstance(agent, IndividualAgent)]
        return float(np.mean(agent_knowledge)) if agent_knowledge else 0.0

    def compute_ai_bias(self):
        # Return the current bias of the AI
        return float(self.ai_agent.bias_level)

    def compute_average_es(self):
        # Calculate the average emotional state
        agent_es = [agent.ES for agent in self.schedule.agents if isinstance(agent, IndividualAgent)]
        return float(np.mean(agent_es)) if agent_es else 0.0

    def step(self):
        # Collect data
        self.datacollector.collect(self)
        # Step all agents, including the AI
        self.schedule.step()

    # Methods to expose the network for visualization
    def get_combined_network(self):
        return self.G

    def get_network_with_layers(self):
        return self.G

