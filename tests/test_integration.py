import pytest
from unittest.mock import patch, MagicMock
from aiklyra.client import (
    AiklyraClient,
    InsufficientCreditsError,
    AnalysisError,
    AiklyraAPIError,
    ConversationFlowAnalysisRequest,
    ValidationError,
    JobSubmissionResponse,
    JobStatusResponse,
)

@pytest.fixture
def setup_client():
    """
    Fixture to set up test client and data.
    """
    base_url = "http://localhost:8002"
    client = AiklyraClient(base_url=base_url)
    conversation_data = {
        "session_1": [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi there!"},
        ]
    }
    return client, conversation_data


@patch("aiklyra.client.requests.post")
def test_submit_analysis_success(mock_post, setup_client):
    """
    Test successful job submission.
    """
    client, conversation_data = setup_client

    # The API now returns a job_id.
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"job_id": "12345"}
    mock_post.return_value = mock_response

    result = client.submit_analysis(conversation_data)

    assert isinstance(result, JobSubmissionResponse)
    assert result.job_id == "12345"

    expected_url = f"{client.base_url}/{AiklyraClient.BASE_ANALYSE_ENDPOINT}"
    expected_payload = ConversationFlowAnalysisRequest(
        conversation_data=conversation_data,
        min_clusters=5,
        max_clusters=10,
        top_k_nearest_to_centroid=10,
        role="Any"
    ).model_dump()

    mock_post.assert_called_once_with(
        expected_url,
        headers={
            "Content-Type": "application/json",
            "accept": "application/json",
        },
        json=expected_payload,
    )


@patch("aiklyra.client.requests.post")
def test_submit_analysis_invalid_api_key(mock_post, setup_client):
    """
    Test API error for an invalid API key scenario.
    Since the API key is no longer used, this error is returned as a generic API error.
    """
    client, conversation_data = setup_client

    mock_response = MagicMock()
    mock_response.status_code = 403
    mock_response.json.return_value = {"detail": "Invalid API Key"}
    mock_post.return_value = mock_response

    with pytest.raises(AiklyraAPIError) as exc_info:
        client.submit_analysis(conversation_data)

    assert "Invalid API Key" in str(exc_info.value)


@patch("aiklyra.client.requests.post")
def test_submit_analysis_insufficient_credits(mock_post, setup_client):
    """
    Test insufficient credits error.
    """
    client, conversation_data = setup_client

    mock_response = MagicMock()
    mock_response.status_code = 403
    mock_response.json.return_value = {"detail": "Insufficient credits"}
    mock_post.return_value = mock_response

    with pytest.raises(InsufficientCreditsError):
        client.submit_analysis(conversation_data)


@patch("aiklyra.client.requests.post")
def test_submit_analysis_analysis_error(mock_post, setup_client):
    """
    Test analysis error with a malformed response.
    """
    client, conversation_data = setup_client

    mock_response = MagicMock()
    mock_response.status_code = 200
    # This JSON does not have the expected job_id key.
    mock_response.json.return_value = {"invalid_key": "unexpected_data"}
    mock_post.return_value = mock_response

    with pytest.raises(AnalysisError):
        client.submit_analysis(conversation_data)


@patch("aiklyra.client.requests.post")
def test_submit_analysis_api_error(mock_post, setup_client):
    """
    Test generic API error.
    """
    client, conversation_data = setup_client

    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.text = "Internal Server Error"
    mock_post.return_value = mock_response

    with pytest.raises(AiklyraAPIError) as exc_info:
        client.submit_analysis(conversation_data)

    assert "Error 500" in str(exc_info.value)


@patch("aiklyra.client.requests.post")
def test_submit_analysis_invalid_conversation_data_type(mock_post, setup_client):
    """
    Test ValidationError when conversation_data is not a dictionary.
    """
    client, _ = setup_client
    invalid_conversation_data = ["not a dictionary"]

    with pytest.raises(ValidationError) as exc_info:
        client.submit_analysis(conversation_data=invalid_conversation_data)

    assert "conversation_data must be a dictionary." in str(exc_info.value)
    mock_post.assert_not_called()


@patch("aiklyra.client.requests.post")
def test_submit_analysis_invalid_min_clusters(mock_post, setup_client):
    """
    Test ValidationError when min_clusters is non-positive.
    """
    client, valid_data = setup_client

    with pytest.raises(ValidationError) as exc_info:
        client.submit_analysis(conversation_data=valid_data, min_clusters=0)

    assert "min_clusters and max_clusters must be positive integers." in str(exc_info.value)
    mock_post.assert_not_called()


@patch("aiklyra.client.requests.post")
def test_submit_analysis_invalid_max_clusters(mock_post, setup_client):
    """
    Test ValidationError when max_clusters is non-positive.
    """
    client, valid_data = setup_client

    with pytest.raises(ValidationError) as exc_info:
        client.submit_analysis(conversation_data=valid_data, max_clusters=-5)

    assert "min_clusters and max_clusters must be positive integers." in str(exc_info.value)
    mock_post.assert_not_called()


@patch("aiklyra.client.requests.post")
def test_submit_analysis_min_clusters_greater_than_max(mock_post, setup_client):
    """
    Test ValidationError when min_clusters exceeds max_clusters.
    """
    client, valid_data = setup_client

    with pytest.raises(ValidationError) as exc_info:
        client.submit_analysis(
            conversation_data=valid_data,
            min_clusters=10,
            max_clusters=5
        )

    assert "max_clusters must be greater than or equal to min_clusters." in str(exc_info.value)
    mock_post.assert_not_called()
