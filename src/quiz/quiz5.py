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
import glob
import os
from types import SimpleNamespace
from typing import Iterable, Tuple, Any, List, Set

import ahocorasick


def create_ac(data: Iterable[Tuple[str, Any]]) -> ahocorasick.Automaton:
    """
    Creates the Aho-Corasick automation and adds all (span, value) pairs in the data and finalizes this matcher.
    :param data: a collection of (span, value) pairs.
    """
    AC = ahocorasick.Automaton(ahocorasick.STORE_ANY)

    for span, value in data:
        if span in AC:
            t = AC.get(span)
        else:
            t = SimpleNamespace(span=span, values=set())
            AC.add_word(span, t)
        t.values.add(value)

    AC.make_automaton()
    return AC


def read_gazetteers(dirname: str) -> ahocorasick.Automaton:
    data = []
    for filename in glob.glob(os.path.join(dirname, '*.txt')):
        label = os.path.basename(filename)[:-4]
        for line in open(filename):
            data.append((line.strip(), label))
    return create_ac(data)


def match(AC: ahocorasick.Automaton, tokens: List[str]) -> List[Tuple[str, int, int, Set[str]]]:
    """
    :param AC: the finalized Aho-Corasick automation.
    :param tokens: the list of input tokens.
    :return: a list of tuples where each tuple consists of
             - span: str,
             - start token index (inclusive): int
             - end token index (exclusive): int
             - a set of values for the span: Set[str]
    """
    smap, emap, idx = dict(), dict(), 0
    for i, token in enumerate(tokens):
        smap[idx] = i
        idx += len(token)
        emap[idx] = i
        idx += 1

    # find matches
    text = ' '.join(tokens)
    spans = []
    for eidx, t in AC.iter(text):
        eidx += 1
        sidx = eidx - len(t.span)
        sidx = smap.get(sidx, None)
        eidx = emap.get(eidx, None)
        if sidx is None or eidx is None: continue
        spans.append((t.span, sidx, eidx + 1, t.values))

    return spans


def remove_overlaps(entities: List[Tuple[str, int, int, Set[str]]]) -> List[Tuple[str, int, int, Set[str]]]:
    """
    :param entities: a list of tuples where each tuple consists of
             - span: str,
             - start token index (inclusive): int
             - end token index (exclusive): int
             - a set of values for the span: Set[str]
    :return: a list of entities where each entity is represented by a tuple of (span, start index, end index, value set)
    """
    # TODO: to be updated
    tmp = []
    pointer = 0
    nextItem = None
    nextnextItem = None
    while pointer < len(entities):
        currItem = entities[pointer]
        if pointer + 1 < len(entities):
            nextItem = entities[pointer + 1]
        else:
            nextItem = None
        if pointer + 2 < len(entities):
            nextnextItem = entities[pointer + 2]
        else:
            nextnextItem = None

        if nextnextItem is not None and nextItem is not None:
            if currItem[2] > nextItem[1]:
                if nextItem[2] > nextnextItem[1]:
                    tmp.append(currItem)
                    tmp.append(nextnextItem)
                    pointer = pointer + 2
                else:
                    mymax = max([currItem, nextItem], key=lambda x: len(x[0].split()))
                    mymin = min([currItem, nextItem], key=lambda x: len(x[0].split()))
                    tmp.append(mymax)
                    if mymin in tmp:
                        tmp.remove(min([currItem, nextItem], key=lambda x: len(x[0].split())))
                    pointer = pointer + 2
            else:
                tmp.append(currItem)
                pointer = pointer + 1
        elif nextnextItem is None and nextItem is not None:
            if currItem[2] > nextItem[1]:
                mymax = max([currItem, nextItem], key=lambda x: len(x[0].split()))
                mymin = min([currItem, nextItem], key=lambda x: len(x[0].split()))
                tmp.append(mymax)
                if mymin in tmp:
                    tmp.remove(min([currItem, nextItem], key=lambda x: len(x[0].split())))
                pointer = pointer + 2
            else:
                tmp.append(currItem)
                tmp.append(nextItem)
                pointer = pointer + 2
        else:
            tmp.append(currItem)
            pointer = pointer + 1

    result = list()
    for item in tmp:
        if item not in result:
            result.append(item)
    return result


def to_bilou(tokens: List[str], entities: List[Tuple[str, int, int, str]]) -> List[str]:
    """
    :param tokens: a list of tokens.
    :param entities: a list of tuples where each tuple consists of
             - span: str,
             - start token index (inclusive): int
             - end token index (exclusive): int
             - a named entity tag
    :return: a list of named entity tags in the BILOU notation with respect to the tokens
    """
    # TODO: to be updated
    return tokens


if __name__ == '__main__':
    gaz_dir = 'dat/ner'
    AC = read_gazetteers('../../dat/ner')

    tokens = 'Atlantic City of Georgia'.split()
    #tokens = 'wjodifh AAA BB CCC DD EEE FF FHDSKHFW'.split()
    #tokens = 'Jinho is a professor at Emory University in the South Korean South Korea United Stateswwww of a America'.split()
    entities = match(AC, tokens)
    print(entities)
    entities = remove_overlaps(entities)
    print(entities)
