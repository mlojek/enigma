from exceptions import Rotor_Error, Plugboard_Error, Enigma_Error
import argparse
import json

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

rotor = {
    '1': {
        'cipher': 'EKMFLGDQVZNTOWYHXUSPAIBRCJ',
        'notch': 'Q'
    },
    '2': {
        'cipher': 'AJDKSIRUXBLHWTMCQGZNPYFVOE',
        'notch': 'E'
    },
    '3': {
        'cipher': 'BDFHJLCPRTXVZNYEIWGAKMUSQO',
        'notch': 'V'
    },
    '4': {
        'cipher': 'ESOVPZJAYQUIRHXLNFTGKDCMWB',
        'notch': 'J'
    },
    '5': {
        'cipher': 'VZBRGITYUPSDNHLXAWMJQOFECK',
        'notch': 'Z'
    }
}

reflector = {
    'A': 'EJMZALYXVBWFCRQUONTSPIKHGD',
    'B': 'YRUHQSLDPXNGOKMIEBFZCWVJAT',
    'C': 'FVPJIAOYEDRZXWGCTKUQSBNMHL'
}


def shift_char(char: str, shift_value: int) -> str:
    '''Encrypts a letter of the alphabet in caesar cipher'''

    if not type(char) == str:
        raise TypeError('Not a valid input type')
    if len(char) > 1:
        raise ValueError('Only one letter at the time can be encrypted')
    if char.upper() not in alphabet:
        raise ValueError('Not a valid alphabet letter')

    index = alphabet.index(char.upper())
    index += shift_value
    index %= 26
    return alphabet[index]


def caesar_shift(string: str, shift_value: int) -> str:
    '''Encrypts a string in caesar cipher'''

    if not type(string) == str:
        raise TypeError('Not a valid string')

    resulting_string = ''
    for char in string.upper():
        if char in alphabet:
            resulting_string += shift_char(char, shift_value)
        else:
            resulting_string += char
    return resulting_string


def create_plugboard_dict(string: str) -> dict:
    '''Creates a plugboard dictionary object from string
    INPUT: pairs of letters A-Z divided by spaces'''

    plugboard = {}

    if len(string) == 0:
        return plugboard

    for pair in string.split(' '):
        pair = pair.upper()

        if pair[0] == pair[1]:
            raise Plugboard_Error('A letter cannot be connected to itself')
        if not len(pair) == 2:
            raise Plugboard_Error('Plugboard connection must link two letters')
        if pair[0] in plugboard.keys() or pair[1] in plugboard.keys():
            raise Plugboard_Error('A single letter can be connected only once')

        plugboard[pair[0]] = pair[1]
        plugboard[pair[1]] = pair[0]
    return plugboard


def enigma_from_json(path: str) -> object:
    '''Creates Enigma object with settings from json file'''
    file_handle = open(path, 'r')
    settings = json.load(file_handle)

    rotors = settings['rotors'] or '123'
    ringset = settings['ring_setting'] or 'AAA'
    position = settings['position'] or 'AAA'
    reflector = settings['reflector'] or 'A'
    plugboard = settings['plugboard'] or ''

    resulting_enigma = Enigma(rotors, ringset, position, reflector, plugboard)
    return resulting_enigma


