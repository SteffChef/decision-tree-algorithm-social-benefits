from src.dataset import DataSet
from src.cli import CLI

if __name__ == '__main__':

    dataset = DataSet()
    cli = CLI(dataset)
    cli.run()