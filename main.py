from sh import git
import tempfile

from sourcerepo_sync.event import Event
from sourcerepo_sync.sourcerepo import SourceRepo


def sync(event, context):
    event = Event(event)
    sourcerepo = SourceRepo(event)

    with tempfile.TemporaryDirectory() as tmpdir:
        git.clone('--mirror', event.clone_url, _cwd=tmpdir)
        git.push('--mirror', sourcerepo.url, _cwd=tmpdir)

    return
