import pytest
from unittest.mock import MagicMock, patch
from aiklyra.metrics.agent_metrics.agent_metrics import AgentMetrics, LLMClient, FaithfulnessSchema, ScoreSchema

@pytest.fixture
def agent_metrics():
    user_input = [{"question": "What is AI?"}]
    reference_topics = ["Artificial Intelligence"]
    task_name = "faithfulness"
    llm_answer = "AI is the simulation of human intelligence in machines."
    model_instance = MagicMock()

    return AgentMetrics(
        user_input=user_input,
        reference_topics=reference_topics,
        task_name=task_name,
        llm_answer=llm_answer,
        model_instance=model_instance
    )

@patch('aiklyra.metrics.agent_metrics.agent_metrics.LLMClient.judge_model')
def test_get_score_faithfulness(mock_judge_model, agent_metrics):
    mock_judge_model.beta.chat.completions.parse.return_value.choices[0].message.content = "Faithfulness score: 0.9"
    result = agent_metrics._get_score()
    assert result == "Faithfulness score: 0.9"
    mock_judge_model.beta.chat.completions.parse.assert_called_once_with(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": agent_metrics.system_prompt},
            {"role": "user", "content": agent_metrics.prompt}
        ],
        response_format=FaithfulnessSchema
    )

@patch('aiklyra.metrics.agent_metrics.agent_metrics.LLMClient.judge_model')
def test_get_score_other_task(mock_judge_model, agent_metrics):
    agent_metrics.task_name = "topic_adherence"
    mock_judge_model.beta.chat.completions.parse.return_value.choices[0].message.content = "Score: 0.8"
    result = agent_metrics._get_score()
    assert result == "Score: 0.8"
    mock_judge_model.beta.chat.completions.parse.assert_called_once_with(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": agent_metrics.system_prompt},
            {"role": "user", "content": agent_metrics.prompt}
        ],
        response_format=ScoreSchema
    )

@patch('aiklyra.metrics.agent_metrics.agent_metrics.LLMClient.judge_model')
def test_get_score_exception(mock_judge_model, agent_metrics):
    mock_judge_model.beta.chat.completions.parse.side_effect = Exception("API error")
    with pytest.raises(ValueError) as excinfo:
        agent_metrics._get_score()
    assert "API error" in str(excinfo.value)
