from src.Algorithm import Algorithm
from src.CLI import CLI

if __name__ == '__main__':
    algorithm = Algorithm()
    cli = CLI(algorithm)
    cli.run()