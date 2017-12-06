from unittest import TestCase
import os
import validator.core.utils as utils
import tempfile


class TestUtils(TestCase):

    def test_split_name_ext_from_filename(self):
        path = "test_service.log"

        name, ext = utils.split_name_ext(path)

        self.assertTrue(name == "test_service")
        self.assertTrue(ext[1:] == "log")

    def test_split_name_ext_from_path(self):
        path = "core/tests/test_service.log"

        name, ext = utils.split_name_ext(path)

        self.assertTrue(name == "core/tests/test_service")
        self.assertTrue(ext[1:] == "log")

    def test_split_name_ext_from_empty_ext(self):
        path = "test_service"

        name, ext = utils.split_name_ext(path)

        self.assertTrue(name == "test_service")
        self.assertTrue(ext == "")

    def test_split_name_ext_from_empty_ext_path(self):
        path = "core/tests/test_service"

        name, ext = utils.split_name_ext(path)

        self.assertTrue(name == "core/tests/test_service")
        self.assertTrue(ext == "")

    def test_split_name_ext_from_tmpfilename(self):
        model_descriptor, model_path = tempfile.mkstemp(dir=".")

        name, ext = utils.split_name_ext(model_path)

        self.assertTrue(len(name) > 0)
        self.assertTrue(ext == "")

        os.close(model_descriptor)
        os.remove(model_path)
