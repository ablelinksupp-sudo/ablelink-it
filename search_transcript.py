import json

with open(r'C:\Users\Success\.gemini\antigravity-ide\brain\e0dee0d6-8af2-4526-8e65-8a0f86cb110c\.system_generated\logs\transcript_full.jsonl', 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

# ค้นหา tool_calls ที่มี write_to_file กับ it_support.html
results = []
for i, line in enumerate(lines):
    try:
        data = json.loads(line)
        tool_calls = data.get('tool_calls', [])
        for tc in tool_calls:
            args = tc.get('args', {})
            target = args.get('TargetFile', '') or args.get('targetFile', '')
            if 'it_support.html' in str(target):
                code = args.get('CodeContent', '') or args.get('ReplacementContent', '') or args.get('CommandLine', '')
                results.append((data.get('step_index', i), len(str(code)), tc.get('name','')))
    except:
        pass

print("Found steps with it_support.html writes:")
for r in results:
    print(f"  step {r[0]}: {r[2]} - content len {r[1]}")
