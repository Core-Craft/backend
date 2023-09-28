from app.models.user import User as UserModel

class UserSerializer:
    @classmethod
    def from_request(cls, user_data: UserModel) -> dict:
        return UserModel(**user_data) 

    @classmethod
    def to_response(cls, user_data: dict) -> UserModel:
        return {
            "id": user_data.get("id", ""),
            "email": user_data.get("email", "")
        }
        
    # @root_validator
    # def check_aadhar(cls, values):
