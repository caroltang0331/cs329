# ========================================================================
# Copyright 2021 Emory University
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
import re


def normalize(text):
    dictionary = {
        'one': '1',
        'two': '2',
        'three': '3',
        'four': '4',
        'five': '5',
        'six': '6',
        'seven': '7',
        'eight': '8',
        'nine': '9',
        'ten': '10',
        'eleven': '11',
        'twelve': '12',
        'thir': '3',
        'for': '4',
        'fif': '5',
        'twen': '2'
    }
    for key in dictionary:
        RE = re.compile(key)
        hundres = RE.search((text))
        while (hundres is not None):
            ms = RE.search(text)
            endTy = text[ms.end() + 2:]
            endY = text[ms.end() + 1:]
            endTeen = text[ms.end() + 4:]
            endEen = text[ms.end() + 3:]
            text = text[: ms.start()] + dictionary[key] + text[ms.end():]
            if text[ms.start() + len(dictionary[key]):ms.start() + len(dictionary[key]) + 2] == 'ty':
                middleNum = 10 * int(dictionary[key])
                text = text[: ms.start()] + str(middleNum) + endTy
            elif text[ms.start() + len(dictionary[key]):ms.start() + len(dictionary[key]) + 1] == 'y':
                middleNum = 10 * int(dictionary[key])
                text = text[: ms.start()] + str(middleNum) + endY
            elif text[ms.start() + len(dictionary[key]):ms.start() + len(dictionary[key]) + 4] == 'teen':
                text = text[: ms.start()] + str(10 + int(dictionary[key])) + endTeen
            elif text[ms.start() + len(dictionary[key]):ms.start() + len(dictionary[key]) + 3] == 'een':
                text = text[: ms.start()] + str(10 + int(dictionary[key])) + endEen
            hundres = RE.search(text)
    print(text)
    RE = re.compile(r'\d\d+[\s-]\d')
    spaceOrDash = RE.search(text)
    print(spaceOrDash)
    # if spaceOrDash is not None:
    #    plus = int(text[ms.start() + 3: ms.start() + 4])
    #    middleNum = middleNum + plus
    #    text = text[:ms.start()] + str(middleNum) + text[ms.start() + 4]
    #    print(text)

    RE = re.compile(r'(hundred)')
    hundres = RE.search(text)
    while hundres is not None:
        ms = RE.search(text)
        text = text[: ms.start()] + '100' + text[ms.end():]
        if text[ms.start() - 2: ms.start()] == ('a ' or 'A '):
            text = text[: ms.start() - 2] + text[ms.start():]
        #RE = re.compile(r'\d\d[\s-]\d')
        #numSpace = RE.search(text)
        print(text)
        #print(numSpace)
        #print(text[ms.start() - 5:ms.start()])
        hundres = RE.search(text)

    RE = re.compile(r'(thousand)')
    hundres = RE.search(text)
    while hundres is not None:
        ms = RE.search(text)
        text = text[: ms.start()] + '1000' + text[ms.end():]
        if text[ms.start() - 2: ms.start()] == ('a ' or 'A '):
            text = text[: ms.start() - 2] + text[ms.start():]
        hundres = RE.search(text)

    RE = re.compile(r'(million)')
    hundres = RE.search(text)
    while hundres is not None:
        ms = RE.search(text)
        text = text[: ms.start()] + '1000000' + text[ms.end():]
        if text[ms.start() - 2: ms.start()] == ('a ' or 'A '):
            text = text[: ms.start() - 2] + text[ms.start():]
        hundres = RE.search(text)

    RE = re.compile(r'(billion)')
    hundres = RE.search(text)
    while hundres is not None:
        ms = RE.search(text)
        text = text[: ms.start()] + '1000000000' + text[ms.end():]
        if text[ms.start() - 2: ms.start()] == ('a ' or 'A '):
            text = text[: ms.start() - 2] + text[ms.start():]
        hundres = RE.search(text)

    RE = re.compile(r'(trillion)')
    hundres = RE.search(text)
    while hundres is not None:
        ms = RE.search(text)
        text = text[: ms.start()] + '1000000000000' + text[ms.end():]
        if text[ms.start() - 2: ms.start()] == ('a ' or 'A '):
            text = text[: ms.start() - 2] + text[ms.start():]
        hundres = RE.search(text)

    #print(text)
    return text





def normalize_extra(text):
    # TODO: to be updated
    return text


if __name__ == '__main__':
    S = [
        'I met twelve people eighty-three',
        'I have one brother and two sisters thirty two',
        'A year has one billion five million thirteen thousand eighteen hundred sixty-five days, and two hundred',
        'I made a million dollars'
    ]

    T = [

        'I met 12 people',
        'I have 1 brother and 2 sisters',
        'A year has 365 days',
        'I made 1000000 dollars'
    ]

    correct = 0
    for s, t in zip(S, T):
        if normalize(s) == t:
            correct += 1

    print('Score: {}/{}'.format(correct, len(S)))
