## Instructions


1. Ensure that you have python 3.11 installed in your system.
2. Create a virtual environment in the root directory of the api
    ```
    python -m venv .venv
    ```
3. Activate the virtual environment
    ```
    # for linux/wsl
    source .venv/bin/activate
    ```
4. Install the requirements
    ```
    pip install -r requirements.txt
    ```
5. Start the API server to start accepting requests from frontend
    ```
    uvicorn app:app --reload --host 0.0.0.0
    ```