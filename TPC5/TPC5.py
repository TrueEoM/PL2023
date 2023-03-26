import re
import sys

class PhoneBooth:
    def __init__(self):
        self.state = 'on_hook'
        self.credit = 0
        self.call_cost = 0
        self.number = ''
        self.valid_coins = ['5c', '10c', '20c', '50c', '1e', '2e']

    def process_input(self, input_str):
        input_str = input_str.strip().lower()

        if self.state == 'on_hook':
            if input_str == 'levantar':
                self.state = 'dial_tone'
                return "Introduza moedas."
            else:
                return "Telefone desligado."

        elif self.state == 'dial_tone':
            if input_str.startswith('moeda'):
                coins = input_str[6:].split(',')
                coins = [coin.strip() for coin in coins]
                valid_coins = [coin for coin in coins if coin in self.valid_coins]
                invalid_coins = [coin for coin in coins if coin not in self.valid_coins]

                if invalid_coins:
                    return f"{', '.join(invalid_coins)} - moeda inválida; saldo = {self.format_credit()}"

                for coin in valid_coins:
                    self.credit += self.parse_coin(coin)

                return f"saldo = {self.format_credit()}"

            elif input_str.startswith('t='):
                number = input_str[2:]

                if number.startswith('00'):
                    if self.credit < 150:
                        return f"saldo insuficiente; saldo = {self.format_credit()}"
                    else:
                        self.call_cost = 150
                        self.credit -= self.call_cost
                        self.number = number
                        self.state = 'dialing'
                        return f"Estabelecendo ligação para {self.number}..."

                elif number.startswith('601') or number.startswith('641'):
                    return f"Esse número não é permitido neste telefone. Queira discar novo número!"

                elif number.startswith('800'):
                    self.number = number
                    self.state = 'ringing'
                    return "A chamar..."

                elif number.startswith('808'):
                    self.number = number
                    self.call_cost = 10
                    self.credit -= self.call_cost
                    self.state = 'ringing'
                    return "A chamar..."

                elif number.startswith('2'):
                    if self.credit < 25:
                        return f"saldo insuficiente; saldo = {self.format_credit()}"
                    else:
                        self.call_cost = 25
                        self.credit -= self.call_cost
                        self.number = number
                        self.state = 'ringing'
                        return "A chamar..."

                else:
                    return f"Número inválido: {number}"

            elif input_str == 'abortar':
                coins = self.credit
                self.credit = 0
                self.state = 'on_hook'
                return f"troco={self.format_coins(coins)}; Volte sempre!"

            else:
                return "Comando inválido."

        elif self.state == 'dialing':
            return "Ligação em curso..."

        elif self.state == 'ringing':
            self.state = 'off_hook'
            return f"Ligação estabelecida para {self.number}."

        elif self.state == 'off_hook':
            if input_str == 'pousar':
                coins = self.credit - self.call_cost
                self.credit = 0
                self.call_cost = 0
                self.state = 'on_hook'
                return ""
