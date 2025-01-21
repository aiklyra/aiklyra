# Aiklyra Python Package 

**Aiklyra** is a Python client library that provides a simple interface to your FastAPI-powered conversation analysis API. It allows developers to easily submit conversation data for clustering, analysis, and graph processing.

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)

---

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Example](#example)
- [Graph Processing and Visualization](#graph-processing-and-visualization)
- [Testing](#testing)
- [Development](#development)
- [License](#license)
- [Contributing](#contributing)
- [Contact](#contact)

---

## Features

- **Simple API Client**: Quickly send conversation data for clustering and analysis.
- **Graph Processing**: Construct, filter, and visualize directed graphs representing conversation flows.
- **Customizable Filters**: Apply graph filtering strategies like thresholding, top-K filtering, and advanced reconnecting filters.
- **Customizable Base URL**: Specify the API's base URL during client initialization.
- **Custom Exceptions**: Detailed exception classes (`InvalidAPIKeyError`, `InsufficientCreditsError`, etc.) for better error handling.
- **Pydantic Models**: Uses Pydantic for data validation and serialization.
- **Easy Integration**: Designed to integrate seamlessly with existing Python codebases.

---

## Installation

1. **Clone or Download the Repository**:
   ```bash
   git clone https://github.com/AiklyraData/aiklyra.git
   cd Aiklyra
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
> - [networkx](https://pypi.org/project/networkx/)  
> - [pyvis](https://pypi.org/project/pyvis/)

---

## Usage

### Basic Setup

1. **Obtain an API Key**  
   Make sure you have a valid API key for your FastAPI service. You need to provide this API key and the base URL of the API.

2. **Import the Client**
   ```python
   from aiklyra.client import AiklyraClient
   ```

3. **Initialize the Client**
   ```python
   client = AiklyraClient(api_key="your_api_key_here", base_url="http://your-api-base-url")
   ```

---

## Example

Below is a simple script that demonstrates sending a conversation for analysis:

```python
from aiklyra.client import AiklyraClient
from aiklyra.exceptions import (
    InvalidAPIKeyError,
    InsufficientCreditsError,
    AnalysisError,
    AiklyraAPIError
)

def main():
    # Replace with your actual API key and base URL
    api_key = "your_api_key_here"
    base_url = "http://your-api-base-url"

    # Initialize the client
    client = AiklyraClient(api_key=api_key, base_url=base_url)

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
        ]
    }

    try:
        # Perform analysis
        response = client.analyse(
            conversation_data=conversation_data,
            min_clusters=5,
            max_clusters=10,
            top_k_nearest_to_centroid=10
        )
        print("Analysis Result:")
        print(response)

    except InvalidAPIKeyError:
        print("Invalid API Key provided.")
    except InsufficientCreditsError:
        print("Insufficient credits for analysis.")
    except AnalysisError as e:
        print(f"Analysis failed: {e}")
    except AiklyraAPIError as e:
        print(f"API Error: {e}")

if __name__ == "__main__":
    main()
```

Run the script:

```bash
python example_usage.py
```

---

## Graph Processing and Visualization

### Graph Construction

The analysis response can be processed into a directed graph using `GraphProcessor`:

```python
from aiklyra.graph.processor import GraphProcessor

# Assuming 'response' is a ConversationFlowAnalysisResponse object
graph_processor = GraphProcessor(analysis=response)

# Access the constructed graph
graph = graph_processor.graph
```

### Graph Filtering

Apply filters to refine the graph. Available filters include:
- `ThresholdFilter`: Removes edges with weights below a specified threshold.
- `TopKFilter`: Retains only the top-K outgoing edges for each node.
- `FRFilter`: Advanced filtering strategy that removes cycles and reconnects subgraphs.

Example:

```python
from aiklyra.graph.filters import ThresholdFilter, TopKFilter

# Apply a threshold filter
threshold_filter = ThresholdFilter(threshold=0.3)
filtered_graph = graph_processor.filter_graph(threshold_filter)

# Apply a top-K filter
topk_filter = TopKFilter(top_k=3)
filtered_graph = graph_processor.filter_graph(topk_filter)
```

### Visualization

Visualize the graph using PyVis or NetworkX:

```python
# PyVis visualization
graph_processor.plot_graph_html(file_name="conversation_flow")

# NetworkX visualization
graph_processor.visualize_graph()
```

---

## Testing

1. **Install Development Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Tests**:
   ```bash
   python -m unittest discover tests
   ```
   or
   ```bash
   pytest
   ```

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

_Thank you for using Aiklyra! We look forward to seeing how you integrate it into your projects._
