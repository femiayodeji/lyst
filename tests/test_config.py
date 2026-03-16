import unittest
from lyst.config import load_config, save_config, show_config, Config, LLMConfig, DBConfig

class TestConfig(unittest.TestCase):
    def test_config_save_and_load(self):
        config = Config(
            llm=LLMConfig(provider="test_provider", model="test_model", base_url="http://test-url.com", stream=True),
            db=DBConfig(connection="sqlite:///test.db")
        )
        save_config(config)
        loaded_config = load_config()
        self.assertEqual(config, loaded_config)

    def test_config_show(self):
        config = Config(
            llm=LLMConfig(provider="test_provider", model="test_model", base_url="http://test-url.com", stream=True),
            db=DBConfig(connection="sqlite:///test.db")
        )
        save_config(config)
        show_config()

    def test_config_missing_db(self):
        config = Config(
            llm=LLMConfig(provider="test_provider", model="test_model", base_url="http://test-url.com", stream=True),
            db=DBConfig(connection="")
        )
        save_config(config)
        self.assertEqual(load_config().db.connection, "")

    def test_config_missing_llm(self):
        config = Config(
            llm=LLMConfig(provider="", model="", base_url="", stream=False),
            db=DBConfig(connection="sqlite:///test.db")
        )
        save_config(config)
        loaded_config = load_config()
        self.assertEqual(loaded_config.llm.provider, "")
        self.assertEqual(loaded_config.llm.model, "")
        self.assertEqual(loaded_config.llm.base_url, "")
        self.assertFalse(loaded_config.llm.stream)

    
    def test_config_invalid_llm_model(self):
        config = Config(
            llm=LLMConfig(provider="test_provider", model="", base_url="http://test-url.com", stream=True),
            db=DBConfig(connection="sqlite:///test.db")
        )
        save_config(config)
        loaded_config = load_config()
        self.assertEqual(loaded_config.llm.model, "")
    


if __name__ == "__main__":
    unittest.main()