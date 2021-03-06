from flask_restful import Resource, Api
from foundation.dataservice import source_impl, configuration_impl
from flask import jsonify


class API_LIST_SOURCE(Resource):
    def get(self):
        lst = source_impl.get_all()
        return jsonify({'sources': lst})

class API_SOURCE(Resource):
    def get(self, source_id):
        s = source_impl.get_by_id(source_id)
        if s is not None:
            return jsonify(dict(
                id=str(s.id),
                created_by=s.created_by,
                created_date=s.created_date,
                is_active=s.is_active,
                mode=s.mode,
                name=s.name,
                project_id=s.project_id,
                project_name=s.project_name,
                status=s.status,
                type_spider=s.type_spider,
                server_ip=s.server_ip
            ))
        else:
            return jsonify({})

class API_SOURCE_BY_SERVER(Resource):
    def get(self, server_ip):
        s = source_impl.get_by_server_ip(server_ip)
        if s is not None:
            return jsonify({'sources': s})
        else:
            return jsonify({'sources': []})

class API_SOURCE_CONFIG(Resource):
    def get(self, key_config, s_id):
        c = configuration_impl.get_config('SOURCE', s_id)
        if key_config.upper() == 'GENERALS':
            return jsonify(dict(
                base_url=c.config['GENERALS']['base_url'],
                max_trying_count=c.config['GENERALS']['max_trying_count'],
                thread_number=c.config['GENERALS']['thread_number'],
                thread_sleep=c.config['GENERALS']['thread_sleep'],
                post_url=c.config['GENERALS']['post_url'],
                thread_number_parsing=c.config['GENERALS']['thread_number_parsing'],
                update_sleep=c.config['GENERALS']['update_sleep'],
                video_base_url = c.config['GENERALS']['video_base_url'],
                chk_unique_css=c.config['GENERALS']['chk_unique_css'],
                filter_pdf=c.config['GENERALS']['filter_pdf'],
                remove_filter_pdf=c.config['GENERALS']['remove_filter_pdf'],
                video_post_url = c.config['GENERALS']['video_post_url']
            ))

        if key_config.upper() == 'PARSERLINKS':
            return jsonify({'configlinks': [v for k,v in c.config['PARSERLINKS']['data'].iteritems()]})

        if key_config.upper() == 'PARSERFIELDS':
            return jsonify({'configfields': [dict(name=k, config=v) for k,v in c.config['PARSERFIELDS']['data'].iteritems()]})

        if key_config.upper() == 'PARSERVIDEOS':
            return jsonify({'configvideos': [dict(name=k, config=v) for k,v in c.config['PARSERVIDEOS']['data'].iteritems()]})