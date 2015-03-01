from django.core import validators
from django.db.models import Field
from django.utils.translation import ugettext_lazy as _

class ByteField(Field):
	description = _("Vector of bytes (up to %(max_length)s)")

	def __init__(self, *args, **kwargs):
		super(ByteField, self).__init__(*args, **kwargs)
		self.validators.append(validators.MaxLengthValidator(self.max_length))

	def db_type(self, connection):
		if connection.settings_dict['ENGINE'] == 'django.db.backends.mysql':
			return 'varbinary(' + str(self.max_length) + ')'
		else:
			raise Exception('Only MySQL is currently suppported!')
