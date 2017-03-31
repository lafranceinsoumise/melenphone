from django.core.management.base import BaseCommand, CommandError

from callcenter.actions.callhub import verify_wehbook, create_webhook

from requests import exceptions

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Checking if webhook already exists...')

        try:
            if(verify_wehbook()):
                self.stdout.write(self.style.SUCCESS('Webhook already exists.'))
                self.stdout.write('Nothing to do.')

            else:
                self.stdout.write('Webhook does not exist. Creating it...')
                create_webhook()
                self.stdout.write(self.style.SUCCESS('Webhook created!'))

        except exceptions.ConnectionError:
            raise CommandError('ConnectionError: could not reach callhub API')
        except exceptions.HTTPError:
            raise CommandError('Callhub returned HTTP error')
        except ValueError:
            raise CommandError('Callhub returned unexpected content')
