#!/usr/bin/env python3
"""
vision_to_json.py — 비전 지능 기반 고정밀 레이아웃-지식 추출기
=========================================================

이미지(PDF 페이지 스캔본)를 분석하여 시각적 좌표가 아닌
'의미론적 블록(Semantic Blocks)' 구조의 고정밀 JSON을 생성합니다.

이 스크립트는 OCR을 직접 수행하지 않습니다. 대신 에이전트가 채워야 할
**표준 스키마 골격(skeleton) JSON 파일을 생성**하고, 명시적 작성 계약을
출력합니다. 에이전트는 이미지를 읽고 이 골격을 채워 최종본을 만듭니다.

[에이전트 작성 계약]
- 입력:  {image_dir}/  (페이지별 PNG/JPG, 파일명 정렬 = 페이지 순서)
- 출력:  {image_dir 부모}/{이름}_vision.json  (이 스크립트가 골격 생성)
- 채울 것:
  · pages[].page_number  : 실제 인쇄 페이지 번호
  · pages[].blocks[]     : {type: Title|Header|Body|Footnote|Footer,
                            text, lang(원어 시 he/grc/lat)}
  · pages[].relations[]  : {footnote_id, ref_in_body} 본문-각주 링크
"""

import json
import argparse
from pathlib import Path

SCHEMA_VERSION = "Elite Vision v2.1"


def create_elite_json_schema(title, pages_data):
    """Elite Vision 모드의 표준 출력 스키마를 정의합니다."""
    return {
        "document_metadata": {
            "title": title,
            "engine": SCHEMA_VERSION,
            "format": "Theology-Knowledge-Object",
        },
        "pages": pages_data,
    }


def _page_skeleton(page_number: int, source_image: str) -> dict:
    """에이전트가 채울 빈 페이지 골격."""
    return {
        "page_number": page_number,
        "source_image": source_image,
        "blocks": [],      # {"type": "Body", "text": "", "lang": null}
        "relations": [],   # {"footnote_id": "1", "ref_in_body": ""}
    }


def build_skeleton(image_dir: str, output: str | None = None) -> str | None:
    img_path = Path(image_dir)
    if not img_path.is_dir():
        print(f"❌ 디렉토리가 아닙니다: {image_dir}")
        return None

    images = sorted(
        f for f in img_path.iterdir()
        if f.suffix.lower() in (".jpg", ".jpeg", ".png")
    )
    if not images:
        print(f"⚠️ 이미지를 찾을 수 없습니다: {image_dir}")
        return None

    title = img_path.name.replace("_images", "")
    pages = [_page_skeleton(i + 1, img.name) for i, img in enumerate(images)]
    schema = create_elite_json_schema(title, pages)

    if not output:
        output = str(img_path.parent / f"{title}_vision.json")
    Path(output).write_text(
        json.dumps(schema, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"🚀 Elite V2J 골격 생성: {output}  ({len(images)} 페이지)")
    print("💡 에이전트 작성 계약:")
    print(f"  1. 입력 이미지({len(images)}장)를 페이지 순서대로 읽으십시오.")
    print("  2. 각 페이지의 Header/Footer를 Body와 분리하여 blocks[]에 기록")
    print("  3. 본문 각주 번호를 식별하여 relations[]에 등록")
    print("  4. 독일어/희랍어/히브리어 원전은 blocks[].lang 태그 부여")
    print(f"  5. 위 골격 파일을 채워 같은 경로에 저장하십시오: {output}")
    return output


def main():
    parser = argparse.ArgumentParser(description="Vision-to-JSON 시맨틱 추출기 (골격 생성)")
    parser.add_argument("image_dir", help="이미지 디렉토리 경로")
    parser.add_argument("--output", "-o", help="결과 JSON 파일 경로")
    args = parser.parse_args()
    build_skeleton(args.image_dir, args.output)


if __name__ == "__main__":
    main()
