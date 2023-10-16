"""Config file for the stock screener app."""
import datetime
import os
from core.configuration.config_base import Configurable, SystemSettings

class Config(SystemSettings):
    name: str = "Stock Screener CLI config"
    description: str = "Configuration for the Stock Screener CLI app."
    ########################
    # Application Settings #
    ########################
    use_history: bool = False
    filters: tuple = ()

    @staticmethod
    def file_path(file_name: str) -> str:
        """Return the path to the file."""
        date = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M')
        return os.path.join(os.getcwd(), f'workspace_output/{file_name}_{date}.csv')


#For late use if needed to define a strongly typed config builder.
class ConfigBuilder(Configurable[Config]):
    """Configuration builder class."""
    default_settings = Config()

    @classmethod
    def build_config_from_env(cls) -> Config:
        """Build the configuration."""
        config_dict = {
            "use_history": os.getenv("USE_HISTORY", default=cls.default_settings.use_history),
        }

        return Config(**config_dict)