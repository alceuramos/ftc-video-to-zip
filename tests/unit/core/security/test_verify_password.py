from core.security import hash_password, verify_password


def test_verify_password_success():
    password = "mysecretpassword"
    hashed_password = hash_password(password)

    # Test successful password verification
    assert verify_password(password, hashed_password) is True


def test_verify_password_fail():
    password = "mysecretpassword"
    hashed_password = hash_password(password)
    # Test unsuccessful password verification with wrong password
    assert verify_password("wrongpassword", hashed_password) is False
