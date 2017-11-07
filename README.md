xivo-auth-client
================

A python library to connect to xivo-auth. HTTPS is used by default. Certificates
are verified by default: if you want to omit the check or use a different CA
bundle, use the verify_certificate argument when instantiating the client.

Usage:

```python
from xivo_auth_client import Client

c = Client('localhost', username='alice', password='alice')

token_data = c.token.new('xivo_user', expiration=3600)  # Creates a new token expiring in 3600 seconds

token_data
{u'expires_at': u'2015-06-04T09:49:30.449625',
 u'issued_at': u'2015-06-04T08:49:30.449607',
 u'token': u'3d95d849-94e5-fc72-4ff8-93b597e6acf6',
 u'auth_id': u'5cdff4a3-24a3-494f-8d32-9c8695e868f9',
 u'xivo_user_uuid': u'5cdff4a3-24a3-494f-8d32-9c8695e868f9',
 u'acls': [u'dird']}

c.token.is_valid(token_data['token'])
True

c.token.get(token_data['token'])
{u'expires_at': u'2015-06-04T09:49:30.449625',
 u'issued_at': u'2015-06-04T08:49:30.449607',
 u'token': u'3d95d849-94e5-fc72-4ff8-93b597e6acf6',
 u'auth_id': u'5cdff4a3-24a3-494f-8d32-9c8695e868f9',
 u'xivo_user_uuid': u'5cdff4a3-24a3-494f-8d32-9c8695e868f9',
 u'acls': [u'dird']}

c.token.get(token_data['token'], required_acls='foobar')  # 403

c.token.is_valid(token_data['token'], required_acl='foobar')
False

c.token.revoke(token_data['token'])

c.token.is_valid(token_data['token'])
False

c.backends.list()
['xivo_user']

# Policies
c.set_token(token_data['token'])

# Create a new policy
c.policies.new(
    'user',
    'The default policy for users',
    ['{% for line in user.lines %}confd.lines.{{ line.id }}.read\n{% endfor %}',
     'dird.me.#'])
{'uuid': '<the policy uuid>'
 'name': 'user',
 'description': 'The default policy for users',
 'acl_templates': ['{% for line in user.lines %}confd.lines.{{ line.id }}.read\n{% endfor %}',
                   'dird.me.#']}

# Get a policy by UUID
c.policies.get('<the policy uuid>')
{'uuid': '<the policy uuid>'
 'name': 'user',
 'description': 'The default policy for users',
 'acl_templates': ['{% for line in user.lines %}confd.lines.{{ line.id }}.read\n{% endfor %}',
                   'dird.me.#']}

# List or search policies
c.policies.list(search='user', order='name', direction='asc', limit=10, offset=0)
{'items': [
    {'uuid': '<the policy uuid>'
     'name': 'user',
     'description': 'The default policy for users',
     'acl_templates': ['{% for line in user.lines %}confd.lines.{{ line.id }}.read\n{% endfor %}',
                       'dird.me.#']},
 ],
 'total': 1}

# Modify a policy
c.policies.edit('<the policy uuid>', 'user', 'A new description', ['#'])
{'uuid': '<the policy uuid>'
 'name': 'user',
 'description': 'A new description',
 'acl_templates': ['#']}

# Add or remove acl templates
c.policies.remove_acl_template('<the policy uuid>', '#')
c.policies.add_acl_template('dird.me.#')
c.policies.add_acl_template('confd.user.{{ user.uuid }}.read')

c.policies.get('<the policy uuid>')
{'uuid': '<the policy uuid>'
 'name': 'user',
 'description': 'A new description',
 'acl_templates': ['dird.me.#', 'confd.user.{{ user.uuid }}.read']}

# delete a policy
c.policies.delete('<the policy uuid>')

# Users

# Creating a user

user = c.users.create(username='alice', email_address='alice@example.com', password='s3cr37')
user
{'uuid': '<user uuid>', 'username': 'alice', 'email_addresses'=[{'address': 'alice@example.com', main=True, confirmed=False}]}

# Adding policies to users

c.users.add_policy(<user_uuid>, <policy_uuid>)

# Removing policies from users

c.users.remove_policy(<user_uuid>, <policy_uuid>)

# Listing users

```python
c.users.list(search='foo', limit=5, offset=10, order='username', direction='asc')
{'total': 42,
 'filtered': 5,  # Number of user matching "foo"
 'items': ...,  # The list of users
}

# Deleting a user

c.users.delete('<user-uuid>')

# Getting a user

c.users.get('<user-uuid>')
{'uuid': '<user uuid>', 'username': 'alice', 'email_addresses'=[{'address': 'alice@example.com', main=True, confirmed=False}]}

# Adding a user to a tenant

c.tenants.add_user('<tenant_uuid>', '<user_uuid>')

# Removing a user from a tenant

c.tenants.remove_user('<tenant_uuid>', '<user_uuid>')

# List users associated to a tenant

c.tenants.get_users('<tenant_uuid>', limit=5, offset=10, order='username', direction='asc')

# List tenants associated to a user

c.users.get_tenants('<user_uuid>', limit=5, offset=10, order='name', direction='asc')

# To use a given certificate file

from xivo_auth_client import Client

c = Client('localhost', username='alice', password='alice', verify_certificate='</path/to/trusted/certificate>')

token_data = c.token.new('xivo_user')
```
