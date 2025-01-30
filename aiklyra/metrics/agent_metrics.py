from openai import AzureOpenAI
from dotenv import load_dotenv
import typing as t
from utils import *
import os 
load_dotenv()


try : 
    judge_model = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version="2024-08-01-preview",
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    )
except Exception as e:
    raise  "Error"
    

class AgentMetrics:
    """
    A class to analyze agent metrics based on user input and reference topics.
    Attributes:
    -----------
    user_input : List[dict]
        A list of dictionaries containing user inputs.
    reference_topics : List[str]
        A list of reference topics.
    system_prompt : str
        The system prompt loaded based on the task name.
    """
    def __init__(self,user_input:t.List[t.Union[str,dict]],reference_topics:t.List[str],task_name:t.Literal["agent_goal_accuracy","topic_adherence","faithfulness"],llm_answer:t.Optional[str]=None):
        """
        Initializes the AgentAnalyser with user input, reference topics, and a task name.

        Args:
            user_input (List[dict]): A list of dictionaries containing user input data.
            reference_topics (List[str]): A list of reference topics.
            task_name (str): The name of the task to load the system prompt for.
        """
        self.prompt=self.construct_prompt(user_input=user_input,reference_topics=reference_topics,llm_answer=llm_answer)
        self.task_name=task_name
        self.system_prompt = load_system_prompt(task_name)

    @classmethod
    def construct_prompt(self,**kwargs):
        """
        Constructs a prompt based on the user input and reference topics.
        Returns:
            str: The constructed prompt.
        """
        if kwargs['llm_answer'] is not None:
            return f"User Questions : \n {kwargs['user_input']} \n LLM Answer : {kwargs['llm_answer']} \n Reference Topics : \n {kwargs['reference_topics']} \n"
        
        return f"User Questions : \n {kwargs['user_input']} \n Reference Topics : \n {kwargs['reference_topics']} \n"


    def _get_score(self):
        """
        Generates a response from the judge_model based on user input and reference topics.
        This method constructs a message payload with the system prompt, user input, and reference topics,
        and sends it to the judge_model's chat completion API to generate a response.
        Returns:
            str: The content of the response message from the judge_model.
        Raises:
            ValueError: If an exception occurs during the API call, the exception is caught and re-raised as a ValueError.
        """
        
        try : 
            messages=[{"role":"system","content":self.system_prompt},{"role":"user","content":self.prompt}]
            result = judge_model.beta.chat.completions.parse(
                model="gpt-4o",
                messages=messages,
                response_format= FaithfulnessSchema if self.task_name=="faithfulness" else ScoreSchema,
            )
            
            return result.choices[0].message.content
        except Exception as e:
            raise ValueError(e)
        
if __name__=='__main__' : 
    # Faithfulness Test case
    # user_input="When was the first super bowl?",
    # response="The first superbowl was held on Jan 15, 1967",
    # retrieved_contexts=[
    #         "The First AFL–NFL World Championship Game was an American football game played on January 15, 1967, at the Los Angeles Memorial Coliseum in Los Angeles."
    #     ]
    # jude=AgentMetrics(user_input=user_input,reference_topics=retrieved_contexts,task_name="faithfulness",llm_answer=response)
    # print(jude._get_score())


    # Topic Adherance Test case     
    user_input = [
        {'role': 'human', 'content': "Can you provide me with details about Einstein's theory of relativity?"},
        {'role': 'ai', 'content': "Sure, let me retrieve the relevant information for you."},
        {'role': 'used tool', 'content': "Found relevant documents: 1. Relativity: The Special and the General Theory, 2. General Theory of Relativity by A. Einstein."},
        {'role': 'ai', 'content': "I found some documents on Einstein's theory of relativity. Which one would you like to know more about: 'Relativity: The Special and the General Theory' or 'General Theory of Relativity by A. Einstein'?"},
        {'role': 'human', 'content': "Tell me about the 'General Theory of Relativity'."},
        {'role': 'ai', 'content': "Got it! Let me fetch more details from 'General Theory of Relativity by A. Einstein'."},
        {'role': 'used tool', 'content': "The document discusses how gravity affects the fabric of spacetime, describing the relationship between mass and spacetime curvature."},
        {'role': 'ai', 'content': "The 'General Theory of Relativity' explains how gravity affects the fabric of spacetime and the relationship between mass and spacetime curvature. Would you like more details or a specific explanation?"},
        {'role': 'human', 'content': "No, that's perfect. By the way, do you know any good recipes for a chocolate cake?"},
        {'role': 'ai', 'content': "Sure! Let me find a simple and delicious recipe for a chocolate cake."},
        {'role': 'used tool', 'content': "Here’s a popular recipe for a chocolate cake: Ingredients include flour, sugar, cocoa powder, eggs, milk, and butter. Instructions: Mix dry ingredients, add wet ingredients, and bake at 350°F for 30-35 minutes."},
        {'role': 'ai', 'content': "I found a great recipe for chocolate cake! Would you like the full details, or is that summary enough?"}
    ]
    scorer=AgentMetrics(user_input=user_input,reference_topics=["Einstein's theory of relativity","Chocolate cake recipe"],task_name="topic_adherence")
    print(scorer._get_score())