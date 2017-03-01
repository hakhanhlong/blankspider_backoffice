from ..database.project import PROJECTS


def get_all():
    return PROJECTS.objects().no_cache()

def get_by_id(id):
    p = PROJECTS.objects(id=id).first()
    return p

def insert(name, created_by):
    p = PROJECTS(name, created_by=created_by)
    return p.save()

def update(id, name, source_count):
    p = PROJECTS.objects(id=id).first()
    p.name = name
    p.source_count = source_count
    return p.save()