from fastapi import HTTPException, status

from app.users.commands import AuthenticateUserCommand, CreateUserCommand, UpdateUserCommand
from app.users.repository import UserRepository
from app.users.schemas import UserResponse
from app.utils.security import hash_password, verify_password

# Notice: no import from app.users.model — service is DB-agnostic.
# It passes data to the repository; the repository owns model construction.


class UserService:
    def __init__(self) -> None:  # no db — repository handles it internally
        self.repository = UserRepository()

    # ── commands (writes) ────────────────────────────────────────────────────

    def create(self, command: CreateUserCommand) -> UserResponse:
        if self.repository.get_by_email(command.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        user = self.repository.build(
            email=command.email,
            full_name=command.full_name,
            hashed_password=hash_password(command.password),
        )
        created = self.repository.create(user)
        return UserResponse.model_validate(created)

    def update(self, user_id: int, command: UpdateUserCommand) -> UserResponse:
        user = self._get_or_404(user_id)
        for field, value in command.model_dump(exclude_unset=True).items():
            setattr(user, field, value)
        self.repository.db.flush()
        self.repository.db.refresh(user)
        return UserResponse.model_validate(user)

    def delete(self, user_id: int) -> None:
        user = self._get_or_404(user_id)
        self.repository.delete(user)

    def authenticate(self, command: AuthenticateUserCommand) -> UserResponse:
        user = self.repository.get_by_email(command.email)
        if not user or not verify_password(command.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is inactive",
            )
        return UserResponse.model_validate(user)

    # ── queries (reads) ──────────────────────────────────────────────────────

    def get(self, user_id: int) -> UserResponse:
        user = self._get_or_404(user_id)
        return UserResponse.model_validate(user)

    def list(self, skip: int = 0, limit: int = 10) -> list[UserResponse]:
        users = self.repository.get_all(skip=skip, limit=limit)
        return [UserResponse.model_validate(u) for u in users]

    # ── private ──────────────────────────────────────────────────────────────

    def _get_or_404(self, user_id: int):
        user = self.repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return user
