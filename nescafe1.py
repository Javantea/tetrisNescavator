import argparse
from states import State, StateChain
from tqdm import tqdm

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

    N = 32767
    seed = 0x8898
    chainList = []
    #level = int(input('Enter starting level (0-19): '))
    level = 6
    if args.level: level = args.level
    gravity = gravityTable[level]
    pieceList = args.pieces or [] #[]
    rowList = args.rows or [] #[]
    clearList = args.clears or [] #[]
    if len(pieceList) < 2:
        print("Usage: nescafe1.py -p L J T Z -r 1 2 3 4 -c 0 0 0 0")
        return

    pieceList = list(map(pieceToNum, pieceList))

    #for i in range(len(args.pieces)):
    #    pieceList.append(args.pieces.pop(0))
    #    rowList.append(args.rows.pop(0))
    #    clearList.append(args.clears.pop(0))

    print("Initializing possible seeds...")
    with tqdm(total=N*8*4,leave=True) as pbar:
        for i in range(N):
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
