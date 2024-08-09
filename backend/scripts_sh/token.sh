#!/bin/bash
echo "Create token..."
python manage.py shell -c "\
from rest_framework.authtoken.models import Token; \
from users.models import User; \
Token.objects.get_or_create(user=User.objects.get(id='1')); \
Token.objects.get_or_create(user=User.objects.get(id='2')); \
Token.objects.get_or_create(user=User.objects.get(id='3')); \
Token.objects.get_or_create(user=User.objects.get(id='4')); \
Token.objects.get_or_create(user=User.objects.get(id='5')); \
Token.objects.get_or_create(user=User.objects.get(id='6')); \
Token.objects.get_or_create(user=User.objects.get(id='7')); \
Token.objects.get_or_create(user=User.objects.get(id='8')); \
Token.objects.get_or_create(user=User.objects.get(id='9')); \
Token.objects.get_or_create(user=User.objects.get(id='10')); \
Token.objects.get_or_create(user=User.objects.get(id='11')); \
Token.objects.get_or_create(user=User.objects.get(id='12')); \
Token.objects.get_or_create(user=User.objects.get(id='13')); \
Token.objects.get_or_create(user=User.objects.get(id='14')); \
Token.objects.get_or_create(user=User.objects.get(id='15')); \
Token.objects.get_or_create(user=User.objects.get(id='16')); \
Token.objects.get_or_create(user=User.objects.get(id='17')); \
Token.objects.get_or_create(user=User.objects.get(id='18')); \
Token.objects.get_or_create(user=User.objects.get(id='19')); \
Token.objects.get_or_create(user=User.objects.get(id='20')); \
Token.objects.get_or_create(user=User.objects.get(id='21')); \
Token.objects.get_or_create(user=User.objects.get(id='22')); \
Token.objects.get_or_create(user=User.objects.get(id='23')); \
Token.objects.get_or_create(user=User.objects.get(id='24')); \
Token.objects.get_or_create(user=User.objects.get(id='25')); \
Token.objects.get_or_create(user=User.objects.get(id='26')); \
Token.objects.get_or_create(user=User.objects.get(id='27')); \
Token.objects.get_or_create(user=User.objects.get(id='28')); \
Token.objects.get_or_create(user=User.objects.get(id='29')); \
Token.objects.get_or_create(user=User.objects.get(id='30')); \
count = Token.objects.all().count()
print(f'Total entries made: {count}.')
"
echo "...token created."