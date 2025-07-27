from clients.client_factory import AuthenticationUserDict, client_factory
from clients.courses.courses_client import CreateCourseRequestDict
from clients.files.files_client import UploadFileRequestDict
from clients.users.public_users_client import CreateUserRequestDict
from tools.console_output_formatter import print_dict
from tools.fakers import get_random_email


create_user_request = CreateUserRequestDict(
    email=get_random_email(),
    password="string",
    lastName="string",
    firstName="string",
    middleName="string",
)

authentication_user = AuthenticationUserDict(
    email=create_user_request["email"], password=create_user_request["password"]
)

create_file_request = UploadFileRequestDict(
    filename="python_course_preview_image.jpg",
    directory="courses",
    upload_file="./testdata/files/image.jpg",
)

puplic_users_client = client_factory.create_public_users_client()
create_user_response = puplic_users_client.create_user(create_user_request)

print_dict(
    create_user_response,
    title="Пользователь создан",
    message=f"Пользователь: {create_user_response['user']['firstName']}",
)

files_client = client_factory.create_files_client(authentication_user)
create_file_response = files_client.upload_file(create_file_request)

print_dict(
    create_file_response,
    title="Файл загружен",
    message=f"Файл: {create_file_response['file']['filename']}",
)

courses_client = client_factory.create_courses_client(authentication_user)
create_course_request = CreateCourseRequestDict(
    title="Python",
    maxScore=100,
    minScore=10,
    description="Python API course",
    estimatedTime="2 weeks",
    previewFileId=create_file_response["file"]["id"],
    createdByUserId=create_user_response["user"]["id"],
)
create_course_response = courses_client.create_course(create_course_request)

print_dict(
    create_course_response,
    title="Курс создан",
    message=f"Курс: {create_course_response['course']['title']}",
)
