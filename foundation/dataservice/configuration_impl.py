from ..database.configuration import CONFIGURATIONS

def get_config(system_object, system_objectid):
    c = CONFIGURATIONS.objects(system_object = system_object, system_object_id=system_objectid).first()
    return c


def insert(system_object, system_objectid, config):
    c = CONFIGURATIONS(system_object = system_object, system_object_id=system_objectid)
    c.config = config
    return c.save()

def update(system_object, system_objectid, config):
    c = CONFIGURATIONS.objects(system_object = system_object, system_object_id=system_objectid).first()
    c.config = config
    return c.save()

