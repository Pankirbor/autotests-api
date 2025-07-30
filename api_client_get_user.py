from clients.authentication.authentication_schema import AuthenticationUserSchema
from clients.users.public_users_client import get_public_users_client
from clients.users.private_users_client import get_private_users_client
from clients.users.users_schema import CreateUserRequestSchema
from tools.console_output_formatter import print_dict

create_user_request = CreateUserRequestSchema()
public_users_client = get_public_users_client()

create_user_response = public_users_client.create_user(create_user_request)
print_dict(
    create_user_response.model_dump(),
    title="Пользователь создан",
    message=f"Пользователь: {create_user_response.user.first_name}",
)


private_users_client = get_private_users_client(
    AuthenticationUserSchema(
        email=create_user_request.email, password=create_user_request.password
    )
)
user = private_users_client.get_user(create_user_response.user.id)

print_dict(
    user.model_dump(by_alias=True),
    title="Пользователь получен",
    message=f"Пользователь: {user.user.first_name}",
)
