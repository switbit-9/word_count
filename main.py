import argparse
import asyncio
import os.path
import sys
import time

from files import ProcessFiles
from collections import Counter, OrderedDict

def load_args():
    parser = argparse.ArgumentParser(description="Find most occured words in files")
    parser.add_argument("-max-words", '--N', type=int, help="Number of most common words to display")
    parser.add_argument("file_path", nargs="+", help="Paths to files to analyze")
    args = parser.parse_args()
    max_words = args.N

    files_paths = []
    path = args.file_path
    if len(path) > 1:
        for file_path in path:
            if not os.path.isfile(file_path):
                print(f"Inputed PATH : {file_path} is not a file")
                sys.exit()
            files_paths.append(file_path)

    elif len(path) == 1:
        file = path[0]
        if not os.path.isdir(file):
            if os.path.isfile(file):
                print(f"Error Inputed Path {path} could not be only one file")
            else:
                print("Error Path")
        for root, dirs, files in os.walk(file, topdown=False):
            for name in files:
                files_paths.append(os.path.join(root, name))

    return max_words, files_paths

async def main():
    num_words, file_paths = load_args()

    tasks = []
    for file_path in file_paths:
        o = ProcessFiles(file_path)
        tasks.append(asyncio.create_task(o.process_file()))

    processed_files = await asyncio.gather(*tasks)

    all_counted_words = {}
    for dict_count in processed_files:
        all_counted_words = dict(Counter(all_counted_words) + Counter(dict_count))

    sorted_counted_words = OrderedDict(sorted(all_counted_words.items(), key=lambda item: item[1], reverse=True))

    print("Maximum <N> words:")
    for i, (word, num_times) in enumerate(sorted_counted_words.items()):
        print(f"Word {word} occurred {num_times} times")
        if i + 1 == num_words:
            break

if __name__ == '__main__':
    start_time = time.time()
    asyncio.run(main())
    print(time.time() - start_time)

