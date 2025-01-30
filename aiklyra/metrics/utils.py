from pydantic import BaseModel

def load_system_prompt(task_name:str)->str:
    """
    Load the system prompt for a given task.

    Args:
        task_name (str): The name of the task for which to load the system prompt.

    Returns:
        str: The content of the system prompt file as a string.

    Raises:
        FileNotFoundError: If the specified prompt file does not exist.
        IOError: If there is an error reading the prompt file.
    """
    try : 

        with open(f"/home/fahd/Desktop/aiklyra/aiklyra/metrics/prompts/{task_name}.txt", "r") as f:
            return f.read()
    except FileNotFoundError or IOError as e:
        raise f"Error : {e} "
    



class FaithfulnessSchema(BaseModel):
    score: float 
    reason : str

class ScoreSchema(BaseModel):
    score: float 
    
    


