from app import check_valid_name

def test_valid_name():
    '''
    This function tests a valid name
    '''
    credential = "abcdefgh"
    assert check_valid_name(credential) == True


def test_invalid_name_with_numbers():
    '''
    This function tests an invalid name with numbers
    '''
    credential = "abcd234"
    assert check_valid_name(credential) == False

def test_invalid_name_with_symbols():
    '''
    This function tests an invalid name with symbols
    '''
    credential = "abc#$%"
    assert check_valid_name(credential) == False

def test_invalid_name_with_symbols_and_numbers():
    '''
    This function tests an invalid name with symbols and numbers
    '''
    credential = "abc#$%456"
    assert check_valid_name(credential) == False

def test_invalid_empty_name():
    '''
    This function tests an invalid empty name
    '''
    credential = ""
    assert check_valid_name(credential) == False
