# Project 6 Report: Myanmar Checkers AI Visualizer

> [!IMPORTANT]
> **AUTOGRADER COMPLIANCE INSTRUCTIONS:**
> This report is parsed automatically by the autograder. To ensure you receive full credit for your work:
> 1. **Do not modify** the section headers (`## ...`) or bold field keys (e.g., `**Name:**`, `**Primary AI Algorithm:**`, `**Live Deployment URL:**`, etc.).
> 2. **Write your answers directly after** the colon `:` of each field, replacing the placeholder text completely (including the outer brackets `[` and `]`).
> 3. **Maintain the file structure**. Changing headers, bold titles, or deleting lines can cause the autograder to miss your responses and award 0 marks.

---

## Student Information
- **Name:** Phyo Thandar Hlaing
- **MMDT ID:** MMDT123

---

## Section 1: AI Agent Configuration
- **Primary AI Algorithm:** Minimax with Alpha-Beta Pruning
- **Pruning Technique:** Alpha-Beta Pruning
- **Evaluation Heuristic Strategy:** Piece Advantage, King Advantage, Center Control, and Mobility

---

## Section 2: Complexity & Evaluation Function Analysis
- **Board Configuration:** An 8×8 checkerboard with 64 squares. Each player starts with 12 pieces placed on the dark squares of the first three rows on their side. The human player uses White/X pieces and the AI uses Black/O pieces.
- **Piece Valuation & Rules:** Normal pieces are valued at 1 point, while kings are valued at 4 points because they have greater mobility and can move over longer diagonal distances. The game uses mandatory capture rules, including backward captures for men, multi-jump captures, and the maximum-capture rule. A piece is promoted to a king when it reaches the opponent’s back row.
- **Heuristic Features Used:** Piece count, king count, center control, and mobility. Normal pieces contribute to material advantage, kings receive a higher value, pieces controlling central squares receive a small positional bonus, and the number of available legal moves is used to measure mobility.

---

## Section 3: Local Verification & Feature Checklist
*Check the algorithms, agents, and features you successfully ran and verified on your local development server by placing an `x` in the brackets (e.g., `[x]`):*
- [x] Myanmar Checkers Game Engine & Board State Representation
- [x] Legal Move Generation and Capture Mechanics
- [x] Minimax Search Algorithm with Alpha-Beta Pruning
- [x] Rule-Based / Heuristic AI Agent
- [x] Uniform Random Baseline Agent
- [x] Interactive Web Visualizer with Playable Board & Game Feedback

---

## Section 4: Deployed and Presentation Information
- **Deployment Platform:** Render
- **Live Deployment URL:** [Provide your live deployment site URL here]
- **Video Presentation Link:** [Provide an accessible link to your 5–7 minute video presentation]

---

## Section 5: Discussion
*Provide your written analysis for each point by replacing the bracket placeholders below:*
- **Explain how Alpha-Beta pruning optimizes decision-making in large-branching board games like Checkers without sacrificing tactical depth.**
    Alpha-Beta pruning makes Minimax faster by avoiding branches that cannot change the final decision. In Checkers, many legal moves can create a large search tree, so exploring every possible continuation is expensive. Alpha-Beta keeps track of the best score already found for both players and stops searching a branch when it is clear that the branch cannot produce a better result. This reduces the number of positions the AI must evaluate, allowing it to search deeper within the same amount of time. The important point is that it does not change the final Minimal decision, it only removes unnecessary calculations.
- **Compare classical Adversarial Search & Heuristic Evaluation in Checkers with modern Generative AI / Deep Reinforcement Learning game agents (e.g., AlphaZero, MCTS, Value Networks, Process Reward Models).**
    Classical Checkers AI uses Minimax, Alpha-Beta pruning, and hand-made heuristics like piece count, kings, mobility, and center control. it is easy to understand, but its strength depends on search depth and the quality of the heuristic. Modern AI systems such as AlphaZero combine search with neural networks, so they can learn which moves and board positions are important from experience. In short, classical AI follows designed rules, while modern AI learns how to guide its search.
