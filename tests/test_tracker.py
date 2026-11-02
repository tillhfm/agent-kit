import os
import subprocess
import sys
import tempfile
import unittest

TRACKER = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "plugin", "scripts", "tracker")


class TrackerTest(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()

    def run_tracker(self, *args, text=None, ok=True):
        env = dict(os.environ, AGENT_KIT_TRACKER_DIR=self.dir)
        done = subprocess.run([sys.executable, TRACKER, *args], input=text, env=env, capture_output=True, text=True)
        if ok:
            self.assertEqual(done.returncode, 0, done.stderr)
        return done.stdout + done.stderr

    def create(self, title, *args):
        return self.run_tracker("create", "--title", title, *args, "-", text=f"{title} wanted.").split()[0]

    def test_frontier_lists_ready_items_by_priority_without_open_blockers(self):
        low = self.create("Low", "--state", "ready", "--priority", "low")
        high = self.create("High", "--state", "ready", "--priority", "high")
        blocker = self.create("Blocker", "--state", "ready")
        blocked = self.create("Blocked", "--state", "ready", "--priority", "urgent", "--blocked-by", blocker)
        self.create("Idea")
        lines = self.run_tracker("frontier").splitlines()
        self.assertEqual([line.split("\t")[0] for line in lines], [high, low, blocker])
        self.run_tracker("set", blocker, "--state", "done")
        self.assertEqual(self.run_tracker("frontier").splitlines()[0].split("\t")[0], blocked)

    def test_claim_refuses_an_item_already_in_progress(self):
        n = self.create("Task", "--state", "ready")
        self.run_tracker("claim", n)
        self.assertIn(f"{n} is in-progress", self.run_tracker("claim", n, ok=False))

    def test_finish_appends_the_comment_and_set_description_keeps_comments(self):
        n = self.create("Task", "--state", "ready")
        self.run_tracker("claim", n)
        self.run_tracker("finish", n, "--review", "-", text="What was asked: a task.")
        self.run_tracker("set", n, "--description", "-", text="Task rewritten.")
        shown = self.run_tracker("show", n)
        self.assertIn("state: review", shown)
        self.assertIn("Task rewritten.", shown)
        self.assertNotIn("Task wanted.", shown)
        self.assertIn("What was asked: a task.", shown)

    def test_attach_copies_the_file_and_names_it_in_a_comment(self):
        n = self.create("Task")
        shot = os.path.join(tempfile.mkdtemp(), "shot.png")
        with open(shot, "wb") as f:
            f.write(b"png")
        self.run_tracker("attach", n, shot)
        self.assertTrue(os.path.isfile(os.path.join(self.dir, f"{n}.files", "shot.png")))
        self.assertIn("Attached:", self.run_tracker("show", n))

    def test_a_title_with_a_newline_is_refused(self):
        self.assertIn("one line", self.run_tracker("create", "--title", "A\nB", "-", text="x", ok=False))

    def test_unknown_state_is_refused(self):
        self.assertIn("unknown state", self.run_tracker("create", "--title", "X", "--state", "todo", "-", text="x", ok=False))

    def first_column(self):
        return [line.split("\t")[:2] for line in self.run_tracker("frontier").splitlines()]

    def test_frontier_lists_sub_items_of_an_active_area_and_then_the_due_report(self):
        area = self.create("Area", "--state", "ready")
        sub = self.create("Iteration", "--parent", area, "--state", "ready")
        queued = self.create("Later", "--parent", area)
        self.assertEqual(self.first_column(), [[sub, "none"]])
        self.run_tracker("claim", sub)
        self.assertIn("state: in-progress", self.run_tracker("show", area))
        self.assertEqual(self.run_tracker("frontier").strip(), "frontier empty")
        said = self.run_tracker("finish", sub, "--done", "-", text="Report.")
        self.assertIn(f"{area} has no sub-item ready or in progress", said)
        self.assertEqual(self.first_column(), [[area, "report"]])
        self.assertIn(f"sub-item: {queued} [idea] Later", self.run_tracker("show", area))

    def test_a_ready_area_without_active_sub_items_is_on_the_frontier_for_its_next_iteration(self):
        area = self.create("Area", "--state", "ready")
        self.create("Parked", "--parent", area)
        self.assertEqual(self.first_column(), [[area, "none"]])

    def test_a_sub_item_of_an_area_in_review_waits(self):
        area = self.create("Area", "--state", "review")
        sub = self.create("Iteration", "--parent", area, "--state", "ready")
        self.assertEqual(self.run_tracker("frontier").strip(), "frontier empty")
        self.assertIn("is review", self.run_tracker("claim", sub, ok=False))

    def test_an_area_is_not_claimed_but_its_sub_items_are(self):
        area = self.create("Area", "--state", "ready")
        self.create("Iteration", "--parent", area, "--state", "ready")
        self.assertIn("claim one of its sub-items", self.run_tracker("claim", area, ok=False))

    def test_a_flat_item_in_progress_is_no_due_report(self):
        flat = self.create("Flat", "--state", "ready")
        self.run_tracker("claim", flat)
        self.assertEqual(self.run_tracker("frontier").strip(), "frontier empty")

    def test_an_area_with_active_sub_items_is_not_closed(self):
        area = self.create("Area", "--state", "ready")
        self.create("Iteration", "--parent", area, "--state", "ready")
        self.assertIn("still has active sub-items", self.run_tracker("finish", area, "--done", "-", text="x", ok=False))
        self.assertIn("still has active sub-items", self.run_tracker("set", area, "--state", "idea", ok=False))

    def test_an_item_in_review_does_not_become_a_sub_item(self):
        area = self.create("Area", "--state", "ready")
        looked = self.create("Look", "--state", "review")
        self.assertIn("never in review", self.run_tracker("set", looked, "--parent", area, ok=False))

    def test_a_sub_item_never_goes_to_review(self):
        area = self.create("Area", "--state", "ready")
        sub = self.create("Iteration", "--parent", area, "--state", "ready")
        self.assertIn("never in review", self.run_tracker("finish", sub, "--review", "-", text="x", ok=False))
        self.assertIn("never in review", self.run_tracker("set", sub, "--state", "review", ok=False))
        self.assertIn("never in review", self.run_tracker(
            "create", "--title", "X", "--parent", area, "--state", "review", "-", text="x", ok=False))

    def test_an_area_with_active_sub_items_cannot_go_to_review(self):
        area = self.create("Area", "--state", "ready")
        sub = self.create("Iteration", "--parent", area, "--state", "ready")
        self.assertIn(f"active sub-items: {sub}", self.run_tracker("finish", area, "--review", "-", text="x", ok=False))
        self.run_tracker("claim", sub)
        self.run_tracker("set", sub, "--state", "idea")
        self.run_tracker("finish", area, "--review", "-", text="Area report.")

    def test_a_sub_item_cannot_be_a_parent(self):
        area = self.create("Area")
        sub = self.create("Iteration", "--parent", area)
        self.assertIn("a sub-item's parent is an area item", self.run_tracker(
            "create", "--title", "X", "--parent", sub, "-", text="x", ok=False))
        other = self.create("Other")
        self.run_tracker("set", other, "--parent", area)
        self.assertIn(f"{other}\tidea\t{area}\tOther", self.run_tracker("list"))


if __name__ == "__main__":
    unittest.main()
