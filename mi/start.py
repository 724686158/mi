#-*- coding: utf-8 -*-
import scrapy.cmdline as cmd
from commands.startpush import StartPush
startpush = StartPush()
startpush.push()
cmd.execute('scrapy crawlall'.split())