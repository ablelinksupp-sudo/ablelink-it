# Apply all subsequent patches on top of step 270 base
import json

with open(r'C:\Users\Success\.gemini\antigravity-ide\brain\e0dee0d6-8af2-4526-8e65-8a0f86cb110c\.system_generated\logs\transcript_full.jsonl', 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

# ดึง patches จาก steps 303,318,326,514,554,568,898,909,910,1160,1162,1166,1174,1184 
patch_steps = [303, 318, 326, 514, 554, 568, 898, 909, 910, 1160, 1162, 1166, 1174, 1184]
patches = {}
for i, line in enumerate(lines):
    try:
        data = json.loads(line)
        si = data.get('step_index')
        if si in patch_steps:
            patches[si] = data
    except:
        pass

print("Found patch steps:", sorted(patches.keys()))

with open(r'C:\xampp\htdocs\demo\it_support.html', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

print(f"Base content: {len(content)} chars")

# Apply replace_file_content patches in order
for si in sorted(patches.keys()):
    data = patches[si]
    tool_calls = data.get('tool_calls', [])
    for tc in tool_calls:
        name = tc.get('name', '')
        args = tc.get('args', {})
        target = args.get('TargetFile', '')
        if 'it_support.html' not in str(target):
            continue
        if name == 'replace_file_content':
            old = args.get('TargetContent', '')
            new = args.get('ReplacementContent', '')
            if old and old in content:
                content = content.replace(old, new, 1)
                print(f"  Step {si}: replaced {len(old)} -> {len(new)} chars OK")
            else:
                print(f"  Step {si}: SKIP (TargetContent not found, len={len(old)})")
        elif name == 'multi_replace_file_content':
            chunks = args.get('ReplacementChunks', [])
            for chunk in chunks:
                old = chunk.get('TargetContent', '')
                new = chunk.get('ReplacementContent', '')
                if old and old in content:
                    content = content.replace(old, new, 1)
                    print(f"  Step {si} chunk: replaced {len(old)} chars OK")
                else:
                    print(f"  Step {si} chunk: SKIP (not found, len={len(old)})")

print(f"\nFinal content: {len(content)} chars")
with open(r'C:\xampp\htdocs\demo\it_support.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Saved!")
