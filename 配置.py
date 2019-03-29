import yaml
import logging
import os

with open('配置/配置.yaml', encoding='utf8') as f:
    配置项 = yaml.load(f)

if os.path.isfile('配置/用户配置.yaml'):
    with open('配置/用户配置.yaml', encoding='utf8') as f:
        配置项.update(yaml.load(f))


class 配置():
    @staticmethod
    def __getattribute__(x):
        return 配置项[x]


配置 = 配置()

if __name__ == '__main__':
    print(配置项)
