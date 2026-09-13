import os
import shutil
import tempfile
import time
from utils.input_loader import load_local_inputs, _read_file_cached


def test_load_local_inputs_caching_and_invalidation():
    tmpdir = tempfile.mkdtemp()
    try:
        # Create dummy search input files
        brief_path = os.path.join(tmpdir, "brief_jd.txt")
        with open(brief_path, "w", encoding="utf-8") as f:
            f.write("Initial JD Content")

        cand_dir = os.path.join(tmpdir, "candidate1")
        os.makedirs(cand_dir, exist_ok=True)
        cv_path = os.path.join(cand_dir, "cv.txt")
        with open(cv_path, "w", encoding="utf-8") as f:
            f.write("Initial CV Content")

        _read_file_cached.cache_clear()

        # First call: cache miss
        search_inputs1, candidates1 = load_local_inputs(tmpdir)
        assert search_inputs1.get("jd_text") == "Initial JD Content"
        assert candidates1.get("candidate1", {}).get("cv_text") == "Initial CV Content"

        hits_before = _read_file_cached.cache_info().hits

        # Second call: cache hit
        search_inputs2, candidates2 = load_local_inputs(tmpdir)
        hits_after = _read_file_cached.cache_info().hits
        assert search_inputs2.get("jd_text") == "Initial JD Content"
        assert candidates2.get("candidate1", {}).get("cv_text") == "Initial CV Content"
        assert hits_after > hits_before

        # Update file content and update mtime explicitly
        with open(brief_path, "w", encoding="utf-8") as f:
            f.write("Updated JD Content")
        os.utime(brief_path, (time.time() + 10, time.time() + 10))

        # Third call: cache invalidation for modified file
        search_inputs3, candidates3 = load_local_inputs(tmpdir)
        assert search_inputs3.get("jd_text") == "Updated JD Content"
        assert candidates3.get("candidate1", {}).get("cv_text") == "Initial CV Content"
    finally:
        shutil.rmtree(tmpdir)
