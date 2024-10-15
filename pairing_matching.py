import csv
import numpy as np
from dataclasses import dataclass, field
from typing import Set, List, Tuple, FrozenSet
from scipy.optimize import linear_sum_assignment
import copy

@dataclass
class Student:
    name: str
    email: str
    pronouns: str
    year: str
    major: str
    role: str
    timezone: float
    time_commitment: float
    races: FrozenSet[str] = field(default_factory=frozenset)

@dataclass
class Mentor:
    name: str
    email: str
    pronouns: str
    year: str
    major: str
    role: str
    timezone: float
    time_commitment: int 
    num_mentees: int
    preferred_mentee_major: str
    mentoring_term: str 
    races: FrozenSet[str] = field(default_factory=frozenset)
    expertise_areas: Set[str] = field(default_factory=set)
    support_areas: Set[str] = field(default_factory=set)
    communication_methods: Set[str] = field(default_factory=set)

    def __hash__(self):
        return hash((self.name, self.email))

@dataclass(frozen=True)
class Mentee:
    name: str
    email: str
    pronouns: str
    year: str
    major: str
    role: str
    timezone: float
    time_commitment: int 
    preferred_mentor_match: str  
    desired_mentoring_term: str  #
    races: FrozenSet[str] = field(default_factory=frozenset)
    desired_support_areas: Set[str] = field(default_factory=set)
    preferred_comm_methods: Set[str] = field(default_factory=set)

    def __hash__(self):
        return hash((self.name, self.email))


def parse_time_commitment(time_str: str) -> float:
    parts = time_str.split()
    if len(parts) >= 1:
        range_parts = parts[0].split('-')
        if len(range_parts) == 2:
            return (float(range_parts[0]) + float(range_parts[1])) / 2
        elif len(range_parts) == 1:
            if range_parts[0].endswith('+'):
                return float(range_parts[0][:-1]) 
            return float(range_parts[0])
    return 0 

def read_csv_data(filename: str) -> Tuple[List[Mentor], List[Mentee]]:
    mentors = []
    mentees = []
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            role = row['Please select wether you want to be a mentor or mentee'].strip().lower()
            
            common_data = {
                "name": f"{row['First Name']} {row['Last Name']}",
                "email": row['Email Address'],
                "pronouns": row['Pronouns'],
                "year": row['Current Grade Level'],
                "major": row['Current Major'],
                "role": role,
                "timezone": 0,
                "time_commitment": parse_time_commitment(row['How many times would you expect to meet with your mentee/mentees ']),
                "races": frozenset(),
            }
            
            if role == 'mentor':
                mentor_data = {
                    **common_data,
                    "num_mentees": int(parse_time_commitment(row['How many mentees would you prefer supporting?'])),
                    "preferred_mentee_major": row['Would you prefer if your mentee is in the same school & major as you?'],
                    "mentoring_term": row.get('Would you prefer short-term or long-term mentoring relationships?', 'medium'),
                    "expertise_areas": set(),
                    "support_areas": set(),
                    "communication_methods": set()
                }
                mentors.append(Mentor(**mentor_data))
            elif role == 'mentee':
                mentee_data = {
                    **common_data,
                    "preferred_mentor_match": row.get('Would you prefer if your mentor is in the same school & major as you?', 'no_preference'),
                    "desired_mentoring_term": row.get('Would you prefer short-term or long-term mentoring relationships?', 'medium'),
                    "desired_support_areas": set(),
                    "preferred_comm_methods": set()
                }
                mentees.append(Mentee(**mentee_data))
            else:
                print(f"Warning: Unrecognized role '{role}' for {common_data['name']}")
    
    print(f"*** Debug: Read {len(mentors)} mentors and {len(mentees)} mentees from CSV ***")
    return mentors, mentees


def calculate_similarity(mentor: Mentor, mentee: Mentee, iteration: int) -> float:
    similarity = 0

    if mentee.preferred_mentor_match == 'same_school_and_major':
        if mentor.major == mentee.major and mentor.school == mentee.school:
            similarity += 3
    elif mentee.preferred_mentor_match == 'same_major':
        if mentor.major == mentee.major:
            similarity += 2
    elif mentee.preferred_mentor_match == 'same_school':
        if mentor.school == mentee.school:
            similarity += 2
    elif mentee.preferred_mentor_match == 'no_preference':
        similarity += 1

    if mentor.time_commitment == mentee.time_commitment:
        similarity += 2
    elif abs(mentor.time_commitment - mentee.time_commitment) == 1:
        similarity += 1

    support_overlap = len(mentor.expertise_areas.intersection(mentee.desired_support_areas))
    similarity += support_overlap * 2 

    comm_method_overlap = len(mentor.communication_methods.intersection(mentee.preferred_comm_methods))
    similarity += comm_method_overlap

    if mentor.mentoring_term == mentee.desired_mentoring_term:
        similarity += 3
    elif (mentor.mentoring_term == 'long' and mentee.desired_mentoring_term in ['medium', 'short']) or \
         (mentor.mentoring_term == 'medium' and mentee.desired_mentoring_term == 'short'):
        similarity += 1


    year_values = {"First-year": 1, "Second-year": 2, "Junior": 3, "Senior": 4, "Masters/Graduate": 5}
    year_diff = year_values.get(mentor.year, 0) - year_values.get(mentee.year, 0)
    if year_diff > 0:
        similarity += 1

    if iteration == 0:
        similarity *= 2
    elif iteration == 1:
        similarity *= 1.5

    return similarity

