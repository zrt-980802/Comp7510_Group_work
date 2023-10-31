'''
Define a variable from storing values that will be accessed globally
If you want to share the values in different py files,
you can put them in appData
e.g. exmample.py:
from Global import appData
appData.num = 100
'''


class AppData:
    ...


appData = AppData()
