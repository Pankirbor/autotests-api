from clients.authentication.authentication_schema import AuthenticationUserSchema
from clients.courses.courses_client import get_courses_client
from clients.courses.courses_schema import CreateCourseRequestSchema
from clients.files.files_client import get_files_client
from clients.files.files_schema import UploadFileRequestSchema
from clients.users.public_users_client import get_public_users_client
from clients.users.users_schema import CreateUserRequestSchema
from tools.console_output_formatter import print_dict


create_user_request = CreateUserRequestSchema()

authentication_user = AuthenticationUserSchema(
    email=create_user_request.email, password=create_user_request.password
)

create_file_request = UploadFileRequestSchema(
    upload_file="./testdata/files/image.jpg",
)

puplic_users_client = get_public_users_client()
create_user_response = puplic_users_client.create_user(create_user_request)

print_dict(
    create_user_response.model_dump(by_alias=True),
    title="Пользователь создан",
    message=f"Пользователь: {create_user_response.user.first_name}",
)

files_client = get_files_client(authentication_user)
create_file_response = files_client.upload_file(create_file_request)

print_dict(
    create_file_response.model_dump(by_alias=True),
    title="Файл загружен",
    message=f"Файл: {create_file_response.file.filename}",
)

courses_client = get_courses_client(authentication_user)
create_course_request = CreateCourseRequestSchema(
    preview_file_id=create_file_response.file.id,
    created_by_user_id=create_user_response.user.id,
)
create_course_response = courses_client.create_course(create_course_request)

print_dict(
    create_course_response.model_dump(by_alias=True),
    title="Курс создан",
    message=f"Курс: {create_course_response.course.title}",
)
