__author__ = 'Xomak'


class ObjectiveExtractor:

    ROBOT_SEQUENCE_FILE = 'sequence.json'

    def __init__(self, ipfs_client):
        self.ipfs_client = ipfs_client

    def get_hash_from_multihash(self, multihash, filename):
        hashes = self.ipfs_client.ls(multihash)
        for hash_info in hashes['Objects'][0]['Links']:
            if hash_info['Name'] == filename:
                return hash_info['Hash']

    def get_robot_sequence(self, dirhash):
        objective_hash = self.get_hash_from_multihash(dirhash, self.ROBOT_SEQUENCE_FILE)
        return self.ipfs_client.cat(objective_hash)
