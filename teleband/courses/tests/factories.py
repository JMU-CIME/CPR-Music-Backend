import datetime

from factory import Faker, SubFactory, LazyFunction
from factory.django import DjangoModelFactory

from teleband.courses.models import Enrollment, Course
from teleband.instruments.tests.factories import InstrumentFactory
from teleband.users.tests.factories import UserFactory, RoleFactory


class CourseFactory(DjangoModelFactory):

    name = Faker("color")
    owner = SubFactory(UserFactory)
    start_date = LazyFunction(datetime.datetime.utcnow)
    end_date = LazyFunction(datetime.datetime.utcnow)

    class Meta:
        model = Course


class EnrollmentFactory(DjangoModelFactory):

    user = SubFactory(UserFactory)
    course = SubFactory(CourseFactory)
    instrument = SubFactory(InstrumentFactory)
    role = SubFactory(RoleFactory)

    class Meta:
        model = Enrollment
