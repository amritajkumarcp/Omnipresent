import json
from app import app, views
# get books data

users = [
    {
       "firstName":"Roy",
       "lastName":"Testerton",
       "dateOfBirth":"19/02/1990",
       "jobTitle":"Software developer",
       "company":"Test co",
       "country":"US"
    },
    {
       "firstName":"Lisa",
       "lastName":"Testora",
       "dateOfBirth":"11/07/1984",
       "jobTitle":"CTO",
       "company":"Test co",
       "country":"GBR"
    },
    {
       "firstName":"Simon",
       "lastName":"McTester",
       "dateOfBirth":"01/11/1987",
       "jobTitle":"Product manager",
       "company":"Mock industries",
       "country":"IND"
    }
]

@app.route("/users")
def get_users():
    """ function to get all users """
    return json.dumps({"users": users})

def test_get_all_users():
    response = views.test_client().get('/users')
    res = json.loads(response.data.decode('utf-8')).get("users")
    assert type(res[0]) is dict
    assert type(res[1]) is dict
    assert type(res[2]) is dict
    assert res[0]['firstName'] == 'Roy'
    assert res[1]['lastName'] == 'Testora'
    assert res[2]['country'] == 'IND'
    assert response.status_code == 201
    assert type(res) is list