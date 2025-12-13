from os import environ 
from os.path import join 
from django.conf import settings 
from django import setup 
from pathlib import Path 
from django.utils.text import slugify
import sys 
from random import choice 

print("Sistema de criação de objetos falsos (Não otimizado)") 
DJANGO_BASE_DIR = Path(__name__).parent.parent 
DJANGO_SETTINGS_MODULE = 'configs.settings' 
NUMBER_OF_OBJECTS = int(input("Quantidade de produtos falsos a serem criados: ")) 
EVALUATION_NUMBER_PER_PRODUCT = 5
DOUBT_NUMBER_PER_PRODUCT = 10
DELETE = bool(input("Deletar models existentes ? ")) 

sys.path.append(str(DJANGO_BASE_DIR)) 
environ['DJANGO_SETTINGS_MODULE'] = DJANGO_SETTINGS_MODULE 
settings.USE_TZ = False 
setup() 

if __name__ == '__main__': 
    from faker import Faker 
    from faker_commerce import Provider 
    from product.models import Product , Category , Doubt , Evaluation 
    from workplace.models import Shop
    from django.contrib.auth import get_user_model 
    
    USER = get_user_model()
    
    fake = Faker("pt_BR") 
    fake.add_provider(Provider) 
    default_user = USER.objects.get(pk = 1) 
    default_shop = default_user.shop
    models = [Product , Category , Doubt , Evaluation ] 
    django_categories = [] 
    if DELETE: 
        for model in models: 
            model.objects.all().delete() 
            
        categories = ['Luxo' , 'Economico' , 'Gamer' , 'Upgrade' , 'Casa' , 'Eletronicos' , 'Celulares' , 'Computadores' , 'Perifericos'] 
        django_categories = [Category(name = category_name , slug = slugify(category_name)) for category_name in categories ]
        Category.objects.bulk_create(django_categories)
            
    django_categories = list(Category.objects.all())  
    
                  
    django_products = []             
    for _ in range(NUMBER_OF_OBJECTS): 
        product = Product.objects.create( 
                        name = fake.ecommerce_name(), 
                        description = fake.text(max_nb_chars=100), 
                        price = fake.pydecimal( left_digits=4, right_digits=2, positive=True ), 
                        shop = default_shop,
                        created_by = default_user ,
                    ) 
        category = choice(django_categories) 
        product.categorys.set([category]) 
        django_products.append(product) 
        
    print("Produtos criados")
    
    django_evaluations = []
    for product in django_products:
        for _ in range(EVALUATION_NUMBER_PER_PRODUCT):
            evaluation = Evaluation(
                product = product,
                user = default_user,
                rating = fake.random_int(min=1 , max=5),
                comment = fake.text(max_nb_chars=200)
            )
            django_evaluations.append(evaluation)
    Evaluation.objects.bulk_create(django_evaluations)
    print("Avaliações criadas")
    
    django_doubts = []
    for product in django_products:
        for _ in range(DOUBT_NUMBER_PER_PRODUCT):
            doubt = Doubt(
                product = product,
                user = default_user,
                title = fake.text(max_nb_chars=100),
                content = fake.text(max_nb_chars=200)
            )
            django_doubts.append(doubt)
            
    Doubt.objects.bulk_create(django_doubts)
    print("Duvidas criadas")