from ma import ma
from models.user import UserModel


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        load_only = ('password',)
        dump_only = ('id',)
        load_instance = True

    # the fields were deleted and we use fields from the usermodel instead
