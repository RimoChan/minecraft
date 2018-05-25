import yaml
import logging

with open('配置/配置.yaml',encoding='utf8') as f:
    配置项=yaml.load(f)


class 配置():
    @staticmethod
    def __getattribute__(x):
        return 配置项[x]
配置=配置()