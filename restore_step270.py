import json

with open(r'C:\Users\Success\.gemini\antigravity-ide\brain\e0dee0d6-8af2-4526-8e65-8a0f86cb110c\.system_generated\logs\transcript_full.jsonl', 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

# ดึงเนื้อหาของ step 270 ซึ่งเป็น write_to_file ที่มี content ยาวสุด
for i, line in enumerate(lines):
    try:
        data = json.loads(line)
        if data.get('step_index') == 270:
            tool_calls = data.get('tool_calls', [])
            for tc in tool_calls:
                if tc.get('name') == 'write_to_file':
                    code = tc.get('args', {}).get('CodeContent', '')
                    print(f"Content length: {len(code)}")
                    # บันทึกเป็นไฟล์
                    with open(r'C:\xampp\htdocs\demo\it_support.html', 'w', encoding='utf-8') as out:
                        out.write(code)
                    print("Saved to it_support.html (step 270 version)")
    except Exception as e:
        pass
