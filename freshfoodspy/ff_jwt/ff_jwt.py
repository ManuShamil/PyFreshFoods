import jwt

private_key = open('jwt-key').read()
public_key = open('jwt-key.pub').read()

def encode(payload):
    token = jwt.encode(payload, private_key, algorithm='RS256').decode('utf-8')

    return token

def decode(token):
    payload = jwt.decode(token,public_key, algorithms='RS256')
    
    return payload

def verify(token):
    try:
        payload = jwt.decode(token,public_key, algorithms='RS256')

        return True

    except:

        return False