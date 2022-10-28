from konlpy.tag import Okt


def eWord(sentence):
    print(sentence)
    twt = Okt()
    tagging = twt.pos(sentence)

    v = []
    sy = []
    for i, j in tagging:
        if j == 'Noun' or j == 'Verb' or j == 'Adjective':
            if j == 'Verb':
                v.append(i)
            else:
                sy.append(i)

    if len(v)!=0:
        sy.append(v[-1])

    if '사람' in sy:
        sy.remove('사람')
        return sy
    else:
        return sy

