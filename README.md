xivo-auth-client
================

A python library to connect to xivo-auth. HTTPS is used by default. Certificates
are verified by default: if you want to omit the check or use a different CA
bundle, use the verify_certificate argument when instantiating the client.

Usage:

```python
from xivo_auth_client import Client

c = Client('localhost', username='alice', password='alice')

# Tokens
token_data = c.token.new('wazo_user', expiration=3600)  # Creates a new token expiring in 3600 seconds

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

## ACL validation
c.token.get(token_data['token'], required_acls='foobar')  # 403

c.token.is_valid(token_data['token'], required_acl='foobar')
False

## Tenant validation
c.token.get(token_data['token'], tenant='alice-tenant-uuid')
{u'expires_at': u'2015-06-04T09:49:30.449625',
 u'issued_at': u'2015-06-04T08:49:30.449607',
 u'token': u'3d95d849-94e5-fc72-4ff8-93b597e6acf6',
 u'auth_id': u'5cdff4a3-24a3-494f-8d32-9c8695e868f9',
 u'xivo_user_uuid': u'5cdff4a3-24a3-494f-8d32-9c8695e868f9',
 u'acls': [u'dird']}

c.token.is_valid(token_data['token'], tenant='alice-tenant-uuid')
True

## Token revocation
c.token.revoke(token_data['token'])

c.token.is_valid(token_data['token'])
False

c.backends.list()
['wazo_user']

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

# list tenants of a policy
c.policies.get_tenants(<policy_uuid>, search='tenant', order='name', direction='asc', limit=10, offset=0)

# Adding policies to tenants
c.tenants.add_policy(<tenant_uuid>, <policy_uuid>)

# Removing policies from tenants
c.tenants.remove_policy(<tenant_uuid>, <policy_uuid>)

# list policies of a tenant
c.tenants.get_policies(<tenant_uuid>, search='policy', order='name', direction='asc', limit=10, offset=0)


# Users

# Creating a user

user = c.users.new(username='alice', email_address='alice@example.com', password='s3cr37')
user = c.users.new(username='alice', email_address='alice@example.com', password='s3cr37', tenant='my-tenant')

user = c.users.register(username='alice', email_address='alice@example.com', password='s3cr37')
user
{'uuid': '<user uuid>', 'username': 'alice', 'email_addresses'=[{'address': 'alice@example.com', main=True, confirmed=False}]}

# Requesting a new email confirmation email
c.users.request_confirmation_email('<user_uuid>', '<email_uuid>')

# Changing the user's password
c.users.change_password(<user_uuid>, old_password='<old_password>', new_password='<new_password>')

# Reset a user's password
c.users.reset_password(username='<username>')
c.users.reset_password(email='<email>')

c.users.set_password(<user_uuid>, '<new password>', token=<token received by mail>)

# Updating the user's email addresses
emails = [{'address': 'foobar@example.com', 'main': True}]
c.users.update_emails(<user_uuid>, emails)

# or as an administrator
emails = [{'address': 'foobar@example.com', 'main': True, 'confirmed': True}]
c.admin.update_user_emails(<user_uuid>, emails)

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

# Editing a user

c.user.edit('<user-uuid>', firstname='foo', username='bar')
{'uuid': '<user uuid>', 'username': 'foo', 'lastname': None, email_addresses=<email addresses>}


# Groups

# Creating a group
group = c.groups.new(name='<group_name>')

# Getting a group
c.groups.get(group['uuid'])

# Modifying a group
c.groups.edit(group['uuid'], {'name': '<new name>'})

# Listing groups
c.groups.list(search='<searched term>', name='<exact match search on name>', order='name', direction='desc', limit=10, offset=20)

# Deleting a group
c.groups.delete(group['uuid'])

# Adding a user to a group
c.groups.add_user(group['uuid'], <user_uuid>)

# Removing a user from a group
c.groups.remove_user(group['uuid'], <user_uuid>)

# List users in a group
c.groups.get_users(group['uuid'])

# List all groups a user belongs to
c.users.get_groups(<user_uuid>)


# Tenants

# Creating a tenant
c.tenants.new(name='<new tenant name>')

# Updating a tenant
c.tenants.edit('<tenant_uuid>', name='<new tenant name>')

# List users associated to a tenant

c.tenants.get_users('<tenant_uuid>', limit=5, offset=10, order='username', direction='asc')

# List tenants associated to a user

c.users.get_tenants('<user_uuid>', limit=5, offset=10, order='name', direction='asc')

# External authentification storage
c.external.create('<auth_service>', '<user_uuid>', {'key': 'value'})
c.external.update('<auth_service>', '<user_uuid>', {'key': 'value'})
c.external.get('<auth_service>', '<user_uuid>')
c.external.delete('<auth_service>', '<user_uuid>')
c.external.list('<user_uuid>', search='<search term>', limit=5, offset=10, order='type', direction='asc')

# To use a given certificate file

from xivo_auth_client import Client

c = Client('localhost', username='alice', password='alice', verify_certificate='</path/to/trusted/certificate>')

token_data = c.token.new('wazo_user')
```
