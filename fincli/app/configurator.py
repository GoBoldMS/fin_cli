from config.config import Config


def build_config(
    use_history: bool = False,
) -> Config:
    """Create the configuration."""
    config = Config()
    config.use_history = use_history
    return config    
    