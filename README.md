# Mentor Matching Program

This project implements a mentor-mentee matching system for educational or professional mentorship programs. It uses an algorithm to optimally pair mentors with mentees based on various criteria and preferences.

## Features

- Reads mentor and mentee data from a CSV file
- Matches mentors and mentees based on multiple factors:
  - Major/school preferences
  - Time commitment
  - Expertise and support areas
  - Communication methods
  - Mentoring term preferences
- Handles multiple iterations to optimize matches
- Produces a CSV output of matched pairs
- Provides matching statistics and identifies overloaded mentors

## Requirements

This project uses Python 3 and requires the following libraries:

- numpy
- dataclasses
- typing
- scipy

A virtual environment (.venv) is set up at the root of the project.

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/yourusername/mentor-matching-program.git
   cd mentor-matching-program
   ```

2. Activate the virtual environment:

   ```
   source .venv/bin/activate  # On Unix or MacOS
   .venv\Scripts\activate     # On Windows
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Ensure your input data is in a CSV file named `mentor-program-responses.csv` in the `data/` directory.

2. Run the main script:

   ```
   python main.py
   ```

3. The program will generate a `mentorship_matches.csv` file in the `data/` directory with the matching results.

## Project Structure

- `main.py`: The main script containing all the logic for data parsing, matching, and output generation.
- `data/`: Directory containing input and output CSV files.
- `requirements.txt`: List of Python package dependencies.
- `.venv/`: Virtual environment directory.

## Customization

You can modify the `calculate_similarity` function in `main.py` to adjust the weighting of different factors in the matching process.

## Contributing

Contributions to improve the matching algorithm or add new features are welcome. Please fork the repository and submit a pull request with your changes.
