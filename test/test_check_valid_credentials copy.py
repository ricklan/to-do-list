from app import check_valid_credentials

def test_valid_string_only_credential_of_length_8():
    '''
    This function tests a valid credential of length 8 made up of only strings
    '''
    credential = "abcdefgh"
    assert check_valid_credentials(credential) == True


def test_valid_string_only_credential_of_length_11():
    '''
    This function tests a valid credential of length 11 made up of only strings
    '''
    credential = "abcdefghxyz"
    assert check_valid_credentials(credential) == True

def test_valid_alphanumeric_credential_of_length_8():
    '''
    This function tests a valid alphanumeric credential of length 8
    '''
    credential = "abcd1234"
    assert check_valid_credentials(credential) == True

def test_valid_alphanumeric_credential_of_length_11():
    '''
    This function tests a valid alphanumeric credential of length 11
    '''
    credential = "abcd1234x6z"
    assert check_valid_credentials(credential) == True

def test_invalid_credential_all_number():
    '''
    This function tests a invalid credential of only numbers
    '''
    credential = "12345678"
    assert check_valid_credentials(credential) == False

def test_invalid_credential_with_symbols():
    '''
    This function tests a invalid credential that has symbols
    '''
    credential = "abcd!23$*%"
    assert check_valid_credentials(credential) == False

def test_invalid_credential_too_short():
    '''
    This function tests a invalid credential of 5 characters
    '''
    credential = "abcde"
    assert check_valid_credentials(credential) == False

def test_invalid_empty_credential():
    '''
    This function tests a invalid empty credential
    '''
    credential = ""
    assert check_valid_credentials(credential) == False