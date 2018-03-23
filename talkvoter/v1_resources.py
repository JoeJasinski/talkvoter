from flask_restful import Resource, Api
from flask import Blueprint
from marshmallow import ValidationError
from webargs.flaskparser import use_args
from .models import db, Talk
from .serializers import VoteSchema, TalkSchema
from .constants import VoteValue


api_bp = Blueprint('api_v1', __name__)
api = Api(api_bp)


class TalksResource(Resource):

    def get(self):
        schema = TalkSchema()
        data = {}
        talk_objs = db.session.query(Talk)
        ret_code = 200
        data = schema.dump(talk_objs, many=True).data
        return data, ret_code


api.add_resource(TalksResource, '/talks/', endpoint="api.talks")


class TalkResource(Resource):

    def get(self, id):
        schema = TalkSchema()
        data = {}
        talk_obj = db.session.query(Talk).filter(Talk.id == id).first()
        if not talk_obj:
            ret_code = 404
            data = {"message": "`talk_id` is not in database"}
        else:
            ret_code = 200
            data = schema.dump(talk_obj).data
        return data, ret_code


api.add_resource(TalkResource, '/talks/<int:id>/', endpoint="api.talk")


class VoteResource(Resource):

    def post(self, id):
        return self.get()

    def get(self, id):
        schema = VoteSchema()
        msg = ""
        try:
            obj = schema.load(
                {'value': VoteValue.in_person.value},
                session=db.session)
        except ValidationError as err:
            err.messages
            valid_data = err.valid_data
            data = str(err)
            ret_code = 400
            msg = "Fail"
        else:
            db.session.add(obj.data)
            db.session.commit()
            data = schema.dump(obj.data)
            msg = "Success"
            ret_code = 200
        return {"message": msg}, ret_code


api.add_resource(VoteResource, '/talks/<int:id>/vote/', endpoint="api.vote")
