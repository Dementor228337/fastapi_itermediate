from datetime import timedelta
from strawberry.file_uploads import Upload
import strawberry
from strawberry.types import Info
from src.api.graphql.decorators import require_authentication, paginate
from src.api.graphql.user.schemas import User, Token, UserPage
from src.core.user.services import UserService, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES


@strawberry.type
class UserMutation:

    @strawberry.mutation
    def register(self, username: str, password: str, email: str) -> User:
        UserService.add(username=username, password=password, email=email, is_admin=False, permissions=[])
        return User(username=username, email=email)

    @strawberry.mutation
    def login(self, username: str, password: str) -> Token:
        user = UserService.authenticate_user(username, password)
        if not user:
            raise ValueError("Incorrect username or password")
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

        access_token = UserService.create_token(data={"sub": username, "type": "access"},
                                                expires_delta=access_token_expires)
        refresh_token = UserService.create_token(data={"sub": username, "type": "refresh"},
                                                 expires_delta=refresh_token_expires)

        return Token(access_token=access_token, refresh_token=refresh_token)

@strawberry.type
class FileMutation:

    @strawberry.mutation
    async def upload_file(self, file: Upload) -> str:
        content = await file.read()
        filename = file.filename
        with open(f"media/uploaded_{filename}", "wb") as f:
            f.write(content)
        return f"File {filename} was uploaded succ"

@strawberry.type
class UserQuery:

    @strawberry.field
    @require_authentication
    @paginate
    def all_users(self, info: Info, limit: int, offset: int) -> UserPage:
        return UserService.get_all()