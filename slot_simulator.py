import random
import math
import matplotlib.pyplot as plt

# ==============================
# CONFIG
# ==============================
TOTAL_BET = 1.0

reels = [
    ["A"]*20 + ["K"]*18 + ["Q"]*16 + ["J"]*14 + ["10"]*12 + ["9"]*10 + ["W"]*6 + ["S"]*2,
    ["A"]*18 + ["K"]*18 + ["Q"]*16 + ["J"]*14 + ["10"]*12 + ["9"]*12 + ["W"]*6 + ["S"]*2,
    ["A"]*16 + ["K"]*16 + ["Q"]*16 + ["J"]*16 + ["10"]*14 + ["9"]*12 + ["W"]*6 + ["S"]*2,
    ["A"]*18 + ["K"]*16 + ["Q"]*14 + ["J"]*14 + ["10"]*14 + ["9"]*14 + ["W"]*6 + ["S"]*2,
    ["A"]*14 + ["K"]*14 + ["Q"]*14 + ["J"]*14 + ["10"]*18 + ["9"]*18 + ["W"]*6 + ["S"]*2,
]

paytable = {
    "A":  {3: 10,  4: 37,  5: 175},
    "K":  {3: 9,   4: 27,  5: 132},
    "Q":  {3: 7,   4: 19,  5: 100},
    "J":  {3: 5,   4: 14,  5: 67},
    "10": {3: 3,   4: 10,  5: 47},
    "9":  {3: 2,   4: 7,   5: 32},
    "W":  {5: 870}
}

paylines = [
    [1,1,1,1,1], [0,0,0,0,0], [2,2,2,2,2], [0,1,2,1,0], [2,1,0,1,2],
    [0,0,1,0,0], [2,2,1,2,2], [1,0,1,0,1], [1,2,1,2,1], [0,1,1,1,0]
]

BET_PER_LINE = TOTAL_BET / len(paylines)

# ==============================
# CORE LOGIC
# ==============================

def spin():
    grid = []
    for reel in reels:
        stop = random.randint(0, len(reel)-1)
        grid.append([
            reel[(stop-1) % len(reel)],
            reel[stop],
            reel[(stop+1) % len(reel)]
        ])
    return grid

def get_line(grid, line):
    return [grid[i][line[i]] for i in range(5)]

def evaluate_line(symbols, bet):
    best_win = 0.0
    for candidate in paytable.keys():
        count = 0
        for s in symbols:
            if s == candidate or s == "W":
                count += 1
            else:
                break
        if count in paytable[candidate]:
            win = paytable[candidate][count] * bet
            best_win = max(best_win, win)
    return best_win

def evaluate_spin(grid):
    total = 0.0
    for line in paylines:
        symbols = get_line(grid, line)
        total += evaluate_line(symbols, BET_PER_LINE)
    return total

def count_scatters(grid):
    return sum(s=="S" for reel in grid for s in reel)

def get_free_spins(scatter_count):
    if scatter_count == 3: return 5
    elif scatter_count == 4: return 7
    elif scatter_count >= 5: return 10
    return 0

def simulate_free_spins(n):
    total_win = 0.0
    spins_remaining = n
    while spins_remaining > 0:
        grid = spin()
        win = evaluate_spin(grid)
        total_win += win
        scatters = count_scatters(grid)
        retrigger = get_free_spins(scatters)
        spins_remaining += retrigger - 1
    return total_win

# ==============================
# SIMULATION + METRICS
# ==============================

def simulate(spins=100_000):
    total_bet = spins * TOTAL_BET
    wins = []
    hit_count = 0

    for _ in range(spins):
        grid = spin()
        spin_win = evaluate_spin(grid)

        scatters = count_scatters(grid)
        fs = get_free_spins(scatters)
        if fs > 0:
            spin_win += simulate_free_spins(fs)

        if spin_win > 0:
            hit_count += 1
        wins.append(spin_win)

    total_win = sum(wins)
    rtp = total_win / total_bet
    hit_freq = hit_count / spins
    mean = total_win / spins
    variance = sum((x - mean)**2 for x in wins) / spins
    std_dev = math.sqrt(variance)
    max_win = max(wins)

    print("=================================")
    print(f"Spins: {spins:,}")
    print(f"Total RTP: {rtp:.4f} ({rtp*100:.2f}%)")
    print(f"Hit Frequency: {hit_freq:.4f} ({hit_freq*100:.2f}%)")
    print(f"Volatility (Std Dev): {std_dev:.4f}")
    print(f"Max Win: {max_win:.2f}x")
    print("=================================")

    return wins

# ==============================
# GRAPH
# ==============================

def plot_win_distribution(wins):
    plt.figure(figsize=(10,6))
    plt.hist(wins, bins=50, color='blue', alpha=0.7, log=True)
    plt.title("Win Distribution Histogram (log scale)")
    plt.xlabel("Win amount")
    plt.ylabel("Frequency (log scale)")
    plt.grid(True, which="both", linestyle='--', linewidth=0.5)
    plt.show()

# ==============================
# MAIN
# ==============================

if __name__ == "__main__":
    wins = simulate(spins=100_000)
    plot_win_distribution(wins)
