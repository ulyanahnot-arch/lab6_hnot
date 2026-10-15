import argparse
import random
from abc import ABC, abstractmethod
from faker import Faker

fake = Faker('uk_UA')


class Employee(ABC):
    def __init__(self, id_code, last_name):
        self.id_code = id_code
        self.last_name = last_name

    @abstractmethod
    def calculate_salary(self):
        """Обчислення середньомісячної заробітної плати"""
        pass

    @abstractmethod
    def calculate_taxes(self):
        """Обчислення податків із заробітної плати"""
        pass

    def __str__(self):

        return f"ID: {self.id_code} | Прізвище: {self.last_name:<15} | Зарплата: {self.calculate_salary():.2f} грн | Податки: {self.calculate_taxes():.2f} грн"


class HourlyEmployee(Employee):
    def __init__(self, id_code, last_name, hourly_rate):
        super().__init__(id_code, last_name)
        self.hourly_rate = hourly_rate

    def calculate_salary(self):
        # 20.8 робочих днів * 8 годин * погодинна ставка
        return 20.8 * 8 * self.hourly_rate

    def calculate_taxes(self):
        # ПДФО 18% + ВЗ 1.5% = 19.5%
        return self.calculate_salary() * 0.195


class FixedEmployee(Employee):
    def __init__(self, id_code, last_name, fixed_salary):
        super().__init__(id_code, last_name)
        self.fixed_salary = fixed_salary

    def calculate_salary(self):
        return self.fixed_salary

    def calculate_taxes(self):
        # ПДФО 18% + ВЗ 1.5% = 19.5%
        return self.calculate_salary() * 0.195

class FopEmployee(Employee):
    def __init__(self, id_code, last_name, hourly_rate, fop_group=3):
        super().__init__(id_code, last_name)
        self.hourly_rate = hourly_rate
        self.fop_group = fop_group  # Додано групу ФОП для можливості фільтрації

    def calculate_salary(self):
        # Зарплата погодинка + 10%
        base_salary = 20.8 * 8 * self.hourly_rate
        return base_salary * 1.10

    def calculate_taxes(self):
        # ЄП 5%, ЄСВ 1760 грн
        return (self.calculate_salary() * 0.05) + 1760


class FreelanceEmployee(Employee):
    def __init__(self, id_code, last_name, lines_of_code, price_per_line):
        super().__init__(id_code, last_name)
        self.lines_of_code = lines_of_code
        self.price_per_line = price_per_line

    def calculate_salary(self):
        # ціна за рядок * кількість рядків
        return self.lines_of_code * self.price_per_line

    def calculate_taxes(self):
        # ПДФО 18% + ВЗ 1.5% + ЄСВ 1760
        return (self.calculate_salary() * 0.195) + 1760



def generate_employees(count=20):
    employees = []
    for _ in range(count):
        id_code = str(random.randint(1000000000, 9999999999))
        last_name = fake.last_name()
        emp_type = random.choice(['hourly', 'fixed', 'fop', 'freelance'])

        if emp_type == 'hourly':
            employees.append(HourlyEmployee(id_code, last_name, hourly_rate=random.uniform(100, 500)))
        elif emp_type == 'fixed':
            employees.append(FixedEmployee(id_code, last_name, fixed_salary=random.uniform(15000, 80000)))
        elif emp_type == 'fop':
            employees.append(FopEmployee(id_code, last_name, hourly_rate=random.uniform(100, 500), fop_group=random.choice([2, 3])))
        elif emp_type == 'freelance':
            employees.append(FreelanceEmployee(id_code, last_name, lines_of_code=random.randint(500, 5000), price_per_line=random.uniform(5, 20)))
    
    return employees

def main():
    parser = argparse.ArgumentParser(description="CLI для управління працівниками ІТ підприємства")
    

    parser.add_argument("--count", type=int, default=15, help="Кількість працівників для генерації")
    parser.add_argument("--fop-group", type=int, help="Фільтр ФОП за групою (наприклад: 3)")
    parser.add_argument("--min-income", type=float, help="Мінімальний рівень доходу")
    parser.add_argument("--max-tax", type=float, help="Максимальна величина сплачених податків")
    
    args = parser.parse_args()

    employees = generate_employees(args.count)

    filtered_employees = employees
    
    if args.fop_group:
        filtered_employees = [e for e in filtered_employees if isinstance(e, FopEmployee) and e.fop_group == args.fop_group]
    
    if args.min_income:
        filtered_employees = [e for e in filtered_employees if e.calculate_salary() >= args.min_income]
        
    if args.max_tax:
        filtered_employees = [e for e in filtered_employees if e.calculate_taxes() <= args.max_tax]


    filtered_employees.sort(key=lambda x: (-x.calculate_salary(), x.last_name))

    print(f"{'='*80}\nСписок працівників ({len(filtered_employees)} знайдено):\n{'='*80}")
    for emp in filtered_employees:
        if isinstance(emp, FopEmployee):
             print(f"{emp} | (ФОП, Група {emp.fop_group})")
        else:
             print(emp)
    print(f"{'='*80}")

if __name__ == "__main__":
    main()