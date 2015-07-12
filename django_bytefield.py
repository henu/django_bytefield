from django.core import validators
from django.core.exceptions import ValidationError
from django.db.models import Field, SubfieldBase
from django.utils.translation import ugettext_lazy as _

import binascii


def validate_hex(value):
    if value is None:
        return
    if not isinstance(value, basestring):
        raise ValidationError(_('Not a string!'))
    for c in value:
        if c not in '01234567890abcdefABCDEF':
            raise ValidationError(_('"%s" is not a hex string!') % value)


class ByteField(Field):
    description = _('Vector of bytes (up to %(max_length)s)')

    __metaclass__ = SubfieldBase

    def __init__(self, *args, **kwargs):
        super(ByteField, self).__init__(*args, **kwargs)
        self.validators.append(validators.MaxLengthValidator(self.max_length * 2))
        self.validators.append(validate_hex)

    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return None
        return binascii.hexlify(value)

    def get_prep_value(self, value):
        if value is None:
            return None
        return binascii.unhexlify(value)

    def db_type(self, connection):
        if connection.settings_dict['ENGINE'] == 'django.db.backends.mysql':
            return 'varbinary(' + str(self.max_length) + ')'
        else:
            raise Exception('Only MySQL is currently suppported!')
