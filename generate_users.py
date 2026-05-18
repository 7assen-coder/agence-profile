import bcrypt

users = [
    ("client@test.com", "cli123", "client"),
    ("admin@test.com", "adm123", "admin"),
    ("agence@test.com", "age123", "agence")
]

print("\nINSERT INTO utilisateurs (email, password, role) VALUES\n")

for email, password, role in users:

    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode()

    print(f"('{email}', '{hashed}', '{role}'),")