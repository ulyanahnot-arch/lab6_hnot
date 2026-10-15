import unittest
import subprocess
from main import HourlyEmployee, FixedEmployee, FopEmployee, FreelanceEmployee

class TestEmployeeCalculations(unittest.TestCase):

    def test_hourly_employee(self):
        emp = HourlyEmployee("123", "Шевченко", 100)
        expected_salary = 20.8 * 8 * 100 # 16640.0
        expected_taxes = expected_salary * 0.195 # 3244.8
        
        self.assertAlmostEqual(emp.calculate_salary(), expected_salary)
        self.assertAlmostEqual(emp.calculate_taxes(), expected_taxes)

    def test_fixed_employee(self):
        emp = FixedEmployee("456", "Франко", 25000)
        expected_salary = 25000
        expected_taxes = 25000 * 0.195 # 4875.0
        
        self.assertAlmostEqual(emp.calculate_salary(), expected_salary)
        self.assertAlmostEqual(emp.calculate_taxes(), expected_taxes)

    def test_fop_employee(self):
        emp = FopEmployee("789", "Українка", 100, fop_group=3)
        base_hourly = 20.8 * 8 * 100
        expected_salary = base_hourly * 1.10 # 18304.0
        expected_taxes = (expected_salary * 0.05) + 1760 # 915.2 + 1760 = 2675.2
        
        self.assertAlmostEqual(emp.calculate_salary(), expected_salary)
        self.assertAlmostEqual(emp.calculate_taxes(), expected_taxes)

    def test_freelance_employee(self):
        emp = FreelanceEmployee("101", "Коцюбинський", 1000, 10)
        expected_salary = 10000
        expected_taxes = (10000 * 0.195) + 1760 # 1950 + 1760 = 3710.0
        
        self.assertAlmostEqual(emp.calculate_salary(), expected_salary)
        self.assertAlmostEqual(emp.calculate_taxes(), expected_taxes)

    def test_cli_execution(self):
        """Тестування роботи CLI за допомогою subprocess"""

        result = subprocess.run(
            ["python", "main.py", "--count", "50", "--min-income", "10000", "--fop-group", "3"],
            capture_output=True,
            text=True
        )
        

        self.assertEqual(result.returncode, 0)

        self.assertIn("Список працівників", result.stdout)

if __name__ == '__main__':
    unittest.main()