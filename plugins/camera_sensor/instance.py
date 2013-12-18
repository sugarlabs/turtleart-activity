import os

from sugar import profile
from sugar import util

class Instance:
    key = profile.get_pubkey()
    keyHash = util.sha_data(key)

    keyHashPrintable = util.printable_hash(keyHash)

    instancePath = None

    def __init__(self, ca):
        self.__class__.instancePath = os.path.join(ca.get_activity_root(), "instance")
        recreateTmp()


def recreateTmp():
    if (not os.path.exists(Instance.instancePath)):
        os.makedirs(Instance.instancePath)

