from app.db.database import SessionLocal
from app.models.user import User
from pwdlib import PasswordHash

EMAIL = "iot-test-user@example.com"
NEW_PASSWORD = "Mypassword123"


def main() -> None:
    db = SessionLocal()

    try:
        user = db.query(User).filter(User.email == EMAIL).first()

        if user is None:
            raise RuntimeError(f"User not found: {EMAIL}")

        user.password_hash = PasswordHash.recommended().hash(NEW_PASSWORD)
        db.commit()

        print(f"PASSWORD RESET FOR: {user.email}")

        matches = PasswordHash.recommended().verify(
            NEW_PASSWORD,
            user.password_hash,
        )
        print("PASSWORD MATCH:", matches)

    finally:
        db.close()


if __name__ == "__main__":
    main()