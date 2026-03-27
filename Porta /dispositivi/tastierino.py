from machine import Pin
from dispositivi.keypad import Keypad
from time import sleep
from dispositivi.servoMotor import Servo
from dispositivi.oled import OledDisplayManager
import time

#Handler
class KeypadHandler:
    def __init__(self, righe, colonne, tasti):
        self.keypad = Keypad(righe, colonne, tasti)

    def get_key(self):
        return self.keypad.read_keypad()



#Classe del password manager
class PasswordManager:
    def __init__(self, password_length=4, correct_password=None):
        self.correct_password = correct_password or ['1', '1', '8', '5']
        self.input = [""] * password_length
        self.copy = [""] * password_length
        self.security = [""] * password_length
        self.index = 0
        self.show_mode = False

    def toggle_show(self):
        self.show_mode = not self.show_mode

    def delete_last(self):
        if self.index > 0:
            self.index -= 1
            self.input[self.index] = ""
            self.copy[self.index] = ""
            self.security[self.index] = ""

    def cancel_all(self):
        for j in range(len(self.input)):
            self.input[j] = ""
            self.copy[j] = ""
            self.security[j] = ""
        self.index = 0

    def add_char(self, char):
        if self.index < len(self.input):
            self.input[self.index] = char
            self.copy[self.index] = char
            self.security[self.index] = '*'
            self.index += 1

    def is_complete(self):
        return self.index == len(self.input)

    def is_correct(self):
        return self.input == self.correct_password

    def get_display(self):
        data = self.copy if self.show_mode else self.security
        return '  '.join(data[:self.index])



#Classe del'access controller
class AccessController:
    def __init__(self, servo, oled_manager=None):
        self.servo = servo
        self.oled_manager = oled_manager

    def grant_access(self):
        if self.oled_manager:
            self.oled_manager.clear()
            self.oled_manager.show_text("Door opening...",10,30)
        self.servo.open()
        self.oled_manager.clear()
        self.oled_manager.show_text("Opened!",35,30)
        sleep(3)
        self.oled_manager.show_text("Door closing...",10,30)
        self.servo.close()
        self.oled_manager.show_text("Closed!",35,30)
        sleep(2)
        self.oled_manager.clear()


    def deny_access(self):
        if self.oled_manager:
            self.oled_manager.show_text("Wrong password!",10,30)



#Classe del controller
class MainController:
    def __init__(self, righe_pins, colonne_pins, servo_pin, oled_manager=None):
        righe = [Pin(pin) for pin in righe_pins]
        colonne = [Pin(pin) for pin in colonne_pins]
        tasti = [
            ['1', '2', '3', 'Del'],
            ['4', '5', '6', 'Show'],
            ['7', '8', '9', 'Canc'],
            ['*', '0', '#', 'Go']
        ]

        self.oled = oled_manager
        self.keypad_handler = KeypadHandler(righe, colonne, tasti)
        self.password_manager = PasswordManager(correct_password=['1', '1', '8', '5'])
        servo = Servo(servo_pin)
        self.access_controller = AccessController(servo, oled_manager)

    def stampa(self):
        self.oled.clear()
        self.oled.display.text("Insert password: ", 0, 20)
        testo = self.password_manager.get_display()
        self.oled.display.text(testo, 24, 40)
        self.oled.display.show()

    def run(self, timeout=30):
        start_time = time.ticks_ms()
        self.stampa()
        
        while True:
            if time.ticks_diff(time.ticks_ms(), start_time) > timeout * 1000:
                self.oled.clear()
                self.oled.show_text("Timeout!", 35, 30)
                sleep(2)
                self.password_manager.cancel_all()
                self.oled.clear()
                return False

            key = self.keypad_handler.get_key()
            if key:
                if key == 'Show':
                    self.password_manager.toggle_show()
                    self.stampa()
                elif key == 'Del':
                    self.password_manager.delete_last()
                    self.stampa()
                elif key == 'Canc':
                    self.password_manager.cancel_all()
                    self.stampa()
                elif key == 'Go':
                    if self.password_manager.is_complete():
                        if self.password_manager.is_correct():
                            self.oled.show_text('Welcome!', 35, 30)
                            self.access_controller.grant_access()
                            self.password_manager.cancel_all()
                            return True
                        else:
                            self.oled.show_text('Wrong Password!', 5, 30)
                            sleep(0.5)
                            self.password_manager.cancel_all()
                            self.stampa()
                elif key not in ['Go']:
                    self.password_manager.add_char(key)
                    self.stampa()
            sleep(0.3)
