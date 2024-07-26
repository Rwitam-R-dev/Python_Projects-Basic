import random

def print_welcome_message():
    print("Welcome to the Number Guessing Game!")
    print("I'm thinking of a number between 1 and 100.")

def get_difficulty():
    while True:
        difficulty = input("Choose a difficulty (easy, medium, hard): ").lower()
        if difficulty == 'easy':
            return 1, 50
        elif difficulty == 'medium':
            return 1, 100
        elif difficulty == 'hard':
            return 1, 200
        else:
            print("Invalid choice. Please select 'easy', 'medium', or 'hard'.")

def get_guess():
    while True:
        try:
            guess = int(input("Enter your guess: "))
            return guess
        except ValueError:
            print("Invalid input. Please enter a number.")

def play_game():
    min_number, max_number = get_difficulty()
    target_number = random.randint(min_number, max_number)
    attempts = 0

    print(f"Guess the number between {min_number} and {max_number}.")

    while True:
        guess = get_guess()
        attempts += 1

        if guess < target_number:
            print("Too low! Try again.")
        elif guess > target_number:
            print("Too high! Try again.")
        else:
            print(f"Congratulations! You guessed the number in {attempts} attempts.")
            break

def main():
    print_welcome_message()
    
    while True:
        play_game()
        play_again = input("Do you want to play again? (yes/no): ").lower()
        if play_again != 'yes':
            print("Thanks for playing! Goodbye.")
            break

if __name__ == "__main__":
    main()
