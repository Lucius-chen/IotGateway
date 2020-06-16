# -*- coding: utf-8 -*-
# @Time    : 2020/6/16 0016 17:37
# @Author  : lucius
# @Email   : cnotperfect@foxmail.com
import platform

platform_system = platform.system().lower()

def isWindos():
    return platform_system.find("win")>=0