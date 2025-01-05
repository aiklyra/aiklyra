# Aethra Python Package 

**Aethra** is a Python client library that provides a simple interface to your FastAPI-powered conversation analysis API. It allows developers to easily submit conversation data for clustering and analysis.

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)

---

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Example](#example)
- [Testing](#testing)
- [Development](#development)
- [License](#license)
- [Contributing](#contributing)
- [Contact](#contact)

---

## Features

- **Simple API Client**: Quickly send conversation data for clustering and analysis.
- **Customizable Base URL**: Specify the API's base URL during client initialization.
- **Custom Exceptions**: Detailed exception classes (`InvalidAPIKeyError`, `InsufficientCreditsError`, etc.) for better error handling.
- **Pydantic Models**: Uses Pydantic for data validation and serialization.
- **Easy Integration**: Designed to integrate seamlessly with existing Python codebases.

---

## Installation

1. **Clone or Download the Repository** (if you haven’t already):
   ```bash
   git clone https://github.com/AethraData/aethra.git
   cd Aethra
   ```

2. **Install via `setup.py`**:
   ```bash
   pip install .
   ```
   or

3. **Editable Installation** (recommended for development):
   ```bash
   pip install -e .
   ```

> **Requirements**  
> - Python 3.8+  
> - [requests](https://pypi.org/project/requests/)  
> - [pydantic](https://pypi.org/project/pydantic/)  
> - [python-dotenv](https://pypi.org/project/python-dotenv/)

---

## Usage

### Basic Setup

1. **Obtain an API Key**  
   Make sure you have a valid API key for your FastAPI service. You need to provide this API key and the base URL of the API.

2. **Import the Client**
   ```python
   from aethra.client import AethraClient
   ```

3. **Initialize the Client**
   ```python
   client = AethraClient(api_key="your_api_key_here", base_url="http://your-api-base-url")
   ```

---

## Example

Below is a simple script that demonstrates sending a conversation for analysis:

```python
from aethra.client import AethraClient
from aethra.exceptions import (
    InvalidAPIKeyError,
    InsufficientCreditsError,
    AnalysisError,
    AethraAPIError
)

def main():
    # Replace with your actual API key and base URL
    api_key = "your_api_key_here"
    base_url = "base_url"

    # Initialize the client
    client = AethraClient(api_key=api_key, base_url=base_url)

    # Example conversation data
    conversation_data = {
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

    try:
        response = client.analyse(
            conversation_data=conversation_data,
            min_clusters=5,
            max_clusters=10,
            embedding_model="text-embedding-ada-002",
            top_k_nearest_to_centroid=10,
            tau=0.1
        )
        print("Analysis Result:")
        print(response)

    except InvalidAPIKeyError:
        print("Invalid API Key provided.")
    except InsufficientCreditsError:
        print("Insufficient credits for analysis.")
    except AnalysisError as e:
        print(f"Analysis failed: {e}")
    except AethraAPIError as e:
        print(f"API Error: {e}")

if __name__ == "__main__":
    main()
```

Run the script:

```bash
python example_usage.py
```

---

## Testing

1. **Install Development Dependencies** (if you have a `requirements-dev.txt` or similar):
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Tests**:
   ```bash
   python -m unittest discover tests
   ```
   or
   ```bash
   python ./tests/test_client.py
   ```
   You should see output indicating successful tests or any failures with detailed information.

---

## Development

- **Branching**: Use feature branches for new features or bug fixes.  
- **Pull Requests**: Open a PR with a clear description and pass all tests before merging.  
- **Coding Standards**: Follow PEP 8 style guidelines.

---

## License

This project is licensed under the [Apache License 2.0](LICENSE).  
You are free to use, distribute, and modify the library under the terms of this license.

---

## Contributing

We welcome contributions! To get started:

1. Fork the repository  
2. Create a feature branch (`git checkout -b feature/my-feature`)  
3. Commit your changes (`git commit -m "Add my feature"`)  
4. Push to the branch (`git push origin feature/my-feature`)  
5. Open a Pull Request on GitHub

Please ensure your contributions include tests, documentation, and follow the coding standards described above.

---

## Contact

- **Author**: Your Name (achref.benammar@ieee.org)  
- **GitHub**: [@achrefbenammar404](https://github.com/achrefbenammar404)

If you have questions, suggestions, or issues, feel free to open an issue on the GitHub repository or reach out by email!

---

_Thank you for using Aethra! We look forward to seeing how you integrate it into your projects._
