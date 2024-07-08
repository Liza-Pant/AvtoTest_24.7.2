from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Барбоскин', animal_type='двортерьер',
                                     age='4', pet_photo='images/dog.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name


def test_unsuccessful_add_new_pet_with_negative_age(name='Негативный', animal_type='пес',
                                                    age='-1', pet_photo='images/dog.jpg'):
    """Проверяем что нельзя добавить питомца с отрицательным возрастом"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['age'] >= 0


def test_unsuccessful_add_new_pet_with_empty_data(name='Мышка', animal_type='норушка',
                                                  age='1', pet_photo=''):
    """Проверяем что нельзя добавить питомца с пустыми данными"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    ##     if name == '' or animal_type == '' or age == '' or pet_photo == '':
    #         raise Exception("Нельзя добавить питомца без данных")
    try:
        pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    except FileNotFoundError:
        print('Нельзя добавить питомца без фото')


def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age='5'):
    """Проверяем возможность обновления информации о питомце"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")


def test_successful_add_photo_for_pet(pet_photo='images/cat.jpg'):
    """Проверяем возможность добавления фото питомцу"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    if len(my_pets['pets']) > 0 and my_pets['pets'][0]['pet_photo'] == '':
        status, result = pf.add_photo_for_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
        assert status == 200
        assert result['pet_photo'] != ''
    else:
        raise Exception("У питомца уже есть фото")


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", '3', "images/photo.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()
