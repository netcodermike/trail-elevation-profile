from math import isfinite

def analyze(data):
    points = data['points']
    if len(points) < 2:
        raise ValueError('At least two points required')
    for x,y in points:
        if not all(type(v) in (int,float) and isfinite(v) for v in (x,y)):
            raise ValueError('Distances and elevations must be finite')
    sections = []
    for (a,b),(c,d) in zip(points,points[1:]):
        if c <= a:
            raise ValueError('Distances must strictly increase')
        sections.append((a,c,d-b,100*(d-b)/(c-a)))
    steepest = max(sections,key=lambda row:row[3])
    return {'gainMeters':sum(max(0,r[2]) for r in sections),
            'lossMeters':sum(max(0,-r[2]) for r in sections),
            'maxUphillPercent':round(max(0,steepest[3]),6),
            'steepestUphillMeters':list(steepest[:2]) if steepest[3] > 0 else None}

if __name__ == "__main__":
    import json
    from pathlib import Path
    import sys
    try:
        path, = sys.argv[1:]
        result = analyze(json.loads(Path(path).read_text(encoding="utf-8")))
        print(json.dumps(result, ensure_ascii=True, allow_nan=False))
    except (OSError, ValueError, TypeError, KeyError, AttributeError, OverflowError) as error:
        print(f"Invalid input: {error}", file=sys.stderr)
        sys.exit(2)
