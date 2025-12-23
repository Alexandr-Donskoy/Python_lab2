import argparse
from simulation.simulation import run_simulation

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Симуляция библиотеки")
    parser.add_argument("--steps", type=int, default=20, help="Количество шагов симуляции")
    parser.add_argument("--seed", type=int, default=None, help="Seed для генератора случайных чисел")
    args = parser.parse_args()

    run_simulation(steps=args.steps, seed=args.seed)
