from src.balance import get_balance
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

balance = get_balance(1)

print("Current balance:", balance)