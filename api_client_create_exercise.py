from clients.authentication.authentication_schema import AuthenticationUserSchema
from clients.exercises.exercises_client import get_exercises_client
from clients.exercises.exercises_schema import CreateExerciseRequestSchema
from clients.courses.courses_client import get_courses_client
from clients.courses.courses_schema import CreateCourseRequestSchema
from clients.files.files_client import get_files_client
from clients.files.files_schema import UploadFileRequestSchema
from clients.users.public_users_client import get_public_users_client
from clients.users.users_schema import CreateUserRequestSchema
from tools.console_output_formatter import print_dict
from tools.fakers import get_random_email

user_data = {
    "email": get_random_email(),
    "password": "1234",
    "lastName": "Tolstoy",
    "firstName": "Leo",
    "middleName": "none",
}
create_user_request = CreateUserRequestSchema(**user_data)

upload_file_request = UploadFileRequestSchema(
    **{
        "filename": "image.jpg",
        "directory": "/course",
        "upload_file": "./testdata/files/image.jpg",
    }
)

public_users_client = get_public_users_client()
created_user = public_users_client.create_user(create_user_request)

print_dict(
    created_user.model_dump(),
    title="Пользователь создан",
    message=f"Пользователь: {created_user.user.first_name}",
)

login_data = AuthenticationUserSchema(
    email=create_user_request.email, password=create_user_request.password
)

file_client = get_files_client(login_data)
created_file = file_client.upload_file(upload_file_request)

print_dict(
    created_file.model_dump(),
    title="Файл загружен",
    message=f"Файл: {created_file.file.filename}",
)


create_course_request = CreateCourseRequestSchema(
    **{
        "title": "Основы Python",
        "maxScore": 100,
        "minScore": 50,
        "description": "Курс по основам программирования на Python для начинающих.",
        "estimatedTime": "10 часов",
        "previewFileId": created_file.file.id,
        "createdByUserId": created_user.user.id,
    }
)

courses_client = get_courses_client(login_data)
created_course = courses_client.create_course(create_course_request)

print_dict(
    created_course.model_dump(),
    title="Курс создан",
    message=f"Курс: {created_course.course.title}",
)


create_exercises_request = CreateExerciseRequestSchema(
    **{
        "title": "Упражнение 1: Синтаксис Python",
        "courseId": created_course.course.id,
        "maxScore": 10,
        "minScore": 5,
        "orderIndex": 1,
        "description": "Напишите первую программу на Python.",
        "estimatedTime": "30 минут",
    }
)

exercises_client = get_exercises_client(login_data)
created_exercise = exercises_client.create_exercise(create_exercises_request)

print_dict(
    created_exercise.model_dump(),
    title="Упражнение создано",
    message=f"{created_exercise.exercise.title}",
)
