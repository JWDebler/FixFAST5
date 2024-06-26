from pathlib import Path
from sys import argv
from typing import List
from pod5.tools.pod5_convert_from_fast5 import collect_inputs, is_multi_read_fast5
from h5py import File


def test_file(f5_path) -> List[str]:
    issues = []
    if not is_multi_read_fast5(f5_path):
        issues.append(f"Not a multi-read fast5: {f5_path}")
        return issues

    try:
        with File(str(f5_path), "r") as f5:
            read_ids = [k for k in f5.keys() if k.startswith("read_")]

            if not read_ids:
                issues.append(f"Is empty fast5: {f5_path}")

            for read_id in read_ids:
                try:
                    read = f5[read_id]
                except Exception:
                    issues.append(f"Cannot read {read_id} from: {f5_path}")

                if not read:
                    issues.append(f"Null read {read_id} from: {f5_path}")

                if "Raw" not in read:
                    issues.append(f"Missing 'Raw' group {read_id} from: {f5_path}")
                else:
                    raw = read["Raw"]
                    if "Signal" not in raw:
                        issues.append(f"Missing 'Raw/Signal' group {read_id} from: {f5_path}")

    except Exception as exc:
        issues.append(f"Other exception: {exc} from: {f5_path}")

    return issues

def main(search_dir: Path = Path.cwd()):
    """Checks all FAST5 files in `search_dir` for issues"""

    print(f"Searching {search_dir.resolve()} for fast5 files")

    fast5_paths = collect_inputs([search_dir], False, "*.fast5", threads=1)
    if not fast5_paths:
        raise RuntimeError(
            f"Found no fast5 inputs to process in: {search_dir.resolve()}"
        )

    issues = []
    for f5_path in fast5_paths:
        issue = test_file(f5_path)
        if issue:
            issues.extend(issue)

    print(f"Found {len(issues)} issues from {len(fast5_paths)} input paths")
    if issues:
        try:
            outfile = Path.cwd() / "issues.txt"
            with outfile.open("w") as out:
                print(f"Writing {len(issues)} to {outfile}")
                for issue in issues:
                    out.write(issue + "\n")
        except Exception as exc:
            print(f"Failed to write to output file: {exc}")
            for issue in issues:
                print(issue)


if __name__ == "__main__":
    main(Path(argv[1]))