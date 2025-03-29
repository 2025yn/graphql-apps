import graphene
from graphene_django import DjangoObjectType
from .models import Teacher, Student

class TeacherType(DjangoObjectType):
    class Meta:
        model = Teacher
        fields = ("id", "name", "students")

class StudentType(DjangoObjectType):
    class Meta:
        model = Student
        fields = ("id", "name", "roll_no", "class_teacher")

class Query(graphene.ObjectType):
    all_teachers = graphene.List(TeacherType)
    all_students = graphene.List(StudentType)
    teacher_by_name = graphene.Field(TeacherType, name=graphene.String(required=True))
    students_by_teacher = graphene.List(StudentType, teacher_name=graphene.String())

    def resolve_all_teachers(root, info):
        return Teacher.objects.all()

    def resolve_all_students(root, info):
        return Student.objects.select_related("class_teacher").all()

    def resolve_teacher_by_name(root, info, name):
        try:
            return Teacher.objects.get(name=name)
        except Teacher.DoesNotExist:
            return None

    def resolve_students_by_teacher(root, info, teacher_name):
        return Student.objects.filter(class_teacher__name=teacher_name)

class CreateTeacher(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    teacher = graphene.Field(TeacherType)

    @classmethod
    def mutate(cls, root, info, name):
        teacher = Teacher(name=name)
        teacher.save()
        return CreateTeacher(teacher=teacher)

class CreateStudent(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        roll_no = graphene.String(required=True)
        teacher_id = graphene.ID(required=True)

    student = graphene.Field(StudentType)

    @classmethod
    def mutate(cls, root, info, name, roll_no, teacher_id):
        student = Student(
            name=name,
            roll_no=roll_no,
            class_teacher_id=teacher_id
        )
        student.save()
        return CreateStudent(student=student)

class Mutation(graphene.ObjectType):
    create_teacher = CreateTeacher.Field()
    create_student = CreateStudent.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)


#  9. 高级功能（可选）
# 如果你想添加更多高级功能，如过滤、分页等，可以修改 schema.py：
#
# python
# 复制
# from graphene_django.filter import DjangoFilterConnectionField
#
# class TeacherNode(DjangoObjectType):
#     class Meta:
#         model = Teacher
#         interfaces = (graphene.relay.Node,)
#         filter_fields = ['name']
#
# class StudentNode(DjangoObjectType):
#     class Meta:
#         model = Student
#         interfaces = (graphene.relay.Node,)
#         filter_fields = {
#             'name': ['exact', 'icontains', 'istartswith'],
#             'roll_no': ['exact'],
#             'class_teacher__name': ['exact'],
#         }
#
# class Query(graphene.ObjectType):
#     teacher = graphene.relay.Node.Field(TeacherNode)
#     all_teachers = DjangoFilterConnectionField(TeacherNode)
#
#     student = graphene.relay.Node.Field(StudentNode)
#     all_students = DjangoFilterConnectionField(StudentNode)