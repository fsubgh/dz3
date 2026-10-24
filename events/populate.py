
from django.contrib.auth.models import User
from events.models import Category, Event


# Создаём категории
category1, _ = Category.objects.get_or_create(
    name='Концерты',
    defaults={'description': 'Музыкальные мероприятия'}
)

category2, _ = Category.objects.get_or_create(
    name='Спорт',
    defaults={'description': 'Спортивные мероприятия'}
)

category3, _ = Category.objects.get_or_create(
    name='Образование',
    defaults={'description': 'Обучающие мероприятия'}
)


# Создаём пользователей
users = []

for i in range(1, 6):
    username = f'user{i}'

    user, created = User.objects.get_or_create(
        username=username,
        defaults={
            'email': f'user{i}@example.com',
        }
    )

    users.append(user)


# Создаём мероприятия
events_data = [
    {
        'title': 'Музыкальный вечер',
        'description': 'Вечер живой музыки',
        'price': 500,
        'max_participants': 50,
        'is_active': True,
        'categories': [category1],
        'participants': [users[0], users[1]],
    },
    {
        'title': 'Футбольный турнир',
        'description': 'Турнир среди любительских команд',
        'price': 300,
        'max_participants': 100,
        'is_active': True,
        'categories': [category2],
        'participants': [users[0], users[1], users[2]],
    },
    {
        'title': 'Python для начинающих',
        'description': 'Основы программирования на Python',
        'price': 0,
        'max_participants': 30,
        'is_active': True,
        'categories': [category3],
        'participants': [users[0], users[1], users[2], users[3]],
    },
    {
        'title': 'Рок-концерт',
        'description': 'Концерт местных рок-групп',
        'price': 1000,
        'max_participants': 200,
        'is_active': True,
        'categories': [category1, category2],
        'participants': [users[0], users[1], users[2], users[3], users[4]],
    },
    {
        'title': 'Мастер-класс по Django',
        'description': 'Создание веб-приложений',
        'price': 700,
        'max_participants': 40,
        'is_active': True,
        'categories': [category3, category1],
        'participants': [users[1], users[2]],
    },
    {
        'title': 'Забег выходного дня',
        'description': 'Любительский забег в парке',
        'price': 200,
        'max_participants': 80,
        'is_active': True,
        'categories': [category2],
        'participants': [users[0], users[3], users[4]],
    },
    {
        'title': 'Семинар по дизайну',
        'description': 'Основы современного дизайна',
        'price': 400,
        'max_participants': 35,
        'is_active': False,
        'categories': [category3],
        'participants': [users[1], users[4]],
    },
    {
        'title': 'Закрытая выставка',
        'description': 'Выставка современных художников',
        'price': 600,
        'max_participants': 60,
        'is_active': False,
        'categories': [category1],
        'participants': [users[0], users[2]],
    },
]


# Добавляем мероприятия и связанные данные
for data in events_data:
    event, created = Event.objects.get_or_create(
        title=data['title'],
        defaults={
            'description': data['description'],
            'author': users[0],
            'price': data['price'],
            'max_participants': data['max_participants'],
            'is_active': data['is_active'],
        }
    )

    event.categories.set(data['categories'])
    event.participants.set(data['participants'])

print('Тестовые данные успешно добавлены!')
print('Категорий:', Category.objects.count())
print('Пользователей:', User.objects.count())
print('Мероприятий:', Event.objects.count())
