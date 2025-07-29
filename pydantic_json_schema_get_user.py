from clients.authentication.authentication_schema import AuthenticationUserSchema
from clients.users.public_users_client import get_public_users_client
from clients.users.private_users_client import get_private_users_client
from clients.users.users_schema import GetUserResponseSchema, CreateUserRequestSchema
from tools.assertions.schema import validate_json_schema
from tools.fakers import get_random_email

public_users_client = get_public_users_client()

create_user_request = CreateUserRequestSchema(
    email=get_random_email(),
    password="string",
    last_name="string",
    first_name="string",
    middle_name="string",
)

create_user_reponse = public_users_client.create_user(create_user_request)
new_user = create_user_reponse.user

private_users_client = get_private_users_client(
    AuthenticationUserSchema(
        email=create_user_request.email, password=create_user_request.password
    )
)

schema = GetUserResponseSchema.model_json_schema()
get_users_response = private_users_client.get_user_api(new_user.id)

validate_json_schema(get_users_response.json(), schema)
