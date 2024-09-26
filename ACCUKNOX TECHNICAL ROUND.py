# Question 1 : django signals are executed synchronously by default. this means that they are triggered and executed
# within the same request/responce cycle.

# code snippet

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import MyModel

@receiver(post_save, sender=MyModel)
def my_signal_handler(sender, instance, **kwargs):
    print("Signals received !")
# create a new instance of MyModel
my_model_instance = MyModel.objects.create(name="Example")

# the signal handler will be executed immediately after the object is created
print("After object creation")


# Question 2 : Django signals do not run in the same thread as the caller.

import threading
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

def create_profile(sender,instance,created,**kwargs):
    if created:
        print(f"Thread ID in signals:{threading.get_ident()}")
        Profile.objects.create(user=instance)

@receiver(post_save,sender=User)
def receive_signal(sender,instance,created,**kwargs):
    print(f"Thread ID in receiver : {threading.get_ident()}")
    create_profile(sender,instance,created,**kwargs)

#Create a new user
user = User.objects.create(username='test_user')


# Question 3 : django signals do not run in the same database transaction as the caller. This behavior is intentional to prevent
# cascading failures and ensure data integrity.

from django.db import models, transaction
from django.dispatch import Signal

# create a signal
my_signal = Signal()

# create a model 
class MyModel(models.Model):
    name = models.Charfield(max_length=100)

def my_signal_handler(sender,**kwargs):
    try:
        # create a new record in the same transaction as the signal handler
        MyModel.objects.create(name="New record from signals")
    except Exception as e:
        # handle exceptions within the signal handler
        print(f"Error in signal handler : {e}")

# connect the signal handler
my_signal.connect(my_signal_handler)

# start a transaction with 
transaction.atomic()

    # create a record
    MyModel.objects.create(name = "Initial record")

    # send the signal
    my_signal.send(sender = MyModel)

    # try to create another record in the same transaction
    MyModel.objects.create(name = "Another record in the same transaction")


# Topic : Custom classes in python

class Rectangle:
    def __init__(self,length,width):
        self.length = length
        self.width = width
    def __iter__(self):
        yield{'length':self.length}
        yield{'width':self.width}

# create a rectangle object
my_rectangle = Rectangle(7,5)

# iterate over the rectangle
for item in my_rectangle:
    print(item)