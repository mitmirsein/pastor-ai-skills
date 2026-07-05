#!/usr/bin/env python3
"""
vision_extractor.py — 에이전트 비전 기반 고정밀 신학 논문 추출기
============================================================

전통적인 텍스트 추출 방식이 실패하거나 품질이 낮을 때,
이미지(페이지별 JPEG/PNG)로부터 에이전트의 시각 지능을 활용하여
연구용 마크다운을 직접 생성합니다.

이 스크립트는 OCR을 직접 수행하지 않습니다. 페이지 순서를 확정하고
**에이전트가 채울 출력 경로와 작성 계약을 명시**하는 컨트롤러입니다.

[에이전트 작성 계약]
- 입력:  {image_dir}/  (페이지별 PNG/JPG, 파일명 정렬 = 페이지 순서)
- 출력:  {image_dir 부모}/{이름}_vision_raw.md   ← 에이전트가 직접 작성
- 산출물 형식: 연구용 마크다운 (원어 보존, 각주는 `> [각주 N]` 블록)

용도 구분:
- vision_extractor.py → 사람이 읽는 **마크다운** 산출 (이 파일)
- vision_to_json.py   → 기계 처리용 **시맨틱 JSON** 골격 산출
"""

import os
import sys
import argparse
from pathlib import Path

def process_vision_extraction(image_dir, output_file=None):
    """
    이미지 디렉토리 내의 파일들을 페이지 순서대로 정렬하여 
    에이전트에게 처리를 요청하는 컨텍스트를 생성합니다.
    """
    img_path = Path(image_dir)
    if not img_path.is_dir():
        print(f"❌ 디렉토리가 아닙니다: {image_dir}")
        return

    # 이미지 파일 수집 및 정렬
    images = sorted(
        [f for f in img_path.iterdir() if f.suffix.lower() in ('.jpg', '.jpeg', '.png')],
        key=lambda x: str(x)
    )

    if not images:
        print(f"⚠️ 이미지를 찾을 수 없습니다: {image_dir}")
        return

    # 출력 경로 설정 (결정적)
    if not output_file:
        output_file = img_path.parent / f"{img_path.name.replace('_images', '')}_vision_raw.md"

    print(f"📷 비전 추출 모드 가동 (총 {len(images)} 페이지 수집됨)")
    print("--------------------------------------------------")
    for idx, img in enumerate(images):
        print(f"  [{idx+1}/{len(images)}] {img.name}")
    print("--------------------------------------------------")
    print("💡 에이전트 작성 계약:")
    print(f"  1. 위 {len(images)}개 이미지를 페이지 순서대로 '고정밀 신학 OCR' 하십시오.")
    print("  2. 원어(히브리어/헬라어/독일어)는 원문 그대로 보존")
    print("  3. 각주는 `> [각주 N]` 블록으로 분리")
    print(f"  4. 결과 마크다운을 다음 경로에 저장하십시오:\n     {output_file}")

    return str(output_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="비전 기반 이미지-to-마크다운 추출 컨트롤러")
    parser.add_argument("image_dir", help="추출된 이미지들이 들어있는 디렉토리 경로")
    parser.add_argument("--output", "-o", help="결과 마크다운 파일 경로")
    
    args = parser.parse_args()
    process_vision_extraction(args.image_dir, args.output)
