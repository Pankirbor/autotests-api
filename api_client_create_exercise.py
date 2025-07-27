from clients.client_factory import client_factory, AuthenticationUserDict
from clients.courses.courses_client import CreateCourseRequestDict
from clients.exercises.exercises_client import CreateExerciseRequestDict
from clients.files.files_client import UploadFileRequestDict
from clients.users.public_users_client import CreateUserRequestDict
from tools.console_output_formatter import print_dict
from tools.fakers import get_random_email


user_data = {
    "email": get_random_email(),
    "password": "1234",
    "lastName": "Tolstoy",
    "firstName": "Leo",
    "middleName": "none",
}
course_data = {
    "title": "Основы Python",
    "maxScore": 100,
    "minScore": 50,
    "description": "Курс по основам программирования на Python для начинающих.",
    "estimatedTime": "10 часов",
    "previewFileId": "",
    "createdByUserId": "",
}

file_data = {
    "filename": "image.jpg",
    "directory": "/course",
    "upload_file": "./testdata/files/image.jpg",
}

exercises_data = {
    "title": "Упражнение 1: Синтаксис Python",
    "courseId": "",
    "maxScore": 10,
    "minScore": 5,
    "orderIndex": 1,
    "description": "Напишите первую программу на Python.",
    "estimatedTime": "30 минут",
}

public_users_client = client_factory.create_public_users_client()
created_user = public_users_client.create_user(CreateUserRequestDict(**user_data))

print_dict(
    created_user,
    title="Пользователь создан",
    message=f"Пользователь: {created_user['user']['firstName']}",
)

login_data = AuthenticationUserDict(
    email=user_data["email"], password=user_data["password"]
)

file_client = client_factory.create_files_client(login_data)
created_file = file_client.upload_file(UploadFileRequestDict(**file_data))

print_dict(
    created_file,
    title="Файл загружен",
    message=f"Файл: {created_file['file']['filename']}",
)

courses_client = client_factory.create_courses_client(login_data)
course_data["previewFileId"] = created_file["file"]["id"]
course_data["createdByUserId"] = created_user["user"]["id"]
created_course = courses_client.create_course(CreateCourseRequestDict(**course_data))

print_dict(
    created_course,
    title="Курс создан",
    message=f"Курс: {created_course['course']['title']}",
)

exercises_client = client_factory.create_exercises_client(login_data)
exercises_data["courseId"] = created_course["course"]["id"]
created_exercise = exercises_client.create_exercise(
    CreateExerciseRequestDict(**exercises_data)
)

print_dict(
    created_exercise,
    title="Упражнение создано",
    message=f"{created_exercise['exercise']['title']}",
)
