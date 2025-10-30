## Monte Carlo Search for "Teen Do Paanch"

This project explores the performance of various Monte Carlo search algorithms in the context of the Indian trick-taking card game **Teen Do Paanch (TDP)**.
A complete simulation environment for a simplified 3-player version of TDP was built. The project then evaluated several decision-making algorithms under three distinct experimental setups:

1.  **Perfect Information:** All hands are known.
2.  **Imperfect Information:** Opponent hands are hidden.
3.  **Self-Play:** Algorithms compete against each other.

---

### 1. Perfect Information (All Cards Known)

In this baseline scenario, agents play knowing all cards in their opponents' hands.

* **Algorithms Tested:** Flat Monte Carlo, UCB, UCT (minimax and $max^{n}$ variants), and Sequential Halving.
* **Opponents:** Agents were tested against "Random" players and "Rule-Based" players (who always play their highest legal card).

#### Key Findings (Perfect Info):
* ]**Best Performance:** Against rule-based opponents, **UCT (max"")** achieved the highest win rate at **62.6%**.
* **Strongest vs. Random:** Flat Monte Carlo (59.2%) and **Sequential Halving (59.4%)** were the most effective against random opponents.
* **Efficiency:** **Sequential Halving** was the fastest algorithm, while Flat Monte Carlo was approximately 4x slower than tree-based methods.

---

### 2. Imperfect Information (Hidden Cards)

This setup models a realistic game where opponent hands are hidden. The project used a sampled determinization approach, where the agent generates multiple "possible worlds" (plausible opponent hands) and evaluates them.

* **Sampling Methods:**
    1.  **Basic Sampling:** Hidden cards are randomly redistributed.
    2.  **Inference-Based Sampling:** Creates more realistic worlds by using trick history (e.g., inferring a player is out of a suit if they fail to follow).

#### Key Findings (Imperfect Info):
* **Inference is Key:** Inference-based sampling consistently improved performance over basic sampling for all algorithms. For example, UCT's win rate jumped from 48% to 55% against rule-based players.
* **Top Performer:** **Sequential Halving** (with inference) proved highly robust, achieving a **57% win rate** against rule-based opponents.
* **Efficiency:** Sequential Halving remained the most time-efficient method.

---

### 3. Self-Play Tournament

In the final experiment, the top algorithms (UCB, UCT, and Sequential Halving) were made to play against each other.

#### Key Findings (Self-Play):
* **Clear Winner:** **Sequential Halving** consistently demonstrated the strongest performance.
* **Superior Adaptation:** In the most realistic setup (imperfect information with inference), Sequential Halving clearly outperformed the others with a 43% win rate**, while the performance of UCB (32%) and UCT (25%) dropped significantly].

### Overall Conclusion

Across all experiments, **Sequential Halving** emerged as the most practical and high-performing algorithm for this game. It was consistently the fastest and, when combined with inference-based sampling, it clearly outperformed UCB and UCT in the realistic self-play environment.
