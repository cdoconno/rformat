import pytest
import sys

from rformat.utils import config


class TestConfig(object):
    def test_parse_yaml_raises_type_error_if_provided_nonstring_for_path(self):
        with pytest.raises(TypeError):
            # send am IntType object instead of string, 99 is just an integer
            config.parse_yaml(type(99))

    def test_parse_yaml_raises_does_not_raise_type_error_if_provided_string_for_path(self):
        try:
            config.parse_yaml("./tests/configs/test.yaml")
        except TypeError:
            pytest.fail("Raised a TypeError when provided string for path. If running in test the test file is in tests/configs/test.yaml")

    def test_parse_yaml_returns_dict(self):
        try:
            opts = config.parse_yaml("./tests/configs/test.yaml")
        except TypeError:
            pytest.fail("Raised a TypeError when provided string for path. If running in test the test file is in tests/configs/test.yaml")
        assert type(opts) is dict  # test you get a dict back when providing valid yaml
        assert opts == {'log_level': 'INFO', 'version': '0.0.0'}  # test the contents are parsed properly

    def test_default_config_returns_dict(self):
        assert type(config.default_config()) is dict

    # for more info on parameterize
    # https://docs.pytest.org/en/latest/parametrize.html#parametrize
    @pytest.mark.parametrize("prop,prop_type", [
        ("log_level", str),
    ], scope="class")
    def test_default_config_has_all_the_right_properties_and_prop_types(self, prop, prop_type):
        """overloaded test"""
        assert prop in config.default_config()
        assert type(config.default_config()[prop]) is prop_type
