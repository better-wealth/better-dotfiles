import sys

from better_dotfiles.better_dotfiles import fib


if __name__ == "__main__":
    n = int(sys.argv[1])
    print(fib(n))
