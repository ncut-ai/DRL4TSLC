from traci_ex.basic_commands import *
from traci_ex.value_retrieval import *
from traci_ex.value_changing import *
# import traci_ex
import yaml
from agent_ex.intersection_agent import *
# import agent_ex
import shutil
import os


def read_yaml(yaml_file):
    """to read a yaml file"""
    with open(yaml_file, 'rb') as f:
        all_data = list(yaml.safe_load_all(f))
    return all_data


def start_env(sumo_cmd):
    """Launch the simulation"""
    print('Initializing the simulation environment...')
    simulation_start(sumoCmd=sumo_cmd)


def close_env():
    """Close the environment"""
    simulation_close()


def prerun_env(pre_steps):
    """Warm up the simulation"""
    pre_run_simulation_to_prepare(pre_steps=pre_steps)


def get_env_time():
    """Get the current simulation time"""
    return get_simulation_time()


def env_step():
    """Advance the environment by one step"""
    simulation_step()


def initialize_agents_by(*args):
    """Initialize all intersection agents according to agent settings"""
    agent_settings = args[0]
    rl_setting = args[1]
    intersection_agents = {}
    for key, agent_setting in agent_settings.items():
        intersection_agents[key] = IntersectionAgent(
            agent_setting, rl_setting)
    return intersection_agents


def get_current_state(agent):
    """Obtain the current state of the Agent"""
    state_config = agent.state_config
    state_val = ""  # Initialize the state
    for state_name in state_config['names']:  # Traverse every state variable
        func_name = state_config['func_names'][state_name]
        paras = state_config['paras'][state_name]
        val = eval(func_name)(paras)
        state_val = state_val + str(val) + ","
    agent.save_current_state(state_val)


def select_action(agent):
    """Select an action"""
    agent.select_action()


def deploy_action_into_env(agent):
    """Deploy the action to the environment and wait for execution"""
    action_config = agent.action_config
    action_name = agent.action_current
    func_name = action_config['func_names'][action_name]
    paras = action_config['paras'][action_name]
    # Run the function
    eval(func_name)(paras)


def time_count_step(agent_list):
    """Decrement the strategy execution timer for all Agents by 1, equivalent to executing 1 step"""
    for agent in agent_list:
        agent_list[agent].time_count_step()


def get_reward(agent):
    """Obtain the reward"""
    reward_config = agent.reward_config
    reward_name = reward_config['names']  # There is only one reward
    func_name = reward_config['func_names'][reward_name]
    paras = reward_config['paras'][reward_name]
    #
    val = eval(func_name)(paras)
    agent.save_reward(val)

def update_q_table(agent):
    agent.update_q_table_actor_critic()
    print('Q-Learning')

def save_sumo_output_data(ep):
    """Save SUMO simulation output data"""
    sumo_dir = os.path.join(os.getcwd(), 'sumo_network') # SUMO simulation folder
    default_output_dir = os.path.join(sumo_dir, 'output') # Default folder for simulation output data
    dir_name = f"output_data({ep})" # Output data folder: output_data(99)
    new_output_dir = os.path.join(sumo_dir, dir_name) # With path

    if os.path.exists(new_output_dir) == True: #If exists, clear all files
        shutil.rmtree(new_output_dir) # Delete files and folders
    else:
        pass
    #
    shutil.copytree(default_output_dir, new_output_dir)
