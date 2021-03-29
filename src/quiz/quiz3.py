# ========================================================================
# Copyright 2020 Emory University
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ========================================================================
import pickle
from collections import Counter
from typing import List, Tuple, Dict, Any

DUMMY = '!@#$'


def read_data(filename: str):
    data, sentence = [], []
    fin = open(filename)

    for line in fin:
        l = line.split()
        if l:
            sentence.append((l[0], l[1]))
        else:
            data.append(sentence)
            sentence = []

    return data


def to_probs(model: Dict[Any, Counter]) -> Dict[str, List[Tuple[str, float]]]:
    probs = dict()
    for feature, counter in model.items():
        ts = counter.most_common()
        total = sum([count for _, count in ts])
        probs[feature] = [(label, count/total) for label, count in ts]
    return probs


def evaluate(data: List[List[Tuple[str, str]]], *args):
    total, correct = 0, 0
    for sentence in data:
        tokens, gold = tuple(zip(*sentence))
        pred = [t[0] for t in predict(tokens, *args)]
        total += len(tokens)
        correct += len([1 for g, p in zip(gold, pred) if g == p])
    accuracy = 100.0 * correct / total
    return accuracy


def create_cw_dict(data: List[List[Tuple[str, str]]]) -> Dict[str, List[Tuple[str, float]]]:
    """
    :param data: a list of tuple lists where each inner list represents a sentence and every tuple is a (word, pos) pair.
    :return: a dictionary where the key is a word and the value is the list of possible POS tags with probabilities in descending order.
    """
    model = dict()
    for sentence in data:
        for word, pos in sentence:
            model.setdefault(word, Counter()).update([pos])
    return to_probs(model)


def create_pp_dict(data: List[List[Tuple[str, str]]]) -> Dict[str, List[Tuple[str, float]]]:
    """
    :param data: a list of tuple lists where each inner list represents a sentence and every tuple is a (word, pos) pair.
    :return: a dictionary where the key is the previous POS tag and the value is the list of possible POS tags with probabilities in descending order.
    """
    model = dict()
    for sentence in data:
        for i, (_, curr_pos) in enumerate(sentence):
            prev_pos = sentence[i-1][1] if i > 0 else DUMMY
            model.setdefault(prev_pos, Counter()).update([curr_pos])
    return to_probs(model)


def create_pw_dict(data: List[List[Tuple[str, str]]]) -> Dict[str, List[Tuple[str, float]]]:
    """
    :param data: a list of tuple lists where each inner list represents a sentence and every tuple is a (word, pos) pair.
    :return: a dictionary where the key is the previous word and the value is the list of possible POS tags with probabilities in descending order.
    """
    model = dict()
    for sentence in data:
        for i, (_, curr_pos) in enumerate(sentence):
            prev_word = sentence[i-1][0] if i > 0 else DUMMY
            model.setdefault(prev_word, Counter()).update([curr_pos])
    return to_probs(model)


def create_nw_dict(data: List[List[Tuple[str, str]]]) -> Dict[str, List[Tuple[str, float]]]:
    """
    :param data: a list of tuple lists where each inner list represents a sentence and every tuple is a (word, pos) pair.
    :return: a dictionary where the key is the previous word and the value is the list of possible POS tags with probabilities in descending order.
    """
    model = dict()
    for sentence in data:
        for i, (_, curr_pos) in enumerate(sentence):
            next_word = sentence[i+1][0] if i+1 < len(sentence) else DUMMY
            model.setdefault(next_word, Counter()).update([curr_pos])
    return to_probs(model)

# P(wi,wi-1,pi)/P(wi,wi-1)
def create_first_pos_dict(data: List[List[Tuple[str, str]]]) -> Dict[Tuple[str, str], List[Tuple[str, float]]]:
    PREV_DUMMY = '!@#$'
    model = dict()

    for sentence in data:
        for i, (word, pos) in enumerate(sentence):
            prev_word = sentence[i - 1][0] if i > 0 else PREV_DUMMY
            model.setdefault((prev_word, word), Counter()).update([pos])

    for wordprevwordtuple, counter in model.items():
        ts = counter.most_common()
        total = sum([count for _, count in ts])
        model[wordprevwordtuple] = [(pos, count / total) for pos, count in ts]

    return model


# P(wi,wi+1,pi)/P(wi,wi+1)
def create_second_pos_dict(data: List[List[Tuple[str, str]]]) -> Dict[Tuple[str, str], List[Tuple[str, float]]]:
    NEXT_DUMMY = '!@#$'
    model = dict()

    for sentence in data:
        for i, (word, pos) in enumerate(sentence):
            next_word = sentence[i + 1][0] if i + 1 < len(sentence) else NEXT_DUMMY
            model.setdefault((word, next_word), Counter()).update([pos])
    # print(model)

    for wordnextwordtuple, counter in model.items():
        ts = counter.most_common()
        total = sum([count for _, count in ts])
        model[wordnextwordtuple] = [(pos, count / total) for pos, count in ts]

    return model


