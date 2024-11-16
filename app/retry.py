import time
from functools import wraps

def print_retry_failure(retry_state):
    print(f"Failed after {retry_state.attempt_number} attempts")

def print_retry_attempt(retry_state):
    print(f"Attempt {retry_state.attempt_number} failed: {retry_state}")