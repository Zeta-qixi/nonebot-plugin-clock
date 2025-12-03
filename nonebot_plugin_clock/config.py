from pydantic import BaseModel, Field
from pathlib import Path
from nonebot import require, get_plugin_config

require("nonebot_plugin_localstore")
import nonebot_plugin_localstore as store


class Config(BaseModel):
    group_at_me: bool = Field(default=True)
    use_llm: bool = Field(default=False)

clock_config = get_plugin_config(Config)
AT_ME = clock_config.group_at_me
USE_LLM = clock_config.use_llm

DB_PATH = store.get_plugin_data_file("data.db")
IMAGE_DIR = store.get_plugin_data_file('images')