from concurrent import futures

import grpc

import course_service_pb2
import course_service_pb2_grpc


courses_db = {}
# current_id = 1


class CourseService(course_service_pb2_grpc.CourseServiceServicer):
    current_id = 1

    @classmethod
    def get_id(cls):
        return cls.current_id

    @classmethod
    def increment_id(cls):
        cls.current_id += 1

    def GetCourse(self, request, context):
        course = courses_db.get(request.course_id)
        if course is None:
            context.abort(grpc.StatusCode.NOT_FOUND, "Course not found")

        return course

    def CreateCourse(self, request, context):
        course = course_service_pb2.CourseResponse(
            course_id=self.get_id(),
            title=request.title,
            description=request.description,
            max_score=request.max_score,
            min_score=request.min_score,
        )
        courses_db[course.course_id] = course
        self.increment_id()

        return course

    def DeleteCourse(self, request, context):
        if request.course_id in courses_db:
            del courses_db[request.course_id]
            return course_service_pb2.DeleteCourseResponse(success=True)

        return course_service_pb2.DeleteCourseResponse(success=False)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    course_service_pb2_grpc.add_CourseServiceServicer_to_server(CourseService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("Сервер запущен на порту 50051")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
