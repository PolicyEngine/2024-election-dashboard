import os
from nationwide_impacts.calculator.microsim import calculate_all_reform_impacts


def generate_results():
    # Create data directory if it doesn't exist
    if not os.path.exists("data"):
        os.makedirs("data")

    # Calculate all reform impacts
    results_df = calculate_all_reform_impacts()
    print("Calculations complete!")


if __name__ == "__main__":
    generate_results()
