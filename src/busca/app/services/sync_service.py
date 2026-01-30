class SyncService:

    def __init__(self, orig_repo, dest_repo):
        self.orig_repo = orig_repo
        self.dest_repo = dest_repo

    def sync(self):
        orig_state = self.orig_repo.get_current_state()
        delta = list(self.dest_repo.extract(orig_state))

        self.dest_repo.save_all(delta)

        return {
            self.orig_repo.__class__.__name__: len(orig_state),
            "delta": len(delta),
            self.dest_repo.__class__.__name__: self.dest_repo.size(),
        }
