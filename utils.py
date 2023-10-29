from langchain.agents import create_csv_agent
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType
from ast import literal_eval
import pandas as pd
import io
import tempfile
import os

class table_transformer(object):
    def __init__(self):
        pass

    def clear(self):
        os.system('clear')

    def create_agent(self, path):
        if isinstance(path, list):
            return create_csv_agent(ChatOpenAI(temperature=0, model="gpt-4"),
                                      path,
                                      verbose=False,
                                      agent_type=AgentType.OPENAI_FUNCTIONS)
        elif isinstance(path, str):
            return create_csv_agent(ChatOpenAI(temperature=0, model="gpt-4"),
                                                         path,
                                                         verbose=False,
                                                         agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION)


    def get_dup_columns(self, agent):
        op = agent.run("Find the columns in table 2 that contain the same data with different formatting or under different column names. Return a dictionary string with keys containing the original name and values containing the duplicate name. If no columns are duplicated return '{}'. Do not return any free text.")
        return op
    
    def remove_duplicates(self, agent, cols_to_remove):
        op = agent.run(f"Remove the selected duplicate columns from the table. Return the output as a dictionary. If no columns are specified, return the original table as a dictionary. These are the columns to remove: {cols_to_remove}")
        return op
    
    def compare_tables(self, agent):
        op = agent.run("Which columns in table 2 represent the same information as the columns in table 1? Return a dictionary string with keys containing the original name and values containing the similar field. If no columns are similar return '{}'. Do not return any free text.")
        return op
    
    def rename_prune_table(self, agent, similar_columns):
        sim_col_dict = literal_eval(similar_columns)
        cols_to_keep = list(sim_col_dict.keys())
        print(f"Changing from:to: \n {pd.DataFrame({'From':list(sim_col_dict.keys()), 'To':list(sim_col_dict.values())})}")
        agent.run(f"Rename the columns in table 2, represented by the values in this dictionary, to the names represented by their corresponding key: {similar_columns}")
        op = agent.run(f"Remove all columns from table 2 that are not contained in this list and return the table in dictionary format without any surrounding text: {cols_to_keep}")
        return op
    
    def reformat_columns(self, agent):
        op = agent.run("Reformat the data contained in the columns of table 2 to match the formatting of the corresponding columns in table 1. Ensure numerical values match. Output the reformatted table 2 as a dictionary.")
        return op
    
    def extract_text_between_brackets(self, input_string):
        fi = input_string.index('{')
        li = input_string.rindex('}')
        return input_string[fi:li+1]
    
    def create_df(self, data, eval=True):
        if eval:
            return pd.DataFrame(literal_eval(data))
        else:
            return pd.DataFrame(data)
    
    def present_dups_for_removal(self, input_string):
        d = literal_eval(input_string)
        if len(d) >0:
            return pd.DataFrame({'original':list(d.keys()), 'duplicate':list(d.values())})
        else:
            return None
        
    def create_in_memory_csv(self, dataframe):
        memory_file = io.StringIO()
        dataframe.to_csv(memory_file, index=False)
        csv_data = memory_file.getvalue()
        memory_file.close()
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".csv") as temp_file:
            temp_file.write(csv_data)
            temp_file_path = temp_file.name
        return temp_file_path