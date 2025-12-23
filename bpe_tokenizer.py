from collections import Counter
import regex as re

PAT = r"""'(?:[sdmt]|ll|ve|re)| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+"""


def split_bytes(byte_string: bytes) -> tuple[bytes]:
    """
    Split a byte string into a tuple of single byte bytes objects.
    """
    return tuple((bytes([byte]) for byte in byte_string))

def count_pairs(sequence: tuple[bytes], count_of_sequence: int, counter_to_update: Counter) -> dict[tuple[bytes], int]:
    for i in range(len(sequence) - 1):
        pair = (sequence[i], sequence[i + 1])
        counter_to_update[pair] += count_of_sequence
    return counter_to_update

def byte_pair_encoding(corpus: str, vocab: dict[tuple[bytes], int], num_of_merges: int) -> tuple[dict[int, str], list[tuple[str, str]]]:
    """
    Implement the Byte Pair Encoding (BPE) algorithm to tokenize a corpus.
    """
    # Pre-tokenize the corpus
    tokens: dict(tuple[bytes], int) = {}
    for match in re.finditer(PAT, corpus):
        split_bytes_group = split_bytes(bytes(match.group(), "utf-8"))
        # add the token to the tokens dictionary if doesnt exist
        if split_bytes_group not in tokens:
            tokens[split_bytes_group] = 1
        else:   
            tokens[split_bytes_group] += 1
    print(tokens)
    for _ in range(num_of_merges):
        counter = Counter()
        # print first key
        for key in tokens.keys():
            count_pairs(key, tokens[key], counter)
        # Most frequent pair, with lexicographic tie-breaking
        best_pair = max(counter.keys(), key=lambda pair: (counter[pair], pair))
        curr_vocab_size = len(vocab)
        vocab[best_pair[0] + best_pair[1]] = curr_vocab_size
        for key in list(tokens.keys()):
            new_key = key
            i = 0
            while i < len(new_key) - 1:
                if new_key[i:i+2] == best_pair:
                    # print("Initial part of new key: ", new_key[:i])
                    # print("Best pair: ", best_pair)
                    # print("Final part of new key: ", new_key[i+2:])
                    new_key = new_key[:i] + (best_pair[0] + best_pair[1],) + new_key[i+2:]
                else:
                    i += 1
            if new_key not in tokens:
                tokens[new_key] = tokens[key]
                del tokens[key]
        print(tokens)
    print(vocab)

    

vocab = {}
for i in range(256):
    vocab[bytes([i])] = i
byte_pair_encoding("low low low low low lower lower widest widestest widest newest newest newest newest newest newest", vocab, 2)