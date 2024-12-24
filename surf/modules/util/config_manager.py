# -*- coding: utf-8 -*-
"""
Created By      : ZedFeorius
Created Time    : 2024/12/18 0:51
File Name       : ConfigManager
Last Edit Time  : 
"""
import os
import tomlkit
from surf.appsGlobal import CONFIGHOME
from typing import Any


class TomlConfigManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self, config_file: str = os.path.join(CONFIGHOME, 'surf.toml')):
        if self.__initialized:
            return
        self.config_file = config_file
        self._doc = self._load()
        self.__initialized = True

    def _load(self):
        """加载配置文件到内存，如果文件不存在则创建空文件。"""
        if not os.path.exists(self.config_file):
            with open(self.config_file, 'w', encoding='utf-8') as f:
                f.write("")  # 创建空的 TOML 配置文件
            return tomlkit.document()
        with open(self.config_file, 'r', encoding='utf-8') as f:
            content = f.read()
        if content.strip() == '':
            return tomlkit.document()
        return tomlkit.parse(content)

    def get(self, section: str, option: str, fallback: Any = None) -> Any:
        """获取配置项的字符串值，如果不存在则返回fallback。"""
        return self._doc.get(section, {}).get(option, fallback)

    def get_int(self, section: str, option: str, fallback: int = None) -> int:
        """获取整型配置值，如果不存在则返回fallback。"""
        value = self.get(section, option, fallback)
        try:
            return int(value)
        except (ValueError, TypeError):
            return fallback

    def get_boolean(self, section: str, option: str, fallback: bool = None) -> bool:
        """获取布尔类型的配置值，如果不存在则返回fallback。"""
        value = self.get(section, option, fallback)
        if isinstance(value, bool):
            return value
        # 尝试根据字符串转换为布尔值
        if isinstance(value, str):
            val_lower = value.lower()
            if val_lower in ["true", "yes", "on"]:
                return True
            elif val_lower in ["false", "no", "off"]:
                return False
        return fallback

    def set(self, section: str, option: str, value: Any):
        """设置配置项的值，如果section不存在则创建。"""
        if section not in self._doc:
            self._doc[section] = tomlkit.table()
        self._doc[section][option] = value

    def remove_option(self, section: str, option: str):
        """移除某个配置项。"""
        if section in self._doc and option in self._doc[section]:
            del self._doc[section][option]

    def remove_section(self, section: str):
        """移除某个配置章节。"""
        if section in self._doc:
            del self._doc[section]

    def save(self):
        """将内存中的配置写回文件。"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            f.write(tomlkit.dumps(self._doc))


if __name__ == '__main__':
    # 使用示例
    cm = TomlConfigManager('config.toml')

    # 获取配置项
    db_host = cm.get('database', 'host', fallback='127.0.0.1')
    db_port = cm.get_int('database', 'port', fallback=3306)
    log_level = cm.get('logging', 'level', fallback='DEBUG')

    print(f'Database host: {db_host}')
    print(f'Database port: {db_port}')
    print(f'Logging level: {log_level}')

    # 修改配置项
    cm.set('database', 'port', 5433)
    cm.set('logging', 'level', 'DEBUG')

    # 增加新配置项
    cm.set('app', 'debug_mode', True)

    # 删除配置项
    cm.remove_option('logging', 'file')

    # 保存修改
    cm.save()
