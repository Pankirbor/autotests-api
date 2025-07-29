from clients.client_factory import client_factory
from clients.authentication.authentication_schema import AuthenticationUserSchema
from clients.users.users_schema import CreateUserRequestSchema
from tools.fakers import get_random_email
from tools.console_output_formatter import print_dict

create_user_request = CreateUserRequestSchema(
    **{
        "email": get_random_email(),
        "password": "1234",
        "lastName": "Tolstoy",
        "firstName": "Leo",
        "middleName": "none",
    }
)
public_users_client = client_factory.create_public_users_client()

create_user_response = public_users_client.create_user(create_user_request)
print_dict(
    create_user_response.model_dump(),
    title="Пользователь создан",
    message=f"Пользователь: {create_user_response.user.first_name}",
)


private_users_client = client_factory.create_private_users_client(
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
