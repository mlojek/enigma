import pytest
from enigma import (shift_char, caesar_shift,
                    create_plugboard_dict, Rotor, Enigma)
from exceptions import Rotor_Error, Plugboard_Error, Enigma_Error


def test_rotor_invalid_type():
    with pytest.raises(Rotor_Error):
        Rotor('S', 'A', 'A')


def test_rotor_invalid_ring_setting():
    with pytest.raises(Rotor_Error):
        Rotor('1', '2', 'A')


def test_rotor_invalid_starting_position():
    with pytest.raises(Rotor_Error):
        Rotor('1', 'A', '?')


def test_rotot_lowercase_init():
    Rotor('1', 'a', 'u')


def test_rotor_initial_position():
    test_rotor = Rotor('1', 'K', 'M')
    assert test_rotor.position() == 'M'


def test_rotor_turn_postition():
    test_rotor = Rotor('1', 'K', 'F')
    test_rotor.turn()
    assert test_rotor.position() == 'G'


def test_rotor_liro_string():
    test_rotor = Rotor('1', 'K', 'F')
    with pytest.raises(ValueError):
        test_rotor.liro('Toomanycharacters')


def test_rotor_liro_invalid_char():
    test_rotor = Rotor('1', 'K', 'F')
    with pytest.raises(ValueError):
        test_rotor.liro(' ')


def test_rotor_liro_invalid_input_type():
    test_rotor = Rotor('1', 'K', 'F')
    with pytest.raises(TypeError):
        test_rotor.liro(2)


def test_rotor_rilo_string():
    test_rotor = Rotor('1', 'K', 'F')
    with pytest.raises(ValueError):
        test_rotor.rilo('Toomanycharacters')


def test_rotor_rilo_invalid_char():
    test_rotor = Rotor('1', 'K', 'F')
    with pytest.raises(ValueError):
        test_rotor.rilo(' ')


def test_rotor_rilo_invalid_input_type():
    test_rotor = Rotor('1', 'K', 'F')
    with pytest.raises(TypeError):
        test_rotor.rilo(2)


def test_rotor_type():
    test_rotor = Rotor('2', 'N', 'F')
    assert test_rotor.rotor_type() == '2'


def test_rotor_ring_setting():
    test_rotor = Rotor('1', 'F', 'K')
    assert test_rotor.ring_setting() == 'F'


def test_rotor_set_position():
    test_rotor = Rotor('1', 'F', 'K')
    test_rotor.set_position('N')
    assert test_rotor.position() == 'N'


def test_rotor_set_position_not_string():
    test_rotor = Rotor('1', 'F', 'K')
    with pytest.raises(TypeError):
        test_rotor.set_position(3)


def test_rotor_set_position_invalid():
    test_rotor = Rotor('1', 'F', 'K')
    with pytest.raises(ValueError):
        test_rotor.set_position(' ')


def test_rotor_set_position_too_long():
    test_rotor = Rotor('1', 'F', 'K')
    with pytest.raises(ValueError):
        test_rotor.set_position('Toolongpositionname')


def test_shift_char_not_string():
    with pytest.raises(TypeError):
        shift_char(2, 3)


def test_shift_char_too_long():
    with pytest.raises(ValueError):
        shift_char('Toolonginputstring', 3)


def test_shift_char_not_letter():
    with pytest.raises(ValueError):
        shift_char(' ', 3)


def test_caesar_shift_not_string():
    with pytest.raises(TypeError):
        caesar_shift(3, 3)


def test_caesar_shift_lowercase():
    assert caesar_shift('abcdstu', 2) == 'CDEFUVW'


def test_caesar_shift_nonletters():
    assert caesar_shift(' ?!@$ ?', 5) == ' ?!@$ ?'


def test_caesar_shift_mixed_charcters():
    assert caesar_shift('Test message! 1234', 7) == 'ALZA TLZZHNL! 1234'


def test_plugboard_self_connect():
    with pytest.raises(Plugboard_Error):
        create_plugboard_dict('AA')


def test_plugboard_too_many_connected():
    with pytest.raises(Plugboard_Error):
        create_plugboard_dict('GGG')


def test_plugboard_already_connected():
    with pytest.raises(Plugboard_Error):
        create_plugboard_dict('AS SF')


def test_plugboard_lowercase():
    assert create_plugboard_dict('ad fh')


def test_plugboard_empty():
    assert create_plugboard_dict('') == {}


def test_enigma_init_rotor_type():
    with pytest.raises(TypeError):
        Enigma(123, 'AAA', 'AAA', 'A', '')


def test_enigma_init_ring_type():
    with pytest.raises(TypeError):
        Enigma('123', 123, 'AAA', 'A', '')


def test_enigma_init_position_type():
    with pytest.raises(TypeError):
        Enigma('123', 'AAA', 123, 'A', '')


def test_enigma_init_reflector_type():
    with pytest.raises(TypeError):
        Enigma('123', 'AAA', 'AAA', 123, '')


def test_enigma_init_plugboard_type():
    with pytest.raises(TypeError):
        Enigma('123', 'AAA', 'AAA', 'A', 123)


def test_enigma_init_rotor_length():
    with pytest.raises(ValueError):
        Enigma('1')


def test_enigma_init_rotor_value():
    with pytest.raises(ValueError):
        Enigma('238')


def test_enigma_init_ring_length():
    with pytest.raises(ValueError):
        Enigma('123', 'A')


def test_enigma_init_ring_value():
    with pytest.raises(ValueError):
        Enigma('123', '!@#')


def test_enigma_init_position_length():
    with pytest.raises(ValueError):
        Enigma('123', 'AAA', 'A')


def test_enigma_init_position_value():
    with pytest.raises(ValueError):
        Enigma('123', 'AAA', '!@#')


def test_enigma_init_reflector_value():
    with pytest.raises(ValueError):
        Enigma('123', 'AAA', 'AAA', 'U')


def test_enigma_init_reflector_length():
    with pytest.raises(ValueError):
        Enigma('123', 'AAA', 'AAA', 'AA')


def test_enigma_turn():
    enigma = Enigma('123', 'AAA', 'ADU')
    assert enigma.position() == 'ADU'
    enigma.turn()
    assert enigma.position() == 'ADV'
    enigma.turn()
    assert enigma.position() == 'AEW'
    enigma.turn()
    assert enigma.position() == 'BFX'
    enigma.turn()
    assert enigma.position() == 'BFY'


def test_enigma_encrypt_special_char():
    enigma = Enigma()
    with pytest.raises(Enigma_Error):
        enigma.encrypt('!@#')


def test_enigma_plugboard_string():
    enigma = Enigma()
    enigma.new_plugboard('AB ID KC LW')
    assert enigma.plugboard_string() == 'AB ID KC LW'


def test_enigma_add_connection():
    enigma = Enigma()
    enigma.new_plugboard('AB ID KC LW')
    enigma.add_connection('ER')
    assert enigma.plugboard_string() == 'AB ID KC LW ER'


def test_enigma_delete_connection():
    enigma = Enigma()
    enigma.new_plugboard('AB ID KC LW')
    enigma.delete_connection('I')
    assert enigma.plugboard_string() == 'AB KC LW'
