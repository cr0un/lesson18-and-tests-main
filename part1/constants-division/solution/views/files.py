from flask_restx import Resource, Namespace

from constants import DOWN_PAYMENT, ANNUAL_RATE

from models import File

file_ns = Namespace('files')


@file_ns.route('/')
class FilesView(Resource):
    def get(self):
        files = File.query.all()
        res = []
        for s in files:
            sm_d = s.__dict__
            del sm_d['_sa_instance_state']
            res.append(sm_d)
        return res, 200

    def post(self):
        return "", 201


@file_ns.route('/<int:fid>')
class FileView(Resource):
    def get(self, fid):
        file = File.query.get_or_404(fid)
        sm_d = file.__dict__
        del sm_d['_sa_instance_state']
        return sm_d, 200
