# Formula One AI

This project is used to answer any questions about Formula 1. It uses LLMs and an F1 data API to respond to user queries.

## Prerequisites

This project requires Python 3.10 or newer. Please ensure that you have the correct Python version installed before proceeding.

## Installation

Here are the steps to set up this project on your local machine.

1. Clone the repository to your local machine:

```bash
git clone https://github.com/denniszubov/formula-one-ai.git
cd formula-one-ai
```

2. Create a virtual environment (optional, but recommended):

```bash
python -m venv venv
```

Activate the virtual environment:

- On Windows:
```bash
.\venv\Scripts\activate
```

- On Unix or MacOS:
```bash
source venv/bin/activate
```

3. Install the required packages:

```bash
pip install -r requirements.txt
```

## Pre-commit Setup

This project uses pre-commit to manage pre-commit hooks. These hooks help to identify simple issues before submission to code review. We use pre-commit to ensure that your code is properly formatted and doesn't contain any glaring issues.

Follow these steps to set up pre-commit:

1. Install pre-commit. If you've followed the above steps and activated your virtual environment, run:

```bash
pip install pre-commit
```

2. Set up the git hook scripts with:

```bash
pre-commit install
```

Now, pre-commit will run automatically on `git commit`. If issues are found during the pre-commit checks, the commit will be canceled and you'll need to fix these issues before committing again.

### Keeping pre-commit Updated
It's important to keep your pre-commit hooks updated. You can do this by running:

```bash
pre-commit autoupdate
```

This command will automatically update the hook versions in your .pre-commit-config.yaml to their latest versions.

## Environment Variables Setup

This project uses the OpenAI API for some of its operations and requires an API key, which should be stored securely and not exposed in your codebase. To manage this, we use environment variables stored in a `.env` file.

Please follow these steps to set up your `.env` file:

1. Create a file named `.env` in the root directory of the project.
2. Open the `.env` file and add the following line:

```
OPENAI_API_KEY=your_api_key_here
```

Replace `your_api_key_here` with your actual OpenAI API key.

Please note that the `.env` file is listed in the `.gitignore` file and will not be tracked by Git. This is intentional to ensure the security of your API key.

## Common Issues

- **Issue:** If you encounter an error saying the `OPENAI_API_KEY` environment variable is not set, check your `.env` file to ensure the key is properly set.
- **Issue:** If pre-commit fails and you're not sure why, make sure you have installed all the required packages with `pip install -r requirements.txt` and that your pre-commit hooks are updated (`pre-commit autoupdate`).
- **Issue:** If you're finding that pre-commit is not running when you make a commit, ensure that you've run `pre-commit install`.
- **Issue:** If you're seeing a "Python version not supported" error, check your Python version with `python --version`. This project requires Python 3.7 or newer.

## Usage

Once you have successfully set up the project, you can run it with:

```bash
streamlit run frontend.py
```

Then, you can start asking questions about F1 to the bot.

Enjoy!
