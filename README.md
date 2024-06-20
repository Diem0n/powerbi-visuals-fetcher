# PowerBI Visuals Fetcher

This script fetches the top 1000 PowerBI visuals from the Microsoft Store and extracts various metadata, including download URLs, using multithreading to speed up the process.

## Features

- Fetch metadata for PowerBI visuals from the Microsoft Store.
- Multithreaded fetching of download URLs for improved performance.
- JSON output of parsed data.

## Requirements

- Python 3.7 or higher

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/diem0n/powerbi-visuals-fetcher.git
    cd powerbi-visuals-fetcher
    ```

2. Create a virtual environment:

    ```sh
    python -m venv venv
    ```

3. Activate the virtual environment:

    - On Windows:

      ```sh
      .\venv\Scripts\activate
      ```

    - On macOS and Linux:

      ```sh
      source venv/bin/activate
      ```

4. Install the required packages:

    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Run the script:

    ```sh
    python main.py
    ```

2. The script will output a file named `parsed.json` with the fetched and parsed data.

## Configuration

The configuration is set within the script, including the base URL, query parameters, output file, and the number of threads. You can adjust these settings in the `config` dictionary in the `main.py` file.

## Logging

The script uses the `logging` module to provide detailed information about the execution process. The logs will be printed to the console.

## Contributing

Feel free to fork the repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License.
