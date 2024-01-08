from unittest import TestCase
from yogomatt_temperature.command_line import *

class TestConsole(TestCase):
    def test_ds18b20(self):
        read_ds18b20()