import logging, sys, argparse


def str2bool(v):
    # copy from StackOverflow
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def get_entity(tag_seq, char_seq):
    PER = get_PER_entity(tag_seq, char_seq)
    LOC = get_LOC_entity(tag_seq, char_seq)
    EVE = get_EVE_entity(tag_seq, char_seq)
    FAC = get_FAC_entity(tag_seq, char_seq)
    return PER, LOC, EVE, FAC


def get_PER_entity(tag_seq, char_seq):
    length = len(char_seq)
    PER = []
    wordstart = False
    for i, (char, tag) in enumerate(zip(char_seq, tag_seq)):
        if tag == 'B-PER':
            wordstart = True
            if 'per' in locals().keys():
                PER.append(per)
                del per
            per = char
            if i+1 == length:
                PER.append(per)
        if tag == 'I-PER' and wordstart:
            per += char
            if i+1 == length:
                PER.append(per)
        if tag not in ['I-PER', 'B-PER']:
            wordstart = False
            if 'per' in locals().keys():
                PER.append(per)
                del per
            continue
    return PER


def get_LOC_entity(tag_seq, char_seq):
    length = len(char_seq)
    LOC = []
    wordstart = False
    for i, (char, tag) in enumerate(zip(char_seq, tag_seq)):
        if tag == 'B-LOC':
            wordstart = True
            if 'loc' in locals().keys():
                LOC.append(loc)
                del loc
            loc = char
            if i+1 == length:
                LOC.append(loc)

        if tag == 'I-LOC' and wordstart:
            loc += char
            if i+1 == length:
                LOC.append(loc)

        if tag not in ['I-LOC', 'B-LOC']:
            wordstart = False
            if 'loc' in locals().keys():
                LOC.append(loc)
                del loc
            continue

    return LOC


def get_EVE_entity(tag_seq, char_seq):
    length = len(char_seq)
    EVE = []
    wordstart = False
    for i, (char, tag) in enumerate(zip(char_seq, tag_seq)):
        if tag == 'B-EVE':
            wordstart = True
            if 'eve' in locals().keys():
                EVE.append(eve)
                del eve
            eve = char
            if i+1 == length:
                EVE.append(eve)
        if tag == 'I-EVE' and wordstart:
            eve += char
            if i+1 == length:
                EVE.append(eve)
        if tag not in ['I-EVE', 'B-EVE']:
            wordstart = False
            if 'eve' in locals().keys():
                EVE.append(eve)
                del eve
            continue

    return EVE

def get_FAC_entity(tag_seq, char_seq):
    length = len(char_seq)
    FAC = []
    wordstart = False
    for i, (char, tag) in enumerate(zip(char_seq, tag_seq)):
        if tag == 'B-FAC':
            wordstart = True
            if 'fac' in locals().keys():
                FAC.append(fac)
                del fac
            fac = char
            if i+1 == length:
                FAC.append(fac)
        if tag == 'I-FAC' and wordstart:
            fac += char
            if i+1 == length:
                FAC.append(fac)
        if tag not in ['I-FAC', 'B-FAC']:
            wordstart = False
            if 'fac' in locals().keys():
                FAC.append(fac)
                del fac
            continue
    return FAC

def get_logger(filename):
    logger = logging.getLogger('logger')
    logger.setLevel(logging.DEBUG)
    logging.basicConfig(format='%(message)s', level=logging.DEBUG)
    handler = logging.FileHandler(filename)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s: %(message)s'))
    logging.getLogger().addHandler(handler)
    return logger
