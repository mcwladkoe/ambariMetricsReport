import string
from collections import OrderedDict

COLUMNS_DICT = OrderedDict({
    'Timestamp': 'Время выполнения',
    'In._avg (B)': 'Средний Входящий трафик (байт)',
    'Out._avg (B)': 'Средний Исходящий трафик (байт)',
    '1-min._avg': 'Поминутно(?)',
    'CPUs._avg': 'Процессоров Средний',
    'Procs._avg': 'Процессоров задействовано',
    'Nodes._avg': 'Нод задействовано',
    'Nice._avg (%)': '(?)',
    'System._avg (%)': 'Загрузка системы',
    'User._avg (%)': 'Загрузка системы пользователем',
    'Idle._avg (%)': 'Простой системы',
    'Buffer._avg (B)': 'Буфер',
    'Cache._avg (B)': 'Кеш',
    'Share._avg (B)': 'Общая память',
    'Swap._avg (B)': 'SWAP',
    'Total._avg (B)': 'Всего'
})

COLUMNS_RANGE = list(string.ascii_uppercase[1:16])
