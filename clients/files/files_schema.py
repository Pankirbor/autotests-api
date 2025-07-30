from pydantic import BaseModel, Field, HttpUrl

from tools.fakers import fake


class FileSchema(BaseModel):
    """
    Описание структуры файла.
    """

    id: str
    url: HttpUrl
    filename: str
    directory: str


class UploadFileRequestSchema(BaseModel):
    """Класс, определяющий структуру данных для запроса загрузки файла.

    Содержит обязательные параметры, необходимые для передачи файла на сервер.
    """

    filename: str = Field(default_factory=lambda: f"{fake.uuid4()}.jpg")
    directory: str = Field(default="tests")
    upload_file: str


class UploadFileResponseSchema(BaseModel):
    """
    Описание структуры ответа создания файла.
    """

    file: FileSchema
