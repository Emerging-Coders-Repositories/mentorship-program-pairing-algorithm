# Mentor Matching Program

This project implements a mentor-mentee matching system for Northwestern University's Emerging Coders Student Organinazation. If you are unaware about Emerging Coders, here is some background about us:

Emerging Coders is a community for FGLI (First-generation, Low-income) students who are interested in Tech. Our purpose is to enable students in the club improve their skills (e.g., coding projects, networking etc.), provide mentorship and resources throughout your college experience, and to create meaningful projects.

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

2. Run the `pairing_matching` script:

   ```
   python pairing_matching.py
   ```

3. The program will generate a `mentorship_matches.csv` file in the `data/` directory with the matching results.

## Project Structure

- `pairing_matching`: The main script containing all the logic for data parsing, matching, and output generation.
- `data/`: Directory containing input and output CSV files.
- `requirements.txt`: List of Python package dependencies.
- `.venv/`: Virtual environment directory.

## Customization

You can modify the `calculate_similarity` function in `pairing_matching.py` to adjust the weighting of different factors in the matching process.

## Contributing

Contributions to improve the matching algorithm or add new features are welcome. Please fork the repository and submit a pull request with your changes.
