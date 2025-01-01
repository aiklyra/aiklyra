import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.join(""))

import unittest
from unittest.mock import patch
from convolens.client import ConvoLensClient
from convolens.exceptions import (
    InvalidAPIKeyError,
    InsufficientCreditsError,
    AnalysisError,
    ConvoLensAPIError
)
from convolens.models import ConversationFlowAnalysisResponse

class TestConvoLensClient(unittest.TestCase):
    def setUp(self):
        self.api_key = "test_api_key"
        self.client = ConvoLensClient(api_key=self.api_key, base_url="http://localhost:8002")
        self.conversation_data = {
            "conversation_1": [
                {"role": "user", "content": "Hi, I need help with my account."},
                {"role": "agent", "content": "Sure, could you please provide me with your account ID?"},
                {"role": "user", "content": "It's 12345."}
            ],
            "conversation_2": [
                {"role": "user", "content": "Can I change my subscription plan?"},
                {"role": "agent", "content": "Yes, you can change it from the settings page. Would you like me to guide you through the process?"},
                {"role": "user", "content": "That would be helpful. Thank you."}
            ],
            "conversation_3": [
                {"role": "user", "content": "How can I reset my password?"},
                {"role": "agent", "content": "To reset your password, click on 'Forgot Password' on the login page and follow the instructions."},
                {"role": "user", "content": "Got it, thanks."}
            ]
        }

    @patch('convolens.client.requests.post')
    def test_analyse_success(self, mock_post):
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "transition_matrix": [[0.1, 0.9], [0.2, 0.8]],
            "intent_by_cluster": {0: "Account Assistance", 1: "Subscription Management"}
        }
        mock_post.return_value = mock_response

        response = self.client.analyse(conversation_data=self.conversation_data)
        self.assertIsInstance(response, ConversationFlowAnalysisResponse)
        self.assertEqual(response.transition_matrix, [[0.1, 0.9], [0.2, 0.8]])
        self.assertEqual(response.intent_by_cluster, {0: "Account Assistance", 1: "Subscription Management"})

    @patch('convolens.client.requests.post')
    def test_analyse_invalid_api_key(self, mock_post):
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 403
        mock_response.json.return_value = {"detail": "Invalid API Key"}
        mock_post.return_value = mock_response

        with self.assertRaises(InvalidAPIKeyError):
            self.client.analyse(conversation_data=self.conversation_data)

    @patch('convolens.client.requests.post')
    def test_analyse_insufficient_credits(self, mock_post):
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 403
        mock_response.json.return_value = {"detail": "Insufficient credits"}
        mock_post.return_value = mock_response

        with self.assertRaises(InsufficientCreditsError):
            self.client.analyse(conversation_data=self.conversation_data)

    @patch('convolens.client.requests.post')
    def test_analyse_other_error(self, mock_post):
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_post.return_value = mock_response

        with self.assertRaises(ConvoLensAPIError):
            self.client.analyse(conversation_data=self.conversation_data)

if __name__ == '__main__':
    unittest.main()
