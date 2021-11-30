import jwt
import datetime


def create_jwt(project_id, private_key_file, algorithm, jwt_expires_minutes):
    token = {
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=jwt_expires_minutes),
        "aud": project_id,
    }

    with open(private_key_file, "r") as f:
        private_key = f.read()

    print(
        "Creating JWT using {} from private key file {}".format(
            algorithm, private_key_file
        )
    )
    return jwt.encode(token, private_key, algorithm=algorithm)