def create_cost_matrix(mentors: List[Mentor], mentees: List[Mentee], mentor_loads: dict, iteration: int) -> np.ndarray:
    cost_matrix = np.zeros((len(mentors), len(mentees)))
    for i, mentor in enumerate(mentors):
        for j, mentee in enumerate(mentees):
            similarity = calculate_similarity(mentor, mentee, iteration)
            capacity_penalty = max(0, mentor_loads[mentor.email] - mentor.num_mentees + 1) * 0.5
            cost_matrix[i, j] = -similarity + capacity_penalty
    return cost_matrix


def create_similarity_matrix(mentors: List[Mentor], mentees: List[Mentee]) -> np.ndarray:
    similarity_matrix = np.zeros((len(mentors), len(mentees)))
    for i, mentor in enumerate(mentors):
        for j, mentee in enumerate(mentees):
            similarity_matrix[i, j] = calculate_similarity(mentor, mentee)
    return similarity_matrix

def match_mentors_and_mentees(mentors: List[Mentor], mentees: List[Mentee], max_iterations: int = 3) -> List[Tuple[Mentor, Mentee]]:
    original_mentors = mentors.copy()
    all_matches = []
    mentor_loads = {mentor.email: 0 for mentor in mentors}

    for iteration in range(max_iterations):
        cost_matrix = create_cost_matrix(mentors, mentees, mentor_loads, iteration)
        mentor_indices, mentee_indices = linear_sum_assignment(cost_matrix)

        for mentor_idx, mentee_idx in zip(mentor_indices, mentee_indices):
            mentor = mentors[mentor_idx]
            mentee = mentees[mentee_idx]
            all_matches.append((mentor, mentee))
            mentor_loads[mentor.email] += 1

        mentees = [m for i, m in enumerate(mentees) if i not in mentee_indices]

        if not mentees:
            break

    while mentees:
        mentee = mentees.pop(0)
        least_loaded_mentor = min(original_mentors, key=lambda m: mentor_loads[m.email])
        all_matches.append((least_loaded_mentor, mentee))
        mentor_loads[least_loaded_mentor.email] += 1

    return all_matches

def save_matches_to_csv(matches: List[Tuple[Mentor, Mentee]], filename: str):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Mentor Name', 'Mentor Email', 'Mentee Name', 'Mentee Email'])
        for mentor, mentee in matches:
            writer.writerow([mentor.name, mentor.email, mentee.name, mentee.email])


def print_matching_statistics(matches: List[Tuple[Mentor, Mentee]], original_mentors: List[Mentor], original_mentees: List[Mentee]):
    print(f"Total mentors: {len(original_mentors)}")
    print(f"Total mentees: {len(original_mentees)}")
    print(f"Matched pairs: {len(matches)}")

    mentor_match_counts = {mentor.email: 0 for mentor in original_mentors}
    for mentor, _ in matches:
        mentor_match_counts[mentor.email] += 1

    print("\nMentor loads:")
    for mentor in original_mentors:
        print(f"  - {mentor.name}: Suggested capacity {mentor.num_mentees}, Actual matches {mentor_match_counts[mentor.email]}")

    overloaded_mentors = [mentor for mentor in original_mentors if mentor_match_counts[mentor.email] > mentor.num_mentees]
    if overloaded_mentors:
        print("\nMentors matched with more mentees than their suggested capacity:")
        for mentor in overloaded_mentors:
            print(f"  - {mentor.name}: Suggested capacity {mentor.num_mentees}, Actual matches {mentor_match_counts[mentor.email]}")

def save_matches_to_csv(matches: List[Tuple[Mentor, Mentee]], unmatched_mentees: List[Mentee], filename: str):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Mentor Name', 'Mentor Email', 'Mentee Name', 'Mentee Email'])
        for mentor, mentee in matches:
            writer.writerow([mentor.name, mentor.email, mentee.name, mentee.email])
        
        if unmatched_mentees:
            writer.writerow([])
            writer.writerow(['Unmatched Mentees'])
            for mentee in unmatched_mentees:
                writer.writerow([mentee.name, mentee.email])

if __name__ == "__main__":
    mentors, mentees = read_csv_data("data/mentor-program-responses.csv")
    matches = match_mentors_and_mentees(mentors, mentees)
    save_matches_to_csv(matches, [], "data/mentorship_matches.csv")
    print_matching_statistics(matches, mentors, mentees)