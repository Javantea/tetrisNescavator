#!/usr/bin/env pypy3
"""
Nescavate 2
by Javantea
Oct 22-24, 2024

Based on Nescavate
by fractal161

This program is meant to be run with pypy3 but will run in python3.

If you correctly record the level, the pieces (not including the first piece), the row they end up, and whether a clear occurred, you can get the seed. How? By guessing the number of frames that elapse and filtering seeds that produce the sequence. You can see this in action by watching this video that explains what is going on.

"""
import argparse
from states import State, StateChain
try:
    from tqdm import tqdm
except ImportError:
    from contextlib import contextmanager

    @contextmanager
    def tqdm(*args, **kwargs):
        try:
            yield tqdm_nonsense()
        finally:
            pass

    #print("tqdm will give you nice progress bars")
    class tqdm_nonsense:
        def __init__(self, *args, **kwargs):
            pass
        def update(self, val):
            pass

gravityTable = [48, 43, 38, 33, 28, 23, 18, 13, 8, 6, 5, 5, 5, 4, 4, 4, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1]

def pieceToNum(piece):
    return 'tjzosli'.index(piece.lower())


def main():
    parser = argparse.ArgumentParser('nescafe')
    parser.add_argument("-p", "--pieces", action='extend', nargs='+', type=str)
    parser.add_argument("-r", "--rows", action='extend', nargs='+', type=int)
    parser.add_argument("-c", "--clears", action='extend', nargs='+', type=int)
    parser.add_argument("-l", "--level", type=int)
    args = parser.parse_args()

    period = 32767
    seed = 0x8898
    chainList = []
    #level = int(input('Enter starting level (0-19): '))
    level = 6
    if args.level: level = args.level
    print("Level", level)
    gravity = gravityTable[level]
    pieceList = args.pieces or [] #[]
    rowList = args.rows or [] #[]
    clearList = args.clears or [] #[]
    if len(pieceList) < 2:
        print("Usage: nescavate2.py -l 8 -p Z T Z S T J S J T J -r 17 15 13 11 9 7 5 3 1 0 -c 0 0 0 0 0 0 0 0 0 0 0 0")
        return

    pieceList = list(map(pieceToNum, pieceList))
    if len(rowList) < len(pieceList):
        print("Warning: not enough rows")
        rowList += [0]*(len(pieceList) - len(rowList))
    if len(clearList) < len(pieceList):
        print("Warning: not enough clears")
        clearList += [0]*(len(pieceList) - len(clearList))

    #for i in range(len(args.pieces)):
    #    pieceList.append(args.pieces.pop(0))
    #    rowList.append(args.rows.pop(0))
    #    clearList.append(args.clears.pop(0))

    print("Initializing possible seeds...")
    with tqdm(total=period*8*4,leave=True) as pbar:
        for i in range(period):
            for j in range(8):
                for k in range(4):
                    newChain = StateChain(State(seed, j, k, pieceList[1]))
                    newChain.addFrames(rowList[1], clearList[1], gravity)
                    chainList.append(newChain)

            pbar.update(8*4)
            seed = State.prng(seed, 1)

    pieceNum = 2
    while pieceNum < len(pieceList):
        print(f'{len(chainList)} possible third piece seeds.')
        if chainList:
            print(chainList[0].frames)
        if len(chainList) < 65:
            for chain in chainList:
                print(f'{chain.thirdState}, {chain.tailState}')

        newChainList = []

        # Now that we have all the information about the nth piece landing
        # Advance the (n-1)th state by the frame count for the (n-2)th, check if it generates the desired piece.
        with tqdm(total=len(chainList),leave=False) as pbar:
            for chain in chainList:
                newPiece, _ = chain.tailState.getPiece()
                if newPiece == pieceList[pieceNum]:
                    chain.updateTail()
                    chain.addFrames(rowList[pieceNum], clearList[pieceNum], gravity)
                    newChainList.append(chain)
                pbar.update(1)
        chainList = newChainList
        pieceNum += 1
    for chain in chainList:
        print(f'{chain.thirdState}, {chain.tailState}')

if __name__ == "__main__":
    main()
