from copy import deepcopy
from transitions import Machine


class CoffeeMachine(object):

    states = ['order_coffee', 'receive_money', 'return_change', 'make_coffee']

    coffee_menu = {
        1: ("Эспрессо", 100),
        2: ("Американо", 120),
        3: ("Латте", 150),
        4: ("Капучино", 150),
        5: ("Мокка", 270)
    }

    def __init__(self, name='coffee_machine_home'):
        self.name = name
        self.total_order_cost = 0
        self.machine_bank = {'1000': 10, '500': 10, '100': 2, '50': 1, '10': 1}
        self.user_bank = 0
        self.additional_money = 0
        self.machine = Machine(states=CoffeeMachine.states, initial='order_coffee')

        self.machine.add_transition(trigger='order_coffee', source='order_coffee', dest='receive_money')
        self.machine.add_transition(trigger='receive_money', source='receive_money', dest='return_change')
        self.machine.add_transition(trigger='return_change', source='return_change', dest='make_coffee')
        self.machine.add_transition(trigger='make_coffee', source='make_coffee', dest='order_coffee')
        self.machine.add_ordered_transitions()

    def display_coffee_menu(self):
        if self.machine.state == 'order_coffee':
            print('выберите кофе: ')
            for number, coffee in self.coffee_menu.items():
                print(f"{number} - {coffee[0]} - {coffee[1]} рублей")
            try:
                choice = int(input())
                if choice in self.coffee_menu:
                    self.total_order_cost = self.coffee_menu[choice][1]
                    self.machine.order_coffee()
                else:
                    print('Неверный выбор, попробуйте снова.')
                    self.display_coffee_menu()
            except ValueError:
                print('вы ввели не число, попробуйте снова: ')
                self.display_coffee_menu()
        else:
            print('Текущее состояние машины: ', self.machine.state)
            print('Неверное состояние машины для отображения меню.')


    def recive_money(self):
        if self.machine.state == 'receive_money':
            print('стоимость заказа: ', self.total_order_cost, ' рублей')
            while True:
                try:
                    money = int(input("Введите сумму купюры: "))
                    if money >= 0:
                        money_str = str(money)
                        if money_str in self.machine_bank:
                            self.user_bank += money
                            self.machine_bank[money_str] += 1
                            if self.user_bank >= self.total_order_cost:
                                self.machine.receive_money()
                                break
                        else:
                            print("Такой купюры нет в машине, попробуйте снова.")

                except ValueError:
                    print('вы ввели не число, попробуйте снова: ')
        else:
            print('Что то пошло не так :(')

    def calculate_change(self, change: int) -> bool:
        check_change = {}
        variants_bank = deepcopy(self.machine_bank)
        sorted_keys = sorted(variants_bank.keys(), key=int, reverse=True)
        for key in sorted_keys:
            key_value = int(key)
            if key_value <= change:
                num_notes = min(change // key_value, variants_bank[key])
                if num_notes > 0:
                    check_change[key_value] = num_notes
                    change -= num_notes * key_value
                    variants_bank[key] -= num_notes

                if change == 0:
                    break

        if change > 0:
            keys = [int(key) for key in self.machine_bank.keys() if int(key) >= change and self.machine_bank[key] > 0]
            if keys:
                additional_money = change-self.additional_money
                print(f'Необходимо внести еще: {additional_money} рублей.')
            else:
                print('Невозможно выдать сдачу.')
            return False
        else:
            self.machine_bank = variants_bank
            print('Сдача выдана успешно.')
            print('Выдано:', check_change)
            return True

    def return_change(self):
        if self.machine.state == 'return_change':
            print('Стоимость заказа:', self.total_order_cost, 'рублей')
            print('Ваш баланс:', self.user_bank, 'рублей')

            if self.user_bank == self.total_order_cost:
                self.user_bank -= self.total_order_cost
                self.total_order_cost = 0
                print('Сдача не требуется.')
                return

            change = self.user_bank - self.total_order_cost
            print('Ваша сдача:', change, 'рублей')

            success = self.calculate_change(change)

            while not success:
                try:
                    additional_money = int(input('Нужно добавить еще: '))
                    if additional_money >= 0:
                        additional_money_str = str(additional_money)
                        if additional_money_str in self.machine_bank:
                            if self.user_bank + additional_money >= self.user_bank + change:
                                print('Вы внесли слишком много денег, попробуйте снова.')
                                continue
                            self.user_bank += additional_money
                            self.additional_money += additional_money
                            self.machine_bank[additional_money_str] += 1
                            change = self.user_bank - self.total_order_cost
                            success = self.calculate_change(change)
                        else:
                            print("Такой купюры нет в машине, попробуйте снова.")
                    else:
                        print('Сумма не может быть отрицательной, попробуйте снова.')
                except ValueError:
                    print('Вы ввели не число, попробуйте снова.')

            if success:
                self.user_bank -= self.total_order_cost
                self.total_order_cost = 0
                print('Ваша сдача:', change, 'рублей')
                print('Сдача возвращена.')


    def make_coffee(self):
        print('делаю кофе')
        print('кофе можно забирать...')


def start():
    while True != 'q':
        coffe_machine = CoffeeMachine()

        coffe_machine.display_coffee_menu()
        coffe_machine.recive_money()
        coffe_machine.return_change()
        coffe_machine.make_coffee()
        user_input = input('нажмите q для выхода и любую другю кнопку для продолжения...')
        if user_input == 'q':
            break


if __name__ == '__main__':
    start()