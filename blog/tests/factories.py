import factory
from factory import SubFactory, Faker
from django.contrib.auth.models import User
from blog.models import Post, Category
import pytz

# Factory class for User
class UserFactory(factory.django.DjangoModelFactory):
    email = Faker("email")
    username = factory.Sequence(lambda n: f"user{n}")
    first_name = Faker("first_name")
    last_name = Faker("last_name")
    password = factory.PostGenerationMethodCall("set_password", "password")
    is_active = True

    class Meta:
        model = User

# Factory class for Superuser
class SuperUserFactory(UserFactory):
    is_superuser = True
    is_staff = True

# Factory class for Category
class CategoryFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f"Category {n}")

    class Meta:
        model = Category

# Factory class for Posts
class PostFactory(factory.django.DjangoModelFactory):
    title = factory.Sequence(lambda n: f"Post {n}")
    author = SubFactory(UserFactory)
    content = Faker("paragraph")

    # Generate datetime with timezone
    created_at = Faker("date_time_between", start_date="-30d", end_date="now", tzinfo=pytz.timezone("Europe/Paris"))
    updated_at = Faker("date_time_between", start_date="-30d", end_date="now", tzinfo=pytz.timezone("Europe/Paris"))

    posted = True
    
    class Meta:
        model = Post

    @factory.post_generation
    def categories(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for category in extracted:
                self.categories.add(category)
        else:
            self.categories.add(CategoryFactory())
