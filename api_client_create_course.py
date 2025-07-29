from clients.authentication.authentication_schema import AuthenticationUserSchema
from clients.courses.courses_client import get_courses_client
from clients.courses.courses_schema import CreateCourseRequestSchema
from clients.files.files_client import get_files_client
from clients.files.files_schema import UploadFileRequestSchema
from clients.users.public_users_client import get_public_users_client
from clients.users.users_schema import CreateUserRequestSchema
from tools.console_output_formatter import print_dict
from tools.fakers import get_random_email


create_user_request = CreateUserRequestSchema(
    email=get_random_email(),
    password="string",
    lastName="string",
    firstName="string",
    middleName="string",
)

authentication_user = AuthenticationUserSchema(
    email=create_user_request.email, password=create_user_request.password
)

create_file_request = UploadFileRequestSchema(
    filename="python_course_preview_image.jpg",
    directory="courses",
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
    **{
        "title": "Основы Python",
        "maxScore": 100,
        "minScore": 50,
        "description": "Курс по основам программирования на Python для начинающих.",
        "estimatedTime": "10 часов",
        "previewFileId": create_file_response.file.id,
        "createdByUserId": create_user_response.user.id,
    }
)
create_course_response = courses_client.create_course(create_course_request)

print_dict(
    create_course_response.model_dump(by_alias=True),
    title="Курс создан",
    message=f"Курс: {create_course_response.course.title}",
)
