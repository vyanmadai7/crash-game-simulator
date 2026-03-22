import random
import time
import numpy as np
import matplotlib.pyplot as plt

BALANCE = 100.0
history = [] 

def generate_crash_point():
    r = random.random()
    if r <= 0.05:
        return 1.0
    return round(1 / (1 - random.uniform(0.0, 0.97)), 2)

def safe_input(prompt):
    try:
        return input(prompt).strip().lower()
    except KeyboardInterrupt:
        print("\nExiting game")
        exit()

def run_round(bet: float) -> float:
    crash_at = generate_crash_point()
    print("\nTakeOff")

    multiplier = 1.0

    while multiplier < crash_at:
        multiplier = round(multiplier + random.uniform(0.01, 0.15), 2)
        multiplier = min(multiplier, crash_at)

        print(f"x: {multiplier:.2f}", end="\r")
        time.sleep(0.2)

        if multiplier > 1.1:
            answer = safe_input(f"\n[{multiplier:.2f}] Cash out? (y/n): ")
            if answer == 'y':
                winnings = round(bet * multiplier, 2)
                print(f"Cashed out → ${winnings:.2f}")
                return winnings

    print(f"\nCrashed at {crash_at:.2f}x")
    print(f"Lost ${bet:.2f}")
    return 0.0

def show_stats():
    arr = np.array(history)
    rounds = np.arange(1, len(arr) + 1)
    cumulative = np.cumsum(arr)

    plt.figure()
    plt.plot(rounds, cumulative)
    plt.xlabel("Rounds")
    plt.ylabel("Total Profit/Loss ($)")
    plt.title("Game Performance")
    plt.grid()
    plt.show()

def main():
    global BALANCE

    print("=" * 15)
    print("   AVIATOR PRO")
    print("=" * 15)

    round_count = 0

    while True:
        print(f"\nBalance: ${BALANCE:.2f}")

        try:
            bet = float(safe_input("Enter bet: "))
        except ValueError:
            print("Invalid amount")
            continue

        if bet <= 0 or bet > BALANCE:
            print(f"Enter 0 < bet ≤ ${BALANCE:.2f}")
            continue

        BALANCE -= bet
        winnings = run_round(bet)
        BALANCE += winnings
        BALANCE = round(BALANCE, 2)

        profit = winnings - bet
        history.append(profit)
        round_count += 1

        print(f"Round Result: {'+' if profit>=0 else ''}{profit:.2f}")

        if round_count % 10 == 0:
            print("\nShowing stats after 10 rounds...")
            show_stats()

        if BALANCE <= 0:
            print("Game Over")
            show_stats()
            break

        again = safe_input("Play again? (y/n): ")
        if again != 'y':
            show_stats()
            print("Exiting game")
            break

if __name__ == "__main__":
    main()
