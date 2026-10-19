# -*- coding: utf-8 -*-
"""
CHƯƠNG TRÌNH ĐIỀU PHỐI XUẤT TÀI LIỆU WORD:
BÁO CÁO BÀI TẬP LỚN - TRẢ LỜI CHI TIẾT 10 CÂU HỎI (10,0 ĐIỂM)
MÔN: XỬ LÝ DỮ LIỆU LỚN (CTKU122) - TRƯỜNG ĐH TÀI NGUYÊN VÀ MÔI TRƯỜNG HÀ NỘI
"""

import os
import sys
if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

from build_10_cau_cover import build_cover_page
from build_10_cau_content_p1 import add_cau_1, add_cau_2, add_cau_3
from build_10_cau_content_p2 import add_cau_4, add_cau_5, add_cau_6
from build_10_cau_content_p3 import add_cau_7, add_cau_8, add_cau_9, add_cau_10

def build_full_document(output_path):
    print(">>> [1/5] Khởi tạo tài liệu Word chuẩn A4...")
    doc = docx.Document()
    
    # 1. Cấu hình lề trang theo quy chuẩn A4: Trái 3cm, Phải 2cm, Trên 2cm, Dưới 2cm
    for section in doc.sections:
        section.top_margin = Inches(2.0 / 2.54)
        section.bottom_margin = Inches(2.0 / 2.54)
        section.left_margin = Inches(3.0 / 2.54)
        section.right_margin = Inches(2.0 / 2.54)
        section.different_first_page_header_footer = True
        
        # Header & Footer cho các trang sau trang bìa
        header = section.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("BTL Xử lý Dữ liệu lớn (CTKU122) - Trả lời 10 câu hỏi đánh giá điểm")
        hrun.font.name = "Times New Roman"
        hrun.font.size = Pt(8.5)
        hrun.font.italic = True
        hrun.font.color.rgb = RGBColor(0x71, 0x80, 0x96)
        
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        frun = fp.add_run("Trường Đại học Tài nguyên và Môi trường Hà Nội - Khoa Công nghệ thông tin")
        frun.font.name = "Times New Roman"
        frun.font.size = Pt(8.5)
        frun.font.italic = True
        frun.font.color.rgb = RGBColor(0x71, 0x80, 0x96)

    # 2. Xây dựng trang bìa
    print(">>> [2/5] Đang tạo trang bìa chuẩn mẫu HUNRE...")
    build_cover_page(doc)

    # 3. Thêm nội dung từ Câu 1 đến Câu 5
    print(">>> [3/5] Đang biên soạn nội dung Câu 1 đến Câu 5...")
    add_cau_1(doc)
    add_cau_2(doc)
    add_cau_3(doc)
    add_cau_4(doc)
    add_cau_5(doc)

    # 4. Thêm nội dung từ Câu 6 đến Câu 10
    print(">>> [4/5] Đang biên soạn nội dung Câu 6 đến Câu 10...")
    add_cau_6(doc)
    add_cau_7(doc)
    add_cau_8(doc)
    add_cau_9(doc)
    add_cau_10(doc)

    # 5. Lưu tệp kết quả
    print(f">>> [5/5] Đang lưu tệp Word hoàn chỉnh tại: {output_path}...")
    doc.save(output_path)
    print(">>> HOÀN TẤT THÀNH CÔNG! File Word đã sẵn sàng.")

if __name__ == "__main__":
    out_file = r"c:\dulieulon\BaoCao_TraLoi_10_CauHoi.docx"
    build_full_document(out_file)
