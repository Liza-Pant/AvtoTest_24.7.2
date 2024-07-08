from app.calculator import Calculator
import pytest

class TestCalc:
    def setup_method(self):
        self.calc = Calculator

    def test_multiply(self):
        assert self.calc.multiply(self, 5, 6) == 30

    def test_division(self):
        assert self.calc.division(self, 30, 6) == 5

    def test_subtraction(self):
        assert self.calc.subtraction(self, 5, 6) == -1

    def test_adding(self):
        assert self.calc.adding(self, 5, 6) == 11

    def teardown(self):
        print('Выполнение метода Teardown')

# assert self.calc.adding(self, 1, 1) == 2