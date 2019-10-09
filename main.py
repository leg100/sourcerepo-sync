import tempfile
import sh


def sync(event, context):
    event = Event(event)
    sourcerepo = SourceRepo(event)

    with tempfile.TemporaryDirectory() as tmp_dir:
        git = sh.git.bake(_cwd=tmp_dir)
        git.clone('--mirror', event.clone_url, '.')
        git.push('--mirror', sourcerepo.url)

    return
