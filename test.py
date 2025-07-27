import auth

print(auth.list_users())  # باید ['admin'] باشه ابتدا

success, msg = auth.register_user("user1", "pass1")
print(success, msg)

success, role = auth.authenticate("user1", "pass1")
print("Authenticated:", success, "Role:", role)
