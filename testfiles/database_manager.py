import pandas as pd 
import os
import regex as re

def initialize_csv(filename = "courses.csv"):
    # definition of columns based on project requirements
    columns = [
        "Title", "Provider", "Category", "Level", "Cost", "Duration", "Language"
    ]

    if not os.path.exists(filename):
        df = pd.DataFrame(columns=columns)
        df.to_csv(filename, index=False)
        print(f"Created {filename}")
    else:
        print(f"{filename} already exists.")

def add_course_to_csv(course_data, filename="courses.csv"):
    # course_data should be a dictionary
    df = pd.DataFrame([course_data])
    # mode='a' means Append (add to the end)
    # header=False means don't write the column names again
    df.to_csv(filename, mode='a', index=False, header=False)

# Testing it out 
if __name__ == "__main__":
    initialize_csv()

    test_course = {
        "Title": "Αρχές γλωσσών προγραμματισμού και μεταφραστών",
        "Provider": "University of Patras",
        "Level": "Beginner",
        "Cost": 0.0,
        "Duration": 10, # Cost and Duration must be numbers so opeartions can be performed on them later.
        "Language": "Greek"
    }

    add_course_to_csv(test_course)
    print("Test course added!")

