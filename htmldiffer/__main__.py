import sys
import diff

try:
    a, b = sys.argv[1:3]
except ValueError:
    print("htmldiffer: highlight the differences between two html files")
    print("usage: " + sys.argv[0] + " a b")
    sys.exit(1)
d = diff.HTMLDiffer(a, b)

print(d.deleted_diff, d.inserted_diff, d.combined_diff)