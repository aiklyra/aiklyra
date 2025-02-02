import pytest
from unittest.mock import patch, MagicMock
from aiklyra.client import (
    AiklyraClient,
    AnalysisError,
    AiklyraAPIError,
    ConversationFlowAnalysisRequest
)
from aiklyra.exceptions import (
    InvalidAPIKeyError,
    InsufficientCreditsError,
    ValidationError
)
from aiklyra.models import JobSubmissionResponse, JobStatusResponse


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
def test_analyse_success(mock_post, setup_client):
    """
    Test successful analysis submission.
    """
    client, conversation_data = setup_client

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"job_id": "123456"}
    mock_post.return_value = mock_response

    result = client.submit_analysis(conversation_data)
    print(result)
    assert isinstance(result, JobSubmissionResponse)
    # Uncomment the following line if you want to check the job_id value.
    # assert result.job_id == "123456"

    # Update the expected headers to include both Content-Type and accept.
    expected_headers = {
        "Content-Type": "application/json",
        "accept": "application/json"
    }
    expected_payload = ConversationFlowAnalysisRequest(
        conversation_data=conversation_data,
        min_clusters=5,
        max_clusters=10,
        top_k_nearest_to_centroid=10,
        role="Any"
    ).model_dump()

    mock_post.assert_called_once_with(
        f"{client.base_url}/{AiklyraClient.BASE_ANALYSE_ENDPOINT}",
        headers=expected_headers,
        json=expected_payload,
    )


@patch("aiklyra.client.requests.post")
def test_analyse_analysis_error(mock_post, setup_client):
    """
    Test analysis error with malformed response.
    """
    client, conversation_data = setup_client

    mock_response = MagicMock()
    mock_response.status_code = 200
    # Simulate an unexpected payload that does not match JobSubmissionResponse.
    mock_response.json.return_value = {"invalid_key": "unexpected_data"}
    mock_post.return_value = mock_response

    with pytest.raises(AnalysisError):
        client.submit_analysis(conversation_data)


@patch("aiklyra.client.requests.post")
def test_analyse_api_error(mock_post, setup_client):
    """
    Test generic API error during analysis submission.
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
def test_missing_authorization_header(mock_post, setup_client):
    """
    Test missing authorization header scenario.
    """
    client, conversation_data = setup_client

    mock_response = MagicMock()
    mock_response.status_code = 422
    mock_response.json.return_value = {
        "detail": [
            {"type": "missing", "loc": ["header", "authorization"], "msg": "Field required"}
        ]
    }
    mock_post.return_value = mock_response

    with pytest.raises(AiklyraAPIError) as exc_info:
        client.submit_analysis(conversation_data)

    assert "Error 422" in str(exc_info.value)


@patch("aiklyra.client.requests.post")
def test_analyse_invalid_conversation_data_type(mock_post, setup_client):
    """Test ValidationError when conversation_data is not a dictionary."""
    client, _ = setup_client
    invalid_conversation_data = ["not a dictionary"]

    with pytest.raises(ValidationError) as exc_info:
        client.submit_analysis(conversation_data=invalid_conversation_data)

    assert "conversation_data must be a dictionary." in str(exc_info.value)
    mock_post.assert_not_called()


@patch("aiklyra.client.requests.post")
def test_analyse_invalid_min_clusters(mock_post, setup_client):
    """Test ValidationError when min_clusters is non-positive."""
    client, valid_data = setup_client

    with pytest.raises(ValidationError) as exc_info:
        client.submit_analysis(conversation_data=valid_data, min_clusters=0)

    assert "min_clusters and max_clusters must be positive integers." in str(exc_info.value)
    mock_post.assert_not_called()


@patch("aiklyra.client.requests.post")
def test_analyse_invalid_max_clusters(mock_post, setup_client):
    """Test ValidationError when max_clusters is non-positive."""
    client, valid_data = setup_client

    with pytest.raises(ValidationError) as exc_info:
        client.submit_analysis(conversation_data=valid_data, max_clusters=-5)

    assert "min_clusters and max_clusters must be positive integers." in str(exc_info.value)
    mock_post.assert_not_called()


@patch("aiklyra.client.requests.post")
def test_analyse_min_clusters_greater_than_max(mock_post, setup_client):
    """Test ValidationError when min_clusters exceeds max_clusters."""
    client, valid_data = setup_client

    with pytest.raises(ValidationError) as exc_info:
        client.submit_analysis(
            conversation_data=valid_data,
            min_clusters=10,
            max_clusters=5
        )

    assert "max_clusters must be greater than or equal to min_clusters".lower() in str(exc_info.value).lower()
    mock_post.assert_not_called()


# -----------------------------------------------
# New tests for check_job_status method
# -----------------------------------------------

@patch("aiklyra.client.requests.get")
def test_check_job_status_success(mock_get, setup_client):
    """
    Test successful job status check.
    """
    client, _ = setup_client
    job_id = "123456"

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "job_id": job_id,
        "status": "completed",
        "estimated_wait_time": 0,
        "result": {
            "transition_matrix": [[0.1, 0.9], [0.8, 0.2]],
            "intent_by_cluster": { "0": "greeting", "1": "response" }
        }
    }
    mock_get.return_value = mock_response

    job_status = client.check_job_status(job_id)

    assert isinstance(job_status, JobStatusResponse)
    assert job_status.job_id == job_id
    assert job_status.status == "completed"
    # Depending on your model, you may need to assert on the nested result fields.
    assert job_status.result["transition_matrix"] == [[0.1, 0.9], [0.8, 0.2]]
    assert job_status.result["intent_by_cluster"]["0"] == "greeting"

    expected_url = f"{client.base_url}/{AiklyraClient.JOB_STATUS_ENDPOINT}/{job_id}"
    expected_headers = {
        "Content-Type": "application/json",
        "accept": "application/json"
    }
    mock_get.assert_called_once_with(expected_url, headers=expected_headers)


@patch("aiklyra.client.requests.get")
def test_check_job_status_analysis_error(mock_get, setup_client):
    """
    Test job status check when the response is malformed.
    """
    client, _ = setup_client
    job_id = "123456"

    mock_response = MagicMock()
    mock_response.status_code = 200
    # Simulate a response that cannot be parsed into a JobStatusResponse.
    mock_response.json.return_value = {"invalid_key": "unexpected_data"}
    mock_get.return_value = mock_response

    with pytest.raises(AnalysisError):
        client.check_job_status(job_id)


@patch("aiklyra.client.requests.get")
def test_check_job_status_api_error(mock_get, setup_client):
    """
    Test job status check when the API returns a non-200 status code.
    """
    client, _ = setup_client
    job_id = "123456"

    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.text = "Job not found"
    mock_get.return_value = mock_response

    with pytest.raises(AiklyraAPIError) as exc_info:
        client.check_job_status(job_id)

    assert "Error 404" in str(exc_info.value)
