from passlib.context import CryptContext


# Instance CryptContext using schemes algorithm bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hasher:
    """A class for hashing processing"""

    @staticmethod
    def verify_password(plain_password, hashed_password):
        """Getting two parameters and compared for confirm password"""

        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        """Getting password and hashes it"""

        return pwd_context.hash(password)
