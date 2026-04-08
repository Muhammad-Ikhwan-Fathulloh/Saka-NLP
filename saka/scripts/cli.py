import argparse
import sys
from saka.core.analyzer import analyze
from saka.core.tokenizer import tokenize
from saka.core.normalizer import normalize

def main():
    parser = argparse.ArgumentParser(description="Saka: Pilar Pemrosesan Bahasa Nusantara")
    parser.add_argument('--stem', type=str, help="Analyze the morphology of a given word")
    parser.add_argument('--tokenize', type=str, help="Tokenize a text into words")
    parser.add_argument('--normalize', type=str, help="Normalize informal/slang words to standard Indonesian")

    args = parser.parse_args()

    if args.stem:
        result = analyze(args.stem)
        print(f"Analysis for '{args.stem}':")
        print(f"  Root: {result.get('root', '')}")
        print(f"  Prefixes: {result.get('prefixes', [])}")
        print(f"  Suffixes: {result.get('suffixes', [])}")
        print(f"  Type: {result.get('type', '')}")
    elif args.tokenize:
        result = tokenize(args.tokenize)
        print(f"Tokens: {result}")
    elif args.normalize:
        result = normalize(args.normalize)
        print(f"Normalized: {result}")
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
