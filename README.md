# Aiklyra Python Package

**Aiklyra** is a Python client library that provides a simple interface to your FastAPI-powered conversation analysis API. It allows developers to easily submit conversation data for clustering, analysis, and graph processing using an asynchronous workflow.

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

- **Asynchronous Analysis**: Submit conversation data for analysis and later retrieve detailed results via job status.
- **Graph Processing**: Construct, filter, and visualize directed graphs representing conversation flows.
- **Customizable Filters**: Apply graph filtering strategies like thresholding, top-K filtering, and advanced reconnecting filters.
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

1. **Configure the Client**  
   The client now uses asynchronous endpoints and does not require an API key. Simply specify the API's base URL.

2. **Import the Client**
   ```python
   from aiklyra.client import AiklyraClient
   ```

3. **Initialize the Client**
   ```python
   client = AiklyraClient(base_url="http://your-api-base-url")
   ```

4. **Submit Analysis & Retrieve Results**  
   The analysis workflow now occurs in two steps:
   - **Submit** your conversation data for analysis. This call returns a job ID.
   - **Check the job status** using the returned job ID to obtain the full analysis results.
   
   ```python
   # Submit conversation data for analysis
   submission = client.submit_analysis(
       conversation_data=your_conversation_data,
       min_clusters=5,
       max_clusters=10,
       top_k_nearest_to_centroid=10
   )
   
   # Later, check the job status to retrieve the analysis result:
   job_status = client.check_job_status(submission.job_id)
   # The actual analysis is available in the "result" field.
   analysis = job_status.result
   ```

---

## Example

Below is an example script that demonstrates the complete workflow:

```python
from aiklyra.client import AiklyraClient
from aiklyra.exceptions import AnalysisError, AiklyraAPIError
import time

def main():
    # Replace with your API's base URL
    base_url = "http://your-api-base-url"

    # Initialize the client (no API key required)
    client = AiklyraClient(base_url=base_url)

    # Example conversation data
    conversation_data = {
        "conversation_1": [
            {"role": "user", "content": "Hi, I need help with my account."},
            {"role": "assistant", "content": "Sure, please provide your account ID."},
            {"role": "user", "content": "It's 12345."}
        ],
        "conversation_2": [
            {"role": "user", "content": "Can I change my subscription plan?"},
            {"role": "assistant", "content": "Yes, you can change it from your settings."},
            {"role": "user", "content": "Great, thank you!"}
        ]
    }

    try:
        # Submit analysis job
        submission = client.submit_analysis(
            conversation_data=conversation_data,
            min_clusters=5,
            max_clusters=10,
            top_k_nearest_to_centroid=10
        )
        print(f"Job submitted. Job ID: {submission.job_id}")

        # Optionally, wait before checking job status (or poll periodically)
        time.sleep(2)

        # Check job status and retrieve analysis result
        job_status = client.check_job_status(submission.job_id)
        if job_status.status == "completed":
            analysis = job_status.result
            print("Analysis Result:")
            print("Transition Matrix:", analysis.transition_matrix)
            print("Intent by Cluster:", analysis.intent_by_cluster)
        else:
            print(f"Job status: {job_status.status}")

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

After obtaining the analysis result (a `ConversationFlowAnalysisResponse` object), you can process it into a directed graph:

```python
from aiklyra.graph.processor import GraphProcessor

# Assuming 'analysis' is your ConversationFlowAnalysisResponse instance
graph_processor = GraphProcessor(analysis)
graph = graph_processor.graph  # This is a NetworkX graph
```

### Graph Filtering

Apply filters to refine the graph. For example, you can use various filters to remove low-weight edges or retain only the top-K connections:

```python
from aiklyra.graph.filters import ThresholdFilter, TopKFilter

# Apply a threshold filter to remove edges below a certain weight.
threshold_filter = ThresholdFilter(threshold=0.3)
filtered_graph = graph_processor.filter_graph(threshold_filter)

# Or apply a top-K filter.
topk_filter = TopKFilter(top_k=3)
filtered_graph = graph_processor.filter_graph(topk_filter)
```

### Visualization

Visualize the graph using PyVis or NetworkX:

```python
# PyVis visualization (creates an HTML file)
graph_processor.plot_graph_html(file_name="conversation_flow.html")

# Alternatively, visualize using NetworkX's built-in methods
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
- **Coding Standards**: Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines.

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
