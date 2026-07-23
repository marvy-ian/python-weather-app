# Contributing to Weather App

Thanks for your interest in contributing! This is a small learning project, so contributions of any size are welcome — bug fixes, new features, documentation improvements, or just suggestions.

## Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/<your-username>/weather-app.git
   cd weather-app
   ```
3. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run the app to make sure everything works:
   ```bash
   python weather_app.py
   ```

## Making Changes

1. Create a new branch for your change:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Make your changes, keeping the code style consistent with the rest of the project (PEP 8 where reasonable).
3. Test your changes manually by running the app.
4. Commit with a clear, descriptive message:
   ```bash
   git commit -m "Add Fahrenheit/Celsius toggle"
   ```
5. Push to your fork and open a Pull Request against `main`.

## Pull Request Guidelines

- Keep PRs focused — one feature or fix per PR is easier to review.
- Describe **what** changed and **why** in the PR description.
- Include a screenshot or GIF if the change affects the UI.
- Make sure the app still runs without errors before submitting.

## Reporting Bugs

If you find a bug, please open an issue and include:
- Steps to reproduce
- What you expected to happen
- What actually happened
- Your OS and Python version

## Suggesting Features

Feature ideas are welcome! Open an issue describing:
- The problem the feature solves
- How you imagine it working
- Any relevant examples or references

## Ideas for Contributions

- Add a °C/°F unit toggle
- Add a multi-day forecast view
- Add city search history or favorites
- Improve error handling for edge cases (e.g. ambiguous city names)
- Add unit tests
- Improve UI/UX styling

## Code of Conduct

Please note that this project follows a [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you agree to uphold it.

## Questions?

Feel free to open an issue if anything here is unclear — happy to help.