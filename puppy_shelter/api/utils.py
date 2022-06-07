from api.models import Adopter, Adoption
from rest_framework.exceptions import ValidationError
 
 
def booly(value: str) -> bool:  # ! wyjac to
    v = value.lower()
    if v == 'false': return False
    if v == 'true': return True
    if v == '0': return False
    if v == '1': return True
    raise ValidationError(
        detail={
            "msg": f"Invalid boolean filter value: '{value}', boolean filters must use [0, 1, true, false] u noob"
        }
    )
 
 
def is_employee(user) -> bool:
    return user.groups.filter(name='employees').exists()
 
def is_super_user(user) -> bool:
    return user.is_superuser
 
def is_adopter(user) -> bool:
    return Adopter.objects.filter(user=user).exists()
 
 
def is_adopter_owner(adopter_id: int, user) -> bool:
    return Adopter.objects.filter(user=user, id=adopter_id).exists()
 
 
def has_user_attached(adopter) -> bool:
    return adopter.user is not None
 
 
def is_adopion_owner(adoption_id: int, user) -> bool:
    return Adoption.objects.filter(adopter__user=user, id=adoption_id).exists()
 