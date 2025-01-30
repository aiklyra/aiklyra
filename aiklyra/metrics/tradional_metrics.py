from rouge_score.rouge_scorer import RougeScorer
from sacrebleu import corpus_bleu
import typing as t


class RougeScore():
    def __init__(self,stemmer:bool,score_type:t.Literal['rouge1','rougeL']) -> None:
        """
        Initializes the RougeScore class with the specified parameters.
        Args:
            stemmer (bool): Whether to use a stemmer for the ROUGE scorer.
            score_type (Literal['rouge1', 'rougeL']): The type of ROUGE score to compute.
        """
        self.scorer = RougeScorer(rouge_types=score_type, use_stemmer=stemmer)
        self.score_type = score_type
    def _getScore(self,reponse:str,context:str,metrics_type:t.Optional[t.Literal["precision","recall","f1"]]=None) ->float :
        """
        Computes the ROUGE score between the response and context.
        Args:
            reponse (str): The target text.
            context (str): The predicted text.
            metrics_type (Optional[Literal["precision", "recall", "f1"]]): The type of metric to return. Defaults to None.
        Returns:
            float: The computed ROUGE score.
        """
        if metrics_type is None:
            return self.scorer.score(target=reponse,prediction=context)[self.score_type[0]]
        
        metrics_type = 0 if metrics_type == "precision" else 1 if metrics_type == "recall" else 2
        return list(self.scorer.score(target=reponse,prediction=context)[self.score_type[0]])[metrics_type]
    
class BlueScore():
    """
    A class to compute BLEU scores for text evaluation.
    Attributes:
        references (List[List[str]]): A list of reference texts.
    """
    def __init__(self,references:t.List[str]) -> None:
        """
        Initializes the BlueScore class with the specified references.
        Args:
            references (List[str]): A list of reference texts.
        """
        self.references = [[ref] for ref in references]
    
    def _getScore(self,prediction:str) -> float:
        """
        Computes the BLEU score for the given prediction against the references.
        Args:
            prediction (str): The predicted text.
        Returns:
            float: The computed BLEU score.
        """
        return corpus_bleu([prediction],self.references).score/100