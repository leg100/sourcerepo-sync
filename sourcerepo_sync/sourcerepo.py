import os
from urllib.parse import quote

from sourcerepo_sync import metadata


class SourceRepo():
    def __init__(self, event):
        self.event = event


    @property
    def url(self):
        project = os.environ['GCP_PROJECT']

        service_account = quote(metadata.service_account())
        token = quote(metadata.access_token())

        return (f'https://{service_account}:{token}@'
            'source.developers.google.com'
            f'/p/{project}'
            f'/r/{self.event.provider}_{self.event.owner}_{self.event.repo}')