class Rotor:
    '''Simulates Enigma Rotor
        rotor_type:         one character, 1-5
        ring_setting:       one character, A-Z
        starting_letter:    one character, A-Z
    '''
    def __init__(self, rotor_type: str, ring_setting: str,
                 starting_letter: str):

        # Exceptions raising for invalid input data:
        if ring_setting.upper() not in alphabet:
            raise Rotor_Error('Invalid ring setting')
        if starting_letter.upper() not in alphabet:
            raise Rotor_Error('Invalid starting letter')
        if rotor_type not in rotor.keys():
            raise Rotor_Error(f'{rotor_type} is not a valid rotor name')

        # Setting the rotor parameters:
        self._rotor_type = rotor_type
        self._ring_setting = ring_setting.upper()
        self._position = 'A'
        self._cipher = rotor[rotor_type]['cipher']
        self._notch = rotor[rotor_type]['notch']

        # Setting rotor position and ring setting:
        ring_shift = -1 * alphabet.index(self._ring_setting)
        self._shift_cipher(ring_shift)
        self._notch = caesar_shift(self._notch, ring_shift)
        self.set_position(starting_letter.upper())

    # Rotor turn methods:

    def _shift_cipher(self, shift_value: int) -> None:
        '''Shifts the rotor cipher to left and by caesar cipher'''

        shift_value %= 26
        self._cipher = caesar_shift(self._cipher, -1 * shift_value)
        self._cipher = self._cipher[shift_value:] + self._cipher[0:shift_value]

    def turn(self) -> bool:
        '''Turns the rotor, returns true if reached the notch'''

        turnover = (self._position == self._notch)
        self._shift_cipher(1)
        self._position = shift_char(self._position, 1)
        return turnover

    # Encryption methods:

    def liro(self, char: str) -> str:
        '''Left in right out character encryption'''

        if not type(char) == str:
            raise TypeError('Encrypted value must be a string')
        if len(char) > 1:
            raise ValueError('Only one character at the time can be encrypted')
        if char.upper() not in alphabet:
            raise ValueError('Invalid character')

        letter = self._cipher.index(char.upper())
        return alphabet[letter]

    def rilo(self, char: str) -> str:
        '''Right in left out character encryption'''

        if not type(char) == str:
            raise TypeError('Encrypted value must be a string')
        if len(char) > 1:
            raise ValueError('Only one character at the time can be encrypted')
        if char.upper() not in alphabet:
            raise ValueError('Invalid character')

        letter = alphabet.index(char)
        return self._cipher[letter]

    # Getters:

    def rotor_type(self) -> str:
        '''Returns rotor type'''
        return self._rotor_type

    def position(self) -> str:
        '''Returns current position (letter)'''
        return self._position

    def ring_setting(self) -> str:
        '''Returns ring setting of the rotor (letter)'''
        return self._ring_setting

    def at_notch(self) -> bool:
        '''True if rotor at notch position'''
        if self._position == self._notch:
            return True
        else:
            return False

    # Setters:

    def set_position(self, new_position: str) -> None:
        '''Sets the rotor to a new position'''

        if not type(new_position) == str:
            raise TypeError('New position must be of string type!')
        if new_position.upper() not in alphabet:
            raise ValueError('New position must be a letter of the alphabet!')
        if len(new_position) > 1:
            raise ValueError('New position must be a single letter!')

        new_position = new_position.upper()
        jump = alphabet.index(new_position) - alphabet.index(self._position)
        jump %= 26
        self._shift_cipher(jump)
        self._position = new_position


class Enigma:
    '''Simulates an Enigma encryption machine.

    rotors:             3 numbers 1-5, default 123
    ring_setting:       3 letters A-Z, default AAA
    starting_position:  3 letters A-Z, default AAA
    reflector_type:     1 letter A-C, default A
    plugboard:          optional, pairs of letters divided by spaces A-Z
    '''
    def __init__(self, rotors: str = '123', ring_setting: str = 'AAA',
                 starting_position: str = 'AAA', reflector_type: str = 'A',
                 plugboard: str = '') -> object:

        if not type(rotors) == str:
            raise TypeError('Invalid input type (rotors)')
        if not type(ring_setting) == str:
            raise TypeError('Invalid input type (ring setting)')
        if not type(starting_position) == str:
            raise TypeError('Invalid input type (starting position)')
        if not type(reflector_type) == str:
            raise TypeError('Invalid input type (reflector type)')
        if not type(plugboard) == str:
            raise TypeError('Invalid input type (plugboard)')

        ring_setting = ring_setting.upper()
        starting_position = starting_position.upper()
        reflector_type = reflector_type.upper()

        if not len(rotors) == 3:
            raise ValueError('Invalid input length (rotors)')
        for number in rotors:
            if number not in '12345':
                raise ValueError('Invalid input value (rotors)')
        if not len(ring_setting) == 3:
            raise ValueError('Invalid input length (ring setting)')
        for letter in ring_setting:
            if letter not in alphabet:
                raise ValueError('Invalid input value (ring setting)')
        if not len(starting_position) == 3:
            raise ValueError('Invalid input length (starting position)')
        for letter in starting_position:
            if letter not in alphabet:
                raise ValueError('Invalid input value (starting position)')
        if reflector_type not in 'ABC':
            raise ValueError('Invalid input value (reflector type)')
        if not len(reflector_type) == 1:
            raise ValueError('Invali input length (reflector type)')

        self._rotors = [
            Rotor(rtype, ring, letter)
            for rtype, ring, letter
            in zip(rotors, ring_setting, starting_position)
        ]
        self._reflector = reflector[reflector_type]
        self._plugboard = create_plugboard_dict(plugboard)

        # Settings dictionary:
        self._settings_dict = {}
        self._settings_dict['rotors'] = rotors
        self._settings_dict['ring_setting'] = ring_setting
        self._settings_dict['position'] = starting_position
        self._settings_dict['reflector'] = reflector_type
        self._settings_dict['plugboard'] = self.plugboard_string

    def turn(self) -> None:
        '''Turns the rotors of the machine'''

        if self._rotors[1].at_notch():
            self._rotors[1].turn()
            self._rotors[0].turn()

        if self._rotors[2].turn():
            self._rotors[1].turn()

    # Encryption:

    def encrypt_char(self, char: str) -> str:
        '''Encrypts a single character'''

        self.turn()
        letter = char.upper()
        letter = self._plugboardyse(letter)
        letter = self._rotors[2].rilo(letter)
        letter = self._rotors[1].rilo(letter)
        letter = self._rotors[0].rilo(letter)
        letter = self._reflector[alphabet.index(letter)]
        letter = self._rotors[0].liro(letter)
        letter = self._rotors[1].liro(letter)
        letter = self._rotors[2].liro(letter)
        letter = self._plugboardyse(letter)
        return letter

    def encrypt(self, string: str) -> str:
        '''Encrypts a message letter by letter, groups
        result string by 5 characters'''

        encrypted_message = ''
        separator = 0

        for char in string:
            if char in (' ', '\t', '\n'):
                continue
            if char.upper() not in alphabet:
                raise Enigma_Error(f'Invalid character to encypt {char}')

            encrypted_message += self.encrypt_char(char.upper())
            separator += 1

            if separator == 5:
                separator = 0
                encrypted_message += ' '

        return encrypted_message

    def _plugboardyse(self, letter: str) -> str:
        '''Private, passes letter through plugboard
        or returns it unchanged if not connected'''

        result = letter.upper()

        if result not in alphabet:
            raise ValueError('Input value not valid')

        if result in self._plugboard.keys():
            result = self._plugboard[result]
        return result

    # Plugboard modifyers:

    def add_connection(self, letters: str) -> None:
        '''Connects given letters on the plugboards
        letters:    2 letters of alphabet'''

        if not type(letters) == str:
            raise TypeError('Invalid input type')
        if not len(letters) == 2:
            raise ValueError('Invalid input length')
        if letters[0] == letters[1]:
            raise ValueError('A letter cannot be connected to itself')
        if letters[0].upper() in self._plugboard.keys():
            raise ValueError('Letter already connected')
        if letters[1].upper() in self._plugboard.keys():
            raise ValueError('Letter already connected')

        self._plugboard[letters[0]] = letters[1]
        self._plugboard[letters[1]] = letters[0]

    def delete_connection(self, letter: str) -> None:
        '''Deletes the connection involving input letter
        doesnt raise any exception if letter not connected'''

        if self._plugboard[letter]:
            self._plugboard.pop(self._plugboard[letter])
            self._plugboard.pop(letter)

    def new_plugboard(self, pairs: str) -> None:
        '''Creates a new plugboard dict from input'''
        try:
            self._plugboard = create_plugboard_dict(pairs)
        except Plugboard_Error:
            raise Plugboard_Error('Invalid input')

    # Getters:

    def plugboard_string(self) -> str:
        '''Returns plugboard as a string of letter pairs'''

        resulting_string = ''
        for key in self._plugboard.keys():
            if key not in resulting_string:
                resulting_string += key
                resulting_string += self._plugboard[key]
                resulting_string += ' '
        resulting_string = resulting_string.rstrip()
        return resulting_string

    def position(self) -> str:
        '''Returns the current position of rotors'''

        result = ''
        for rotor in self._rotors:
            result += rotor.position()
        return result

    # Other:

    def save_settings_to_json(self, path: str) -> None:
        '''Updates settings dictionary and dumps it to a json file'''
        self._settings_dict['position'] = self.position()
        self._settings_dict['plugboard'] = self.plugboard_string()

        file_handle = open(path, 'w')
        json.dump(self._settings_dict, file_handle, indent=4)


