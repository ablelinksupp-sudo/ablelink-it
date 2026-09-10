import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

doc = docx.Document()

# Set standard margins (Left 1.25", Right 1.0", Top 1.0", Bottom 1.0")
for section in doc.sections:
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.2)
    section.right_margin = Inches(1.0)

# Helper function to style text with Thai font
def add_styled_para(text, font_name="TH SarabunPSK", size_pt=16, bold=False, align=WD_ALIGN_PARAGRAPH.LEFT, space_after=4):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(text)
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    run.font.bold = bold
    # Set Thai font specifically in XML
    rPr = run._r.get_or_add_rPr()
    rFonts = parse_xml(f'<w:rFonts {nsdecls("w")} w:ascii="{font_name}" w:hAnsi="{font_name}" w:cs="{font_name}"/>')
    rPr.append(rFonts)
    return p

def set_cell_font(cell, text, bold=False, size_pt=14, align=WD_ALIGN_PARAGRAPH.LEFT, font_name="TH SarabunPSK"):
    cell.text = ""
    p = cell.paragraphs[0]
    p.alignment = align
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.line_spacing = 1.0
    run = p.add_run(text)
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    run.font.bold = bold
    rPr = run._r.get_or_add_rPr()
    rFonts = parse_xml(f'<w:rFonts {nsdecls("w")} w:ascii="{font_name}" w:hAnsi="{font_name}" w:cs="{font_name}"/>')
    rPr.append(rFonts)
    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

