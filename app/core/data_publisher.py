import json
import os.path
import tempfile
from validator.core.specification import TagsSpecification
from validator.core.compile import TaxiCompiler
from validator.core.generator import TagsGenerator

__author__ = 'Xomak'


class IPFSConnector:

    ROBOT_SEQUENCE_FILE = 'sequence.json'
    ROBOT_RESULT_FILE = 'log.txt'
    ROBOT_MODEL_FILE = "model.prism"

    def __init__(self, ipfs_client):
        self.ipfs_client = ipfs_client

    def create_objective(self, signs_list, template_path):
        tmp_dir = tempfile.mkdtemp()
        self._create_robot_sequence_file(tmp_dir, signs_list)
        self._create_checker_file(tmp_dir, signs_list, template_path)
        return self._publish(tmp_dir)

    def create_result(self, signs_list):
        tmp_dir = tempfile.mkdtemp()
        self._create_result_log(tmp_dir, signs_list)
        self._publish(tmp_dir)

    def _create_result_log(self, directory, signs_list):
        with open(os.path.join(directory, self.ROBOT_RESULT_FILE), "w") as f:
            for sign in signs_list:
                f.write(sign + '\n')

    def _create_robot_sequence_file(self, directory, signs_list):
        with open(os.path.join(directory, self.ROBOT_SEQUENCE_FILE), "w") as f:
            sequence = []
            for sign in signs_list:
                sequence.append({"tag_id": sign[0], "action": sign[1]})
            json_data = json.dumps(sequence)
            f.write(json_data)

    def _create_checker_file(self, directory, signs_list, template_path):
        tags = list(map(lambda sign: sign[0], signs_list))
        spec = TagsSpecification(tags)
        generator = TagsGenerator(spec)

        compiler = TaxiCompiler(generator, template_path)
        model = compiler.compile()

        model_path = os.path.join(directory, self.ROBOT_MODEL_FILE)
        with open(model_path, "w") as file:
            file.writelines(str(model))

    def _publish(self, directory):
        add_result = self.ipfs_client.add(directory)
        dirname = os.path.basename(directory)
        for hash_info in add_result:
            if hash_info['Name'] == dirname:
                return hash_info['Hash']

    def get_robot_sequence(self, dirhash):
        objective_hash = self._get_hash_from_multihash(dirhash, self.ROBOT_SEQUENCE_FILE)
        return self.ipfs_client.cat(objective_hash)

    def _get_hash_from_multihash(self, multihash, filename):
        hashes = self.ipfs_client.ls(multihash)
        for hash_info in hashes['Objects'][0]['Links']:
            if hash_info['Name'] == filename:
                return hash_info['Hash']
