# ========================================================================
# Copyright 2020 Emory University
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ========================================================================

import nltk

from typing import Set, Optional, List
from nltk.corpus.reader import Synset
from nltk.corpus import wordnet as wn


def antonyms(sense: str) -> Set[Synset]:
    """
    :param sense: the ID of the sense (e.g., 'dog.n.01').
    :return: a set of Synsets representing the union of all antonyms of the sense as well as its synonyms.
    """
    result = set()
    sen = wn.synset(sense)

    for syn in sen.lemmas():
        if syn.antonyms():
            for allan in syn.antonyms():
                result.add(allan.synset())
    return result


def paths(sense_0: str, sense_1: str) -> List[List[Synset]]:

    result0 = []
    first = wn.synset(sense_0)
    second = wn.synset(sense_1)
    hypernym_path0 = first.hypernym_paths()
    hypernym_path1 = second.hypernym_paths()
    lch = first.lowest_common_hypernyms(second)

    for hypernym in lch:
        for syn_list in hypernym_path1:
            i = next((i for i, syn in enumerate(syn_list) if syn == hypernym), -1)
            if i >= 0:
                path = syn_list[i:]
                for syn_list in hypernym_path0:
                    pathOwn = path.copy()
                    i = next((i for i, syn in enumerate(syn_list) if syn == hypernym), -1)
                    if i >= 0:
                        for e in syn_list[i+1:]:
                            pathOwn.insert(0, e)
                        result0.append(pathOwn)

    myset = set()
    for result in result0:
        myset.add(str(result))

    return list(myset)


if __name__ == '__main__':
    print(antonyms('purchase.v.01'))
    print(antonyms('end.v.02'))
    print(antonyms('nonspecific.a.01'))

    for path in paths('dog.n.01', 'cat.n.01'):
       print([s.name() for s in path])
    print('\n')
    for path in paths('body.n.09', 'sidereal_day.n.01'):
        print([s.name() for s in path])
    print('\n')
    for path in paths('boy.n.01', 'girl.n.01'):
        print([s.name() for s in path])