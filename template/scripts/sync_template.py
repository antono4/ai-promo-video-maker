"""Sync generic files that the template has since improved into this project (run this first when revising or continuing an old project).

python3 scripts/sync_template.py            list the generic files that differ from the template (changes nothing)
python3 scripts/sync_template.py --diff     also print the differences
python3 scripts/sync_template.py --apply    overwrite those files with the template version (confirm first that the differences contain no changes specific to this project)

Only style-agnostic generic files are compared: the scripts under scripts/ except mix.py, and the web/ playback logic.
mix.py, timing.json, scenes, theme, fonts.json, web/config.ts, and web/style.css belong to each project and are not touched.

The template is located in this order: the PROMO_TEMPLATE environment variable -> the clone-mode <repo>/template (this project lives in outputs/<project>/project)
-> a promo-video-maker installed in any AI tool's skills directory under the workspace or the user directory (Skill mode).
"""
import argparse
import filecmp
import glob
import os
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL = "promo-video-maker"
SKILL_DIRS = [".claude/skills", ".cursor/skills", ".agents/skills", ".codex/skills", ".config/agents/skills"]
OWN = {"scripts/mix.py"}


def find_template():
    if os.environ.get("PROMO_TEMPLATE"):
        return os.path.abspath(os.environ["PROMO_TEMPLATE"])
    workspace = os.path.normpath(os.path.join(ROOT, "..", "..", ".."))
    if os.path.isfile(os.path.join(workspace, "template", "scripts", "sync_template.py")):
        return os.path.join(workspace, "template")
    for base in (workspace, os.path.expanduser("~")):
        for d in SKILL_DIRS:
            for skill_md in glob.glob(os.path.join(base, d, "*", "SKILL.md")):
                if f"name: {SKILL}" in open(skill_md, encoding="utf-8").read():
                    return os.path.join(os.path.dirname(skill_md), "template")
    return None


TEMPLATE = find_template()
GENERIC = ["scripts", "web/App.tsx", "web/main.tsx", "web/vite.config.ts"]


def generic_files():
    for g in GENERIC:
        base = os.path.join(TEMPLATE, g)
        if os.path.isfile(base):
            yield g
            continue
        for name in sorted(os.listdir(base)):
            rel = f"{g}/{name}"
            if rel not in OWN and name.endswith((".py", ".js", ".mjs", ".ts", ".tsx")):
                yield rel


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--diff", action="store_true")
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    if not TEMPLATE or not os.path.isdir(TEMPLATE) or os.path.samefile(TEMPLATE, ROOT):
        sys.exit("template not found: this script must run inside <output dir>/<project>/project/; when the template is not in the default location, specify PROMO_TEMPLATE=<tool dir>/template")
    print(f"comparing against {TEMPLATE}")
    css = os.path.join(ROOT, "src", "index.css")
    if os.path.exists(css) and "max-width: none" not in open(css, encoding="utf-8").read():
        print("note  src/index.css is missing img { max-width: none; }: enlarged screenshots will be squashed horizontally; add it as in template/src/index.css")
    changed = []
    for rel in generic_files():
        t, p = os.path.join(TEMPLATE, rel), os.path.join(ROOT, rel)
        if not os.path.exists(p):
            changed.append(rel)
            print(f"missing  {rel}")
        elif not filecmp.cmp(t, p, shallow=False):
            changed.append(rel)
            print(f"differs  {rel}")
            if a.diff:
                subprocess.run(["diff", "-u", p, t])
    if not changed:
        print("all generic files match the template")
        return
    if a.apply:
        for rel in changed:
            shutil.copy2(os.path.join(TEMPLATE, rel), os.path.join(ROOT, rel))
        print(f"overwrote {len(changed)} files with the template version; next run npm run lint and npm run mix to confirm nothing broke")
    else:
        print("once you confirm the differences are all template improvements (not changes specific to this project), add --apply")


if __name__ == "__main__":
    main()