def main():
    '''Parser for batch use'''

    # Parser arguments:
    parser = argparse.ArgumentParser()
    parser.add_argument('-message', '-m',
                        help='message to encrypt')
    parser.add_argument('-rotors', '-r',
                        help='rotors, 3 numbers 1-5')
    parser.add_argument('-setting', '-s',
                        help='ring setting, 3 letters A-Z')
    parser.add_argument('-position', '-p',
                        help='starting position, 3 letters A-Z')
    parser.add_argument('-reflector', '-e',
                        help='reflector type, 1 letter A-C')
    parser.add_argument('-board', '-b',
                        help='plugboard connections, divided by spaces')
    parser.add_argument('-fromfile', '-f',
                        help='file with message to encode')
    parser.add_argument('-tofile', '-t',
                        help='file to save resulting message')
    parser.add_argument('-verbosetofile', '-v',
                        help='like tofile but also prints the result')

    # Setting up the enigma machine:
    args = parser.parse_args()
    rotors = args.rotors or '123'
    setting = args.setting or 'AAA'
    position = args.position or 'AAA'
    reflector = args.reflector or 'A'
    board = args.board or ''
    enigma = Enigma(rotors, setting, position, reflector, board)

    # Input encryption. Note that text file has priority to terminal input
    content_table = []
    if args.fromfile:
        file_handle = open(args.fromfile, 'r')
        for line in file_handle:
            content_table.append(enigma.encrypt(line))
    elif args.message:
        content_table = enigma.encrypt(args.message)

    # Encrypted message output. Output file has priority over terminal
    if args.tofile:
        file_handle = open(args.tofile, 'w')
        for line in content_table:
            file_handle.write(line)
    elif args.verbosetofile:
        file_handle = open(args.verbosetofile, 'w')
        for line in content_table:
            file_handle.write(line)
            print(line)
    else:
        for line in content_table:
            print(line)


if __name__ == "__main__":
    main()
