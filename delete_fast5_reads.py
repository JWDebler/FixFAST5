from pathlib import Path
from sys import argv
from typing import Set
from pod5.tools.pod5_convert_from_fast5 import collect_inputs, is_multi_read_fast5
from h5py import File


def remove_reads(f5_path: Path, bad_ids: Set[str]):
    if not is_multi_read_fast5(f5_path):
        return f"Not a multi-read fast5: {f5_path}"

    try:
        with File(str(f5_path), "r+") as f5:
            read_ids = set([k for k in f5.keys() if k.startswith("read_")])

            if not read_ids:
                return f"Is empty fast5: {f5_path}"

            common_ids = bad_ids & read_ids

            for read_id in common_ids:
                try:
                    del f5[read_id]  # UNCOMMENT THIS LINE TO DELETE READS
                    print(f"Deleted {read_id} from: {f5_path}")
                except Exception:
                    print(f"Cannot delete {read_id} from: {f5_path}")

    except Exception as exc:
        return f"Other exception: {exc} from: {f5_path}"


def main(search_dir: Path = Path.cwd(), bad_reads: Path = Path.cwd() / "bad_reads.txt"):
    """Remove bad reads from fast5"""

    print(f"Searching {search_dir.resolve()} for fast5 files")

    fast5_paths = collect_inputs([search_dir], False, "*.fast5", threads=1)
    if not fast5_paths:
        raise RuntimeError(
            f"Found no fast5 inputs to process in: {search_dir.resolve()}"
        )

    bad_ids = set(
        [
            line
            for line in bad_reads.read_text().splitlines()
            if line.startswith("read_")
        ]
    )
    if not bad_ids:
        raise RuntimeError(f"Found no read ids in: {bad_reads.resolve()}")

    for f5_path in fast5_paths:
        issue = remove_reads(f5_path, bad_ids)
        if issue: 
            print(issue)


if __name__ == "__main__":
    main(Path(argv[1]), Path(argv[2]))