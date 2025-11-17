# python/hcmut/iaslab/nlp/app/main.py
import sys

from .generator import run_generation_task
from .parser import run_parser_task


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'generate':
        run_generation_task(limit=10000)
    else:
        run_parser_task()