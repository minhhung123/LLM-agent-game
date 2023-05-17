class TestingLayer():
    def __init__(self, world,agent_dict):
            self.reasonable_actions_count = {agent_name: 0 for agent_name in agent_dict.keys()}
            self.agent_dict = agent_dict
            self.world = world

    # condition = [surroundings, stamina, wealth]
    # decision = [condition, action]
    def evaluate_action(self, agent_name, decision):
        if self.is_reasonable_action(agent_name, decision):
            self.reasonable_actions_count[agent_name] += 1
        elif self.is_reasonable_action(agent_name, decision) == "unreasonable":
            self.reasonable_actions_count[agent_name] -= 1

    def is_reasonable_action(self, agent_name, decision):
        principles = self.agent_dict[agent_name].principles
        condition = decision[0]
        action = decision[1]
        surroundings, stamina, wealth = condition

        ## TODO: right now the surroundings is a list of strings, we need to change it to a format that is easier to read

        # Depending on game mechanism, based on condition, what are the rules to determine if an action is reasonable?
        # test
        print(surroundings)
        print(type(surroundings[4]))
        if not any(isinstance(obj, int) for obj in surroundings):
            print("There is an explorer nearby")
        
        # General reasonable acts for all agents
        # 1. Do not attack if there is no explorer within 1 grid
        if action == "attack" and all(isinstance(obj, int) for obj in surroundings):
            return "unreasonable"
        # 2. Gather resources if there is one in the grid and no danger nearby
        if action == "gather" and surroundings[4] == 1 and all(isinstance(obj, int) for obj in surroundings):
            return True
        # 3. Rest if stamina is below a certain threshold and no danger nearby
        if action == "rest" and stamina < 2 and all(isinstance(obj, int) for obj in surroundings):
            return True
        
        # Determine if the action is reasonable based on agent's principles
        if "belligerent" in principles:
            # Alice: Attack if there is an explorer within 1 grid
            if action == "attack" and not any(isinstance(obj, int) for obj in surroundings):
                return True
        elif "peaceful" in principles:
            # Bob: Gather resources if stamina is below a certain threshold and no danger nearby
            if action == "rest" and stamina < 2 and all(isinstance(obj, int) for obj in surroundings):
                return True
        elif "weird" in principles:
            # Charlie: Perform a random action
            if action != "":
                return True
            
        return False

    def print_reasonable_action_counts(self):
        for agent_name, count in self.reasonable_actions_count.items():
            print(f"{agent_name} reasonable actions count: {count}")

