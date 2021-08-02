from users import users
from flask import Flask
from transactions import transactions
from Account import accounts
from Admin import admin

app = Flask(__name__)

@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,PATCH,DELETE,OPTIONS')
    return response


app.add_url_rule("/user/signin",
                 view_func=users.sign_in, endpoint="SignIn", methods=["GET"])

app.add_url_rule("/user/signup",
                 view_func=users.sign_up, endpoint="SignUp", methods=["POST"])

app.add_url_rule("/user/signout",
                 view_func=users.sign_out, endpoint="SignOut", methods=["GET"])

app.add_url_rule("/user/delete",
                 view_func=users.delete_user, endpoint="DeleteUser", methods=["DELETE"])

app.add_url_rule("/user/profile",
                 view_func=users.update_profile, endpoint="UpdateProfile", methods=["PUT"])

app.add_url_rule("/internalTransact",
                 view_func=transactions.create_internal_transaction, endpoint="CreateInternalTransaction",
                 methods=["POST"])

app.add_url_rule("/externalTransact",
                 view_func=transactions.create_external_transaction, endpoint="CreateExternalTransaction",
                 methods=["POST"])

app.add_url_rule("/createAccount/<userName>",
                 view_func=accounts.createAccount, endpoint="CreateAccount", methods=["POST"])

app.add_url_rule("/getAccount/<userName>",
                 view_func=accounts.getAccount, endpoint="GetAccount", methods=["GET"])

app.add_url_rule("/getTransaction/<userName>/<accountNumber>",
                 view_func=accounts.getTransactions, endpoint="GetTransactions", methods=["GET"])

app.add_url_rule("/deleteAccount/<userName>/<accountNumber>",
                 view_func=accounts.deleteAccount, endpoint="DeleteAccount", methods=["DELETE"])

app.add_url_rule("/recurringTransact",
                 view_func=transactions.create_recurring_transaction, endpoint="CreateRecurringTransaction", methods=["POST"])

app.add_url_rule("/admin/getFeeTransactions",
                 view_func=admin.getFeesTrnsaction, endpoint="getFeesTransaction", methods=["GET"])

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, host="0.0.0.0", port=8000)
