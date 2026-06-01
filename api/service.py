from typing import Union, List, Tuple
from .dao import User, Balance

def get_user(email: str = None) -> Union[List[User], User]:
    if email:
        user = User.objects(email=email).first()
        return user
    else:
        users = User.objects()
        return list(users)
    
def get_balance(email: str = None) -> Union[List[Tuple[User,Balance]], Tuple[User, Balance]]:
    if email:
        user = User.objects(email=email).first()
        if not user:
            return None
        balance = Balance.objects(user=user.id).first()
        return user, balance

    users = list(User.objects())
    if not users:
        return []
    user_ids = [user.id for user in users]

    balances = Balance.objects(user__in=user_ids)
    balance_map = {
        balance.user: balance
        for balance in balances
    }

    result = [
        (user, balance_map.get(user.id))
        for user in users
    ]
    return result

def set_balance(email: str, token_credits: float):
    user = User.objects(email=email).first()
    if not user:
        raise ValueError(f"User with email {email} not found")
    balance = Balance.objects(user=user.id).first()
    if not balance:
        raise ValueError(f"Balance for user with email {email} not found")
    balance.token_credits = token_credits
    balance.save()