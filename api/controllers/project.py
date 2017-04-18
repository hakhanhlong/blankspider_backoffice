from flask_restful import Resource, Api, reqparse, abort
from foundation.dataservice import project_impl, source_impl
from flask import jsonify





class API_LIST_PROJECT(Resource):
    def get(self):
        lst = project_impl.get_all()
        return jsonify({'projects': [dict(id=str(p.id),
                                          name=p.name,
                                          created_by=p.created_by,
                                          source_count=p.source_count,
                                          sources=[dict(
                                            id=str(s.id),
                                            created_by=s.created_by,
                                            created_date=s.created_date,
                                            is_active=s.is_active,
                                            mode=s.mode,
                                            name=s.name,
                                            project_id=s.project_id,
                                            project_name=s.project_name,
                                            status=s.status,
                                            type_spider=s.type_spider
                                            ) for s in source_impl.get_by_projectid(p.id)]) for p in lst]})

class API_LIST_PROJECT_WITH_SERVERIP(Resource):
    def get(self, server_ip):
        lst = project_impl.get_all()
        return jsonify({'projects': [dict(id=str(p.id),
                                          name=p.name,
                                          created_by=p.created_by,
                                          source_count=p.source_count,
                                          sources=[dict(
                                            id=str(s.id),
                                            created_by=s.created_by,
                                            created_date=s.created_date,
                                            is_active=s.is_active,
                                            mode=s.mode,
                                            name=s.name,
                                            project_id=s.project_id,
                                            project_name=s.project_name,
                                            status=s.status,
                                            type_spider=s.type_spider
                                            ) for s in source_impl.get_by_projectid_and_serverip(p.id, server_ip)]) for p in lst]})

class API_PROJECT(Resource):
    def get(self, project_id):
        pro = project_impl.get_by_id(project_id)
        return jsonify({'projects': pro})


