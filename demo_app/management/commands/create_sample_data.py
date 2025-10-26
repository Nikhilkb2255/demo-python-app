from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from demo_app.models import Category, Product, BlogPost
import random


class Command(BaseCommand):
    help = 'Create sample data for testing the Django demo app'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help='Number of products to create (default: 10)',
        )

    def handle(self, *args, **options):
        count = options['count']
        
        self.stdout.write('Creating sample data...')
        
        # Create categories
        categories_data = [
            {'name': 'Electronics', 'description': 'Electronic devices and gadgets'},
            {'name': 'Clothing', 'description': 'Fashion and apparel'},
            {'name': 'Books', 'description': 'Books and educational materials'},
            {'name': 'Home & Garden', 'description': 'Home improvement and gardening supplies'},
            {'name': 'Sports', 'description': 'Sports equipment and accessories'},
        ]
        
        categories = []
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            categories.append(category)
            if created:
                self.stdout.write(f'Created category: {category.name}')
        
        # Create products
        products_data = [
            {'name': 'Smartphone', 'description': 'Latest generation smartphone with advanced features', 'price': 599.99, 'category': 'Electronics'},
            {'name': 'Laptop', 'description': 'High-performance laptop for work and gaming', 'price': 1299.99, 'category': 'Electronics'},
            {'name': 'Wireless Headphones', 'description': 'Noise-cancelling wireless headphones', 'price': 199.99, 'category': 'Electronics'},
            {'name': 'T-Shirt', 'description': 'Comfortable cotton t-shirt', 'price': 19.99, 'category': 'Clothing'},
            {'name': 'Jeans', 'description': 'Classic denim jeans', 'price': 49.99, 'category': 'Clothing'},
            {'name': 'Sneakers', 'description': 'Comfortable running sneakers', 'price': 79.99, 'category': 'Clothing'},
            {'name': 'Python Programming Book', 'description': 'Complete guide to Python programming', 'price': 39.99, 'category': 'Books'},
            {'name': 'Django Web Development', 'description': 'Learn Django framework for web development', 'price': 44.99, 'category': 'Books'},
            {'name': 'Garden Tools Set', 'description': 'Complete set of gardening tools', 'price': 89.99, 'category': 'Home & Garden'},
            {'name': 'Yoga Mat', 'description': 'Non-slip yoga mat for exercise', 'price': 29.99, 'category': 'Sports'},
        ]
        
        created_products = []
        for i in range(count):
            product_data = random.choice(products_data)
            category = next(cat for cat in categories if cat.name == product_data['category'])
            
            product = Product.objects.create(
                name=f"{product_data['name']} #{i+1}",
                description=product_data['description'],
                price=product_data['price'],
                category=category,
                stock_quantity=random.randint(0, 100),
                is_active=random.choice([True, True, True, False])  # Mostly active
            )
            created_products.append(product)
        
        self.stdout.write(f'Created {len(created_products)} products')
        
        # Create a superuser if it doesn't exist
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123'
            )
            self.stdout.write('Created superuser: admin/admin123')
        
        # Create blog posts
        blog_posts_data = [
            {
                'title': 'Getting Started with Django',
                'content': 'Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. Built by experienced developers, it takes care of much of the hassle of web development, so you can focus on writing your app without needing to reinvent the wheel.',
                'category': 'Books'
            },
            {
                'title': 'Building REST APIs with Django',
                'content': 'Django makes it easy to build REST APIs. You can create API endpoints using function-based views or class-based views. This demo app shows both approaches.',
                'category': 'Books'
            },
            {
                'title': 'Modern Web Development Practices',
                'content': 'Modern web development involves using contemporary tools, frameworks, and practices to build scalable, maintainable applications.',
                'category': 'Books'
            },
        ]
        
        admin_user = User.objects.get(username='admin')
        for post_data in blog_posts_data:
            category = next(cat for cat in categories if cat.name == post_data['category'])
            BlogPost.objects.create(
                title=post_data['title'],
                content=post_data['content'],
                author=admin_user,
                category=category,
                is_published=True
            )
        
        self.stdout.write('Created blog posts')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created sample data!\n'
                f'- Categories: {len(categories)}\n'
                f'- Products: {len(created_products)}\n'
                f'- Blog posts: {len(blog_posts_data)}\n'
                f'- Superuser: admin/admin123'
            )
        )
