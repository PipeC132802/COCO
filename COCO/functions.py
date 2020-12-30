from Apps.ManageUsers.models import Area


def save_areas(areas, user, obj_param):
    obj_param.objects.filter(user=user).delete()
    for area in areas:
        if len(area):
            try:
                area_in_db = Area.objects.get(area__icontains=area)
            except:
                area_in_db = Area.objects.create(area=area.capitalize())
            try:
                obj_param.objects.get(user=user, area=area_in_db)
            except:
                obj_param.objects.create(user=user, area=area_in_db)