#!/usr/bin/env python3
"""Phase 70 end-to-end rollback drill — disposable copy only.

Proves the restore mechanism against a disposable copy of the uplift profile:
1. copy profile (config.yaml + lcm.db + checkpoints manifest) to a scratch dir
2. simulate a bounded-layer "upgrade" (config mutation + lcm.db row insert)
3. restore last-known-good pins (phase10 config snapshot + phase20C lcm backup)
4. verify restored bytes and row counts, emit JSON evidence
Never touches the live profile (reads only).
"""
import hashlib
import json
import shutil
import sqlite3
import sys
import tempfile
from pathlib import Path

PROFILE = Path.home() / ".hermes/profiles/uplift"
EV = PROFILE / "uplift/evidence"
CFG_SNAPSHOT = EV / "phase10-config-snapshot.yaml"
LCM_BACKUP = EV / "phase20C-lcm-backup.db"

def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def db_messages(db: Path) -> int:
    con = sqlite3.connect(f"file:{db}?mode=ro&immutable=1", uri=True)
    n = con.execute("select count(*) from messages").fetchone()[0]
    con.close()
    return n

def main() -> int:
    ev: dict = {"drill": "phase70-end-to-end-rollback", "live_profile_touched": False}
    work = Path(tempfile.mkdtemp(prefix="phase70-rollback-"))
    ev["scratch_dir"] = str(work).replace(str(Path.home()), "~")

    # 1. disposable copy (read-only wrt live profile)
    copy = work / "profile-copy"
    copy.mkdir()
    shutil.copy2(PROFILE / "config.yaml", copy / "config.yaml")
    shutil.copy2(PROFILE / "lcm.db", copy / "lcm.db")
    ev["pre_upgrade"] = {
        "config_sha256": sha256(copy / "config.yaml"),
        "lcm_db_messages": db_messages(copy / "lcm.db"),
    }

    # 2. simulate a bounded-layer upgrade in the copy ONLY
    cfg = copy / "config.yaml"
    text = cfg.read_text()
    mutated = text.replace("tirith_fail_open: true", "tirith_fail_open: false")
    if mutated == text:  # config layout changed; inject a visible marker instead
        mutated = text + "\n# phase70-drill-simulated-upgrade\n"
    cfg.write_text(mutated)
    con = sqlite3.connect(copy / "lcm.db")
    con.execute(
        "insert into messages(session_id, role, content, timestamp) values ('phase70-drill','assistant','simulated upgrade artifact', datetime('now'))")
    con.commit()
    con.close()
    ev["simulated_upgrade"] = {
        "config_changed": mutated != text,
        "config_sha256": sha256(cfg),
        "lcm_db_messages": db_messages(copy / "lcm.db"),
    }

    # 3. restore last-known-good pins into the copy
    shutil.copy2(CFG_SNAPSHOT, cfg)
    shutil.copy2(LCM_BACKUP, copy / "lcm.db")
    for suffix in ("-wal", "-shm"):
        src = Path(str(LCM_BACKUP) + suffix)
        if src.exists():
            shutil.copy2(src, Path(str(copy / "lcm.db") + suffix))

    # 4. verify restore
    ok_cfg = sha256(cfg) == sha256(CFG_SNAPSHOT)
    msgs = db_messages(copy / "lcm.db")
    con = sqlite3.connect(f"file:{copy/'lcm.db'}?mode=ro&immutable=1", uri=True)
    drift = con.execute(
        "select count(*) from messages where session_id='phase70-drill'").fetchone()[0]
    con.close()
    ev["restore"] = {
        "config_sha256": sha256(cfg),
        "config_matches_known_good_snapshot": ok_cfg,
        "lcm_backup_source_sha256": sha256(LCM_BACKUP),
        "lcm_db_messages_restored": msgs,
        "simulated_artifact_rows_after_restore": drift,
    }
    ev["gates"] = {
        "config_restored_identical": ok_cfg,
        "db_restored_and_readable": drift == 0 and msgs > 0,
    }
    ev["pass"] = all(ev["gates"].values())
    out = EV / "phase70-rollback-drill.json"
    out.write_text(json.dumps(ev, indent=2, sort_keys=True))
    shutil.rmtree(work, ignore_errors=True)
    print(json.dumps({"pass": ev["pass"], "evidence": str(out)}))
    return 0 if ev["pass"] else 1

if __name__ == "__main__":
    sys.exit(main())
