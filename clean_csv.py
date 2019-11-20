#!/usr/bin/env python
import pandas as pd
from argparse import ArgumentParser

def main(args):
    df = pd.read_csv(args.input, header=0)
    df.rename(columns=lambda x: x.split("[")[-1].rstrip("]"), inplace=True)
    df.rename(columns={'R Markdown': 'RMarkdown'}, inplace=True)
    df.to_csv(args.output, index=False)

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("input", type=str,
                        help="Input csv file")
    parser.add_argument("output", type=str,
                        help="Output csv file cleaned")
    args = parser.parse_args()
    main(args)
