import pytest
from aiklyra import RougeScore, BlueScore

@pytest.fixture
def rouge1_scorer():
    return RougeScore(stemmer=True, score_type=['rouge1'])

@pytest.fixture
def rougeL_scorer():
    return RougeScore(stemmer=False, score_type=['rougeL'])

def test_rouge1_score(rouge1_scorer, rougeL_scorer):
    response = "The quick brown fox jumps over the lazy dog"
    context = "The quick brown fox jumps over the lazy dog"
    score = rouge1_scorer._getScore(response, context)
    score = rougeL_scorer._getScore(response, context)
    print(f"ROUGE-L Score with different texts: {score}")

def test_rouge1_score_with_partial_match(rouge1_scorer):
    response = "The quick brown fox"
    context = "The quick brown fox jumps over the lazy dog"
    score = rouge1_scorer._getScore(response, context)
    print(f"ROUGE-1 Score with partial match: {score}")

def test_rougeL_score_with_partial_match(rougeL_scorer):
    response = "The quick brown fox"
    context = "The quick brown fox jumps over the lazy dog"
    score = rougeL_scorer._getScore(response, context)
    print(f"ROUGE-L Score with partial match: {score}")

def test_rouge1_score_with_no_match(rouge1_scorer):
    response = "The quick brown fox"
    context = "Lorem ipsum dolor sit amet"
    score = rouge1_scorer._getScore(response, context)
    print(f"ROUGE-1 Score with no match: {score}")

def test_rougeL_score_with_no_match(rougeL_scorer):
    response = "The quick brown fox"
    context = "Lorem ipsum dolor sit amet"
    score = rougeL_scorer._getScore(response, context)
    print(f"ROUGE-L Score with no match: {score}")

@pytest.fixture
def blue_scorer():
    references = ["The quick brown fox jumps over the lazy dog"]
    return BlueScore(references=references)

def test_blue_score(blue_scorer):
    prediction = "The quick brown fox jumps over the lazy dog"
    score = blue_scorer._getScore(prediction)
    assert pytest.approx(score, 0.01) == 1.0

def test_blue_score_with_different_text(blue_scorer):
    prediction = "The quick brown fox jumps over the lazy cat"
    score = blue_scorer._getScore(prediction)
    assert score < 1.0
