from django.core.management.base import BaseCommand
from school.models import Teacher, Student
import random


class Command(BaseCommand):
    help = 'Seeds the database with sample teachers and students'

    def handle(self, *args, **options):
        self.stdout.write('Seeding data...')

        # 清除现有数据
        Teacher.objects.all().delete()
        Student.objects.all().delete()

        # 创建教师
        teachers = [
            {"name": "Mr. Smith"},
            {"name": "Ms. Johnson"},
            {"name": "Dr. Williams"},
            {"name": "Mrs. Brown"},
            {"name": "Prof. Davis"}
        ]

        created_teachers = []
        for teacher_data in teachers:
            teacher = Teacher.objects.create(**teacher_data)
            created_teachers.append(teacher)
            self.stdout.write(f'Created teacher: {teacher.name}')

        # 创建学生
        first_names = ["Emma", "Liam", "Olivia", "Noah", "Ava", "William",
                       "Sophia", "James", "Isabella", "Benjamin", "Mia", "Lucas"]
        last_names = ["Johnson", "Smith", "Williams", "Brown", "Jones",
                      "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]

        for i in range(1, 31):  # 创建30个学生
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            student = Student.objects.create(
                name=f"{first_name} {last_name}",
                roll_no=f"STU{i:03d}",
                class_teacher=random.choice(created_teachers)
            )
            self.stdout.write(
                f'Created student: {student.name} (Roll No: {student.roll_no}) with teacher {student.class_teacher.name}')

        self.stdout.write(self.style.SUCCESS('Successfully seeded database!'))