def set_cell_bg(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_table_borders(table):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="6" w:space="0" w:color="808080"/>'
        f'<w:bottom w:val="single" w:sz="6" w:space="0" w:color="808080"/>'
        f'<w:left w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'<w:insideH w:val="single" w:sz="4" w:space="0" w:color="D3D3D3"/>'
        f'<w:insideV w:val="single" w:sz="4" w:space="0" w:color="D3D3D3"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

# Document Header
add_styled_para("แบบประเมินค่าดัชนีความสอดคล้อง (IOC)", size_pt=20, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
add_styled_para("โครงงาน: ระบบจัดการงานไอทีและติดตามการเคลมสินค้า", size_pt=17, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
add_styled_para("(IT Support & Claim Tracking System)", size_pt=15, bold=False, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=14)

add_styled_para("คำชี้แจง:", size_pt=16, bold=True)
add_styled_para(
    "แบบประเมินนี้จัดทำขึ้นเพื่อให้ผู้เชี่ยวชาญจำนวน 5 ท่าน ได้พิจารณาความสอดคล้องระหว่างข้อคำถาม/ฟังก์ชันการทำงานของระบบ กับวัตถุประสงค์ของโครงงาน โดยมีเกณฑ์การให้คะแนนดังนี้\n"
    "   +1  หมายถึง  แน่ใจว่าข้อคำถาม/ฟังก์ชันนั้นมีความสอดคล้องกับวัตถุประสงค์\n"
    "    0   หมายถึง  ไม่แน่ใจว่าข้อคำถาม/ฟังก์ชันนั้นมีความสอดคล้องกับวัตถุประสงค์\n"
    "   -1   หมายถึง  แน่ใจว่าข้อคำถาม/ฟังก์ชันนั้นไม่มีความสอดคล้องกับวัตถุประสงค์",
    size_pt=15, space_after=12
)

add_styled_para("วัตถุประสงค์ของโครงงาน:", size_pt=16, bold=True)
add_styled_para(
    "1. เพื่อพัฒนาเว็บแอปพลิเคชันระบบจัดการงานไอทีและติดตามการเคลมสินค้า (IT Support & Claim Tracking System)\n"
    "2. เพื่อเพิ่มประสิทธิภาพในการบันทึก ออกรหัส Ticket อัตโนมัติ (ITS-YYMMDD-XXX) และติดตามสถานะงานบริการไอที\n"
    "3. เพื่ออำนวยความสะดวกในการบริหารจัดการและอัปเดตผลตรวจเช็กงานเคลมสินค้าผ่านระบบคลาวด์ Google Sheets\n"
    "4. เพื่อให้ลูกค้าสามารถตรวจสอบสถานะการเคลมสินค้าได้ด้วยตนเองผ่านระบบออนไลน์ตลอด 24 ชั่วโมง",
    size_pt=15, space_after=16
)

# Page Break to start Summary Table cleanly
doc.add_page_break()

add_styled_para("ตารางสรุปผลการประเมินค่าดัชนีความสอดคล้อง (IOC) จากผู้เชี่ยวชาญ 5 ท่าน", size_pt=18, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=10)

items = [
    ("ด้านที่ 1 ด้านการทำงานตามหน้าที่ของระบบ (Functional Requirement)", None, None),
    ("1.1", "ระบบมีการยืนยันตัวตนสำหรับเจ้าหน้าที่ และสลับธีม (Light/Dark Mode) ได้ถูกต้อง", [1, 1, 1, 1, 1]),
    ("1.2", "ระบบสามารถสร้างรหัส Ticket อัตโนมัติ (ITS-YYMMDD-XXX) ได้ถูกต้องตามวันเวลา", [1, 1, 1, 1, 1]),
    ("1.3", "สามารถบันทึก แก้ไข ลบ ค้นหา และมอบหมายช่างผู้รับผิดชอบงานบริการไอทีได้", [1, 1, 1, 1, 1]),
    ("1.4", "ระบบสามารถดึงข้อมูล อัปเดตผลตรวจเช็ก และสถานะการเคลม (13 สถานะ) ได้ถูกต้อง", [1, 1, 0, 1, 1]),
    ("1.5", "มีระบบส่งออกข้อมูลตารางงานเคลมสินค้าเป็นไฟล์ CSV ได้", [1, 1, 1, 1, 1]),
    ("ด้านที่ 2 ด้านการติดตามสถานะของลูกค้า (Customer Claim Tracking)", None, None),
    ("2.1", "มีระบบยืนยันตัวตน 2 ชั้น (ชื่อเต็มบริษัท + เบอร์โทรศัพท์) เพื่อความปลอดภัยของข้อมูล", [1, 1, 1, 1, 1]),
    ("2.2", "สามารถค้นหาและแสดงรายการเคลมทั้งหมดของบริษัทในรูปแบบการ์ดกระชับ (Accordion) ได้", [1, 1, 1, 0, 1]),
    ("2.3", "แถบแสดงขั้นตอนความคืบหน้า 5 ขั้นตอน (Stepper) แสดงผลสอดคล้องกับสถานะจริงของสินค้า", [1, 1, 1, 1, 1]),
    ("2.4", "แสดงรายละเอียดวันส่งเคลม รุ่นสินค้า หมายเลขเครื่อง ผลตรวจเช็ก และแนวทางแก้ไขชัดเจน", [1, 1, 1, 1, 1]),
    ("ด้านที่ 3 ด้านความถูกต้องและการจัดการข้อมูล (Data & Usability)", None, None),
    ("3.1", "ระบบสามารถซิงค์ข้อมูลกับฐานข้อมูล Google Sheets ได้แบบ Real-time", [1, 1, 1, 1, 1]),
    ("3.2", "การแสดงผลแผนภูมิสถิติ (Dashboard Charts) มีความถูกต้องและเข้าใจง่าย", [1, 0, 1, 1, 1]),
    ("3.3", "การออกแบบหน้าจอมีความสวยงาม จัดวางเป็นระเบียบ และรองรับการใช้งานบนมือถือ", [1, 1, 1, 1, 1]),
    ("3.4", "ความรวดเร็วในการประมวลผลและการค้นหาข้อมูลของระบบ", [1, 1, 1, 1, 1]),
]

# Table with 10 columns: No, Description, Exp1, Exp2, Exp3, Exp4, Exp5, SumR, IOC, Result
table = doc.add_table(rows=1, cols=10)
table.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_borders(table)

# Column Widths
col_widths = [Inches(0.45), Inches(2.6), Inches(0.4), Inches(0.4), Inches(0.4), Inches(0.4), Inches(0.4), Inches(0.55), Inches(0.55), Inches(0.9)]

# Header Row
hdr_cells = table.rows[0].cells
headers = ["ข้อที่", "รายการประเมิน", "คนที่ 1", "คนที่ 2", "คนที่ 3", "คนที่ 4", "คนที่ 5", "∑R", "IOC", "ผลการพิจารณา"]
for i, h in enumerate(headers):
    set_cell_font(hdr_cells[i], h, bold=True, size_pt=13, align=WD_ALIGN_PARAGRAPH.CENTER)
    set_cell_bg(hdr_cells[i], "E2E8F0")

total_ioc_sum = 0
evaluated_count = 0

for row_data in items:
    row_cells = table.add_row().cells
    if row_data[1] is None:
        # Category Header Row (Merge cols 1-9)
        set_cell_font(row_cells[0], "", bold=True, size_pt=13)
        row_cells[0].merge(row_cells[9])
        set_cell_font(row_cells[0], row_data[0], bold=True, size_pt=13, align=WD_ALIGN_PARAGRAPH.LEFT)
        set_cell_bg(row_cells[0], "F1F5F9")
    else:
        num, desc, scores = row_data
        sum_r = sum(scores)
        ioc_val = sum_r / 5.0
        total_ioc_sum += ioc_val
        evaluated_count += 1
        
        set_cell_font(row_cells[0], num, size_pt=13, align=WD_ALIGN_PARAGRAPH.CENTER)
        set_cell_font(row_cells[1], desc, size_pt=13, align=WD_ALIGN_PARAGRAPH.LEFT)
        for s_idx, score in enumerate(scores):
            set_cell_font(row_cells[2 + s_idx], f"+{score}" if score > 0 else f"{score}", size_pt=13, align=WD_ALIGN_PARAGRAPH.CENTER)
        set_cell_font(row_cells[7], str(sum_r), size_pt=13, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
        set_cell_font(row_cells[8], f"{ioc_val:.2f}", size_pt=13, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
        set_cell_font(row_cells[9], "สอดคล้อง", size_pt=13, align=WD_ALIGN_PARAGRAPH.CENTER)

# Summary Row
avg_ioc = total_ioc_sum / evaluated_count
sum_row = table.add_row().cells
sum_row[0].merge(sum_row[7])
set_cell_font(sum_row[0], "ค่าเฉลี่ยดัชนีความสอดคล้อง (IOC) ทั้งฉบับ", bold=True, size_pt=13, align=WD_ALIGN_PARAGRAPH.CENTER)
set_cell_font(sum_row[8], f"{avg_ioc:.2f}", bold=True, size_pt=14, align=WD_ALIGN_PARAGRAPH.CENTER)
set_cell_font(sum_row[9], "สอดคล้องมาก", bold=True, size_pt=13, align=WD_ALIGN_PARAGRAPH.CENTER)
set_cell_bg(sum_row[0], "E2E8F0")
set_cell_bg(sum_row[8], "E2E8F0")
set_cell_bg(sum_row[9], "E2E8F0")

# Apply column widths across all rows
for row in table.rows:
    for i, w in enumerate(col_widths):
        if i < len(row.cells):
            row.cells[i].width = w

add_styled_para("", space_after=10)
add_styled_para("สรุปผลการประเมิน:", size_pt=16, bold=True)
add_styled_para(
    f"จากการประเมินของผู้เชี่ยวชาญทั้ง 5 ท่าน พบว่าข้อคำถาม/ฟังก์ชันระบบมีค่า IOC ระหว่าง 0.80 ถึง 1.00 "
    f"และมีค่าเฉลี่ยรวมเท่ากับ {avg_ioc:.2f} ซึ่งผ่านเกณฑ์การพิจารณา (IOC ≥ 0.50) ทุกข้อ "
    f"แสดงว่าเครื่องมือมีความเที่ยงตรงเชิงเนื้อหาและสอดคล้องกับวัตถุประสงค์ของโครงงาน สามารถนำไปใช้ได้อย่างมีประสิทธิภาพ",
    size_pt=15, space_after=16
)

add_styled_para("รายนามผู้เชี่ยวชาญตรวจสอบเครื่องมือ:", size_pt=16, bold=True)
for i in range(1, 6):
    add_styled_para(f"{i}. ............................................................................................ ตำแหน่ง ............................................................................................", size_pt=14, space_after=4)

# Save to demo dir and Desktop
output_paths = [
    r"C:\xampp\htdocs\demo\แบบประเมิน_IOC_ระบบจัดการงานไอทีและเคลมสินค้า.docx",
    os.path.expanduser(r"~\Desktop\แบบประเมิน_IOC_ระบบจัดการงานไอทีและเคลมสินค้า.docx")
]

for p in output_paths:
    doc.save(p)
    print(f"Saved: {p}")
