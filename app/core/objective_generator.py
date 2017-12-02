import json
import os.path
import tempfile

__author__ = 'Xomak'


class ObjectiveGenerator:

    def __init__(self):
        self.tmp_dir = None
        self.signs_list = None

    def generate(self, signs_list):
        self.tmp_dir = tempfile.mkdtemp()
        self.signs_list = signs_list
        self._create_robot_sequence_file()
        self._create_checker_file()

    def _create_robot_sequence_file(self):
        with open(os.path.join(self.tmp_dir, "sequence.json"), "w") as f:
            sequence = []
            for sign in self.signs_list:
                sequence.append({"tag_id": sign[0], "action": sign[1]})
            json_data = json.dumps(sequence)
            f.write(json_data)

    def _create_checker_file(self):
        # Place for Ruslan
        pass

    def publish(self, ipfs_client):
        add_result = ipfs_client.add(self.tmp_dir)
        dirname = os.path.basename(self.tmp_dir)
        for hash_info in add_result:
            if hash_info['Name'] == dirname:
                return hash_info['Hash']