# P(wi,pi-1,pi)/P(wi,pi-1)
def create_third_pos_dict(data: List[List[Tuple[str, str]]]) -> Dict[Tuple[str, str], List[Tuple[str, float]]]:
    PREV_DUMMY = '!@#$'
    model = dict()

    for sentence in data:
        for i, (word, pos) in enumerate(sentence):
            prev_pos = sentence[i - 1][1] if i > 0 else PREV_DUMMY
            model.setdefault((prev_pos, word), Counter()).update([pos])
    # print(model)

    for wordprevwordtuple, counter in model.items():
        ts = counter.most_common()
        total = sum([count for _, count in ts])
        model[wordprevwordtuple] = [(pos, count / total) for pos, count in ts]

    return model


# P(pi-1,pi-2,pi)/P(pi-1,pi-2)
def create_fourth_pos_dict(data: List[List[Tuple[str, str]]]) -> Dict[Tuple[str, str], List[Tuple[str, float]]]:
    PREV_DUMMY = '!@#$'
    model = dict()

    for sentence in data:
        for i, (word, pos) in enumerate(sentence):
            prev_pos = sentence[i - 1][1] if i > 0 else PREV_DUMMY
            prep_pos = sentence[i - 2][1] if i > 1 else PREV_DUMMY
            model.setdefault((prep_pos, prev_pos), Counter()).update([pos])
    # print(model)

    for wordprevwordtuple, counter in model.items():
        ts = counter.most_common()
        total = sum([count for _, count in ts])
        model[wordprevwordtuple] = [(pos, count / total) for pos, count in ts]

    return model

def train(trn_data: List[List[Tuple[str, str]]], dev_data: List[List[Tuple[str, str]]]) -> Tuple:
    """
    :param trn_data: the training set
    :param dev_data: the development set
    :return: a tuple of all parameters necessary to perform part-of-speech tagging
    """
    cw_dict = create_cw_dict(trn_data)
    pp_dict = create_pp_dict(trn_data)
    pw_dict = create_pw_dict(trn_data)
    nw_dict = create_nw_dict(trn_data)
    first_dict = create_first_pos_dict(trn_data)
    second_dict = create_second_pos_dict(trn_data)
    third_dict = create_third_pos_dict(trn_data)
    fourth_dict = create_fourth_pos_dict(trn_data)
    best_acc, best_args = -1, None
    grid = [1.0, 1.5]

    for first_weight in grid:
        for second_weight in grid:
            for third_weight in grid:
                for fourth_weight in grid:
                    args = (cw_dict, pp_dict, pw_dict, nw_dict, first_dict, second_dict, third_dict, fourth_dict, first_weight, second_weight, third_weight, fourth_weight)
                    acc = evaluate(dev_data, *args)
                    print('{:5.2f}% - cw: {:3.1f}, pp: {:3.1f}, pw: {:3.1f}, nw: {:3.1f}'.format(acc, first_weight, second_weight, third_weight, fourth_weight))
                    if acc > best_acc: best_acc, best_args = acc, args

    return best_args


def predict(tokens: List[str], *args) -> List[Tuple[str, float]]:
    cw_dict, pp_dict, pw_dict, nw_dict, first_dict, second_dict, third_dict, fourth_dict, first_weight, second_weight, third_weight, fourth_weight = args
    output = []

    for i in range(len(tokens)):
        scores = dict()
        curr_word = tokens[i]
        prev_pos = output[i-1][0] if i > 0 else DUMMY
        prep_pos = output[i - 2][0] if i > 1 else DUMMY
        prev_word = tokens[i-1] if i > 0 else DUMMY
        next_word = tokens[i+1] if i+1 < len(tokens) else DUMMY

        for pos, prob in cw_dict.get(curr_word, list()):
            scores[pos] = scores.get(pos, 0) + prob * 1.0

        for pos, prob in pp_dict.get(prev_pos, list()):
            scores[pos] = scores.get(pos, 0) + prob * 0.5

        for pos, prob in pw_dict.get(prev_word, list()):
            scores[pos] = scores.get(pos, 0) + prob * 0.5

        for pos, prob in nw_dict.get(next_word, list()):
            scores[pos] = scores.get(pos, 0) + prob * 0.5

        for pos, prob in first_dict.get((prev_word, curr_word), list()):
            scores[pos] = scores.get(pos, 0) + prob * first_weight

        for pos, prob in second_dict.get((curr_word, next_word), list()):
            scores[pos] = scores.get(pos, 0) + prob * second_weight

        for pos, prob in third_dict.get((prev_pos, curr_word), list()):
            scores[pos] = scores.get(pos, 0) + prob * third_weight

        for pos, prob in fourth_dict.get((prep_pos, prev_pos), list()):
            scores[pos] = scores.get(pos, 0) + prob * fourth_weight

        o = max(scores.items(), key=lambda t: t[1]) if scores else ('XX', 0.0)
        output.append(o)

    return output


if __name__ == '__main__':
    path = '../../'  # path to the cs329 directory
    trn_data = read_data(path + 'dat/pos/wsj-pos.trn.gold.tsv')
    dev_data = read_data(path + 'dat/pos/wsj-pos.dev.gold.tsv')
    model_path = path + 'src/quiz/quiz3.pkl'

    # save model
    args = train(trn_data, dev_data)
    pickle.dump(args, open(model_path, 'wb'))
    # load model
    args = pickle.load(open(model_path, 'rb'))
    print(evaluate(dev_data, *args))