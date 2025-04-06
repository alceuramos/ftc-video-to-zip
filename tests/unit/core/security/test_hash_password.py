from core.security import hash_password


def test_hash_password():
    password = "mysecretpassword"
    hashed_password = hash_password(password)
    same_hashed_password = hash_password(password)
    assert isinstance(hashed_password, str)
    assert len(hashed_password) == 64
    assert hashed_password != password
    assert hashed_password == same_hashed_password
