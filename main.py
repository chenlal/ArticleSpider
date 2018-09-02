# -*- coding: utf-8 -*-
__Date__ = '2018/9/2 15:10'
__Author__ = 'jiayu.chen'
__File__ = 'main.py'

from scrapy.cmdline import execute
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

execute(["scrapy","crawl","jobbole"])