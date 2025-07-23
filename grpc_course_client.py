import grpc
import course_service_pb2
import course_service_pb2_grpc


def run():
    channel = grpc.insecure_channel("localhost:50051")
    stub = course_service_pb2_grpc.CourseServiceStub(channel=channel)

    try:
        create_response = stub.CreateCourse(
            course_service_pb2.CreateCourseRequest(
                title="Автотесты API",
                description="Будем изучать написание API автотестов",
                max_score=40,
                min_score=5,
            )
        )
        print(f"Создан курс: {create_response}")

        get_response = stub.GetCourse(course_service_pb2.GetCourseRequest(course_id=1))
        print(f"Получен курс: {get_response}")

        delete_response = stub.DeleteCourse(
            course_service_pb2.DeleteCourseRequest(course_id=1)
        )
        print(f"Удаление курса course_id=1: {delete_response.success}")

    except grpc.RpcError as e:
        print(f"Ошибка gRPC: {e.code()}: {e.details()}")


if __name__ == "__main__":
    run()
