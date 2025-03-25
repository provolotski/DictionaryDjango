class BelstatUser:
    def __init__(self, username, guid,LDAP_Name,  **kwargs):
        self.username = username
        self.guid = guid
        self.LDAP_Name = LDAP_Name
        self.is_active = True
        self.is_authenticated = True
        # Дополнительные поля
        # for key, value in kwargs.items():
        #     setattr(self, key, value)

    def __str__(self):
        return self.username