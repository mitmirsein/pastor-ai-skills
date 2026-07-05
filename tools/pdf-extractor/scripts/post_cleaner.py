import re
import os
import sys


# 문장 종결 부호 `.` 로 끝나도 문장이 끝난 게 아닌 약어들
# (이것들 뒤에서 문단을 flush 하면 신학 텍스트 문장이 중간에 잘림)
ABBREVIATIONS = {
    # 라틴/영어
    'cf', 'cf.', 'vgl', 'vgl.', 'ibid', 'op', 'cit', 'et', 'al', 'al.',
    'ed', 'ed.', 'eds', 'trans', 'tr', 'no', 'nr', 'vol', 'vols', 'pp',
    'esp', 'chap', 'ch', 'sec', 'fig', 'cap', 'col', 'fol', 'lit',
    'i.e', 'e.g', 'viz', 'approx', 'incl', 'St', 'Jr', 'Sr', 'Dr', 'Prof',
    # 독일어
    'z.B', 'u.a', 'd.h', 'usw', 'bzw', 'sog', 'Hrsg', 'Hg', 'Bd', 'Bde',
    'Sp', 'Aufl', 'Diss', 'Anm', 'ebd', 'a.a.O', 'f', 'ff', 'S',
    # 한국어 학술
    '참고', '참조', '이하', '재인용',
}

PAGE_MARKER_RE = re.compile(r'^={5}\s+p\.\d+\s+={5}$')


def _is_abbrev_tail(stripped: str) -> bool:
    """줄이 약어/이니셜로 끝나 문장이 미완결인지 판정.

    - 마지막 토큰이 ABBREVIATIONS 에 속함 (vgl. z.B. Hrsg. 등)
    - 저자 이니셜 패턴으로 끝남 (`R.`, `R.F.`, `J.-P.`)
    """
    if not stripped.endswith('.'):
        return False
    # 저자 이니셜: 끝이 단일 대문자 + 마침표 (옵션 반복)
    if re.search(r'(?:\b[A-ZÄÖÜ]\.){1,4}$', stripped):
        return True
    last = stripped.split()[-1] if stripped.split() else ''
    return last.rstrip('.') in {a.rstrip('.') for a in ABBREVIATIONS}


def clean_markdown(file_path, output_path=None):
    """
    opendataloader 추출 결과의 마크다운을 신학 논문 규격에 맞게 정제합니다.
    
    기능:
    - OCR 노이즈 제거 (하이픈 잘림, 특수문자 오염)
    - Spalte(단 번호) 패턴 탐지 및 강조 표시
    - Literatur(참고문헌) 구역 구조화
    - 문단 결합 (번역 파이프라인 품질 최적화)
    - 공백 정규화

    Args:
        file_path (str): 정제할 .md 파일 경로
        output_path (str, optional): 출력 경로. None이면 _cleaned 접미어 사용
    
    Returns:
        str: 정제된 파일 경로
    """
    print(f"[*] 마크다운 정제 중: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. 하이픈/OCR 노이즈로 잘린 단어 복원
    # 1-a. 줄바꿈 하이프네이션: 라틴 문자 사이에서, 다음 줄이 소문자로
    #      이어질 때만 결합(유럽어 어절 분철). 대문자로 이어지면 고유
    #      합성어 하이픈일 수 있어 보존. 한글/숫자는 건드리지 않음.
    content = re.sub(
        r'([A-Za-zÀ-ÖØ-öø-ÿ]{2,})-\s*\n\s*([a-zà-öø-ÿ]+)',
        r'\1\2', content,
    )
    # 1-b. 단어 내부 물결표(~) OCR 노이즈 제거 — 라틴 문자 사이만.
    #      한국어 가운뎃점(·)은 정상 구분자(예: 북·동·서·남, 저자 나열)
    #      이므로 제거하지 않는다.
    content = re.sub(r'([A-Za-z])~([A-Za-z])', r'\1\2', content)

    # 2. Spalte(단 번호) 패턴 탐지 및 강조 (독일어 신학 사전 Sp. 표기)
    content = re.sub(r'(?:\[| )?Sp\.?\s*(\d+)(?:\]| )?', r'\n\n> [Sp. \1]\n\n', content)

    # 3. Literatur(참고문헌) 구역 구조화
    lines = content.split('\n')
    new_lines = []
    in_literatur = False
    for line in lines:
        if 'Literatur' in line and (line.startswith('###') or line.startswith('######')):
            in_literatur = True
            new_lines.append(f"\n{line}\n")
            continue
        if in_literatur:
            # 다음 헤딩이 나오면 Literatur 구역 종료
            if line.startswith('#'):
                in_literatur = False
                new_lines.append(line)
            elif line.strip():
                new_lines.append(f"> {line}")
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)
    content = '\n'.join(new_lines)

    # 4. 문단 결합 (번역 품질 최적화: 한 문단이 여러 줄에 걸쳐 있는 경우 병합)
    lines = content.split('\n')
    processed_lines = []
    temp_line = ""
    for line in lines:
        stripped = line.strip()
        if not stripped:
            if temp_line:
                processed_lines.append(temp_line)
                temp_line = ""
            processed_lines.append("")
            continue
        # 인용문, 헤딩, 페이지 마커는 그대로 유지
        if line.startswith('>') or line.startswith('#') or PAGE_MARKER_RE.match(stripped):
            if temp_line:
                processed_lines.append(temp_line)
                temp_line = ""
            processed_lines.append(line)
            continue
        # 문장 병합
        if temp_line:
            temp_line = temp_line + " " + stripped
        else:
            temp_line = stripped
        # 문장 종결 부호에서 flush — 단, 약어·이니셜로 끝나면 계속 누적
        # (vgl. / z.B. / Hrsg. / "R.F." 등에서 문장이 잘리는 것 방지)
        if stripped.endswith(('.', '!', '?', ':', ';', '"', ')')) \
                and not _is_abbrev_tail(stripped):
            processed_lines.append(temp_line)
            temp_line = ""
    if temp_line:
        processed_lines.append(temp_line)
    content = '\n'.join(processed_lines)

    # 5. 공백 정규화
    content = re.sub(r' +', ' ', content)
    content = re.sub(r'\n{3,}', '\n\n', content)

    # 출력 경로 결정
    if output_path is None:
        base, ext = os.path.splitext(file_path)
        output_path = f"{base}_cleaned{ext}"

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"[+] 정제 완료 → {output_path}")
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("사용법: python post_cleaner.py <md_파일_경로> [출력_경로]")
        sys.exit(1)
    target_md = sys.argv[1]
    out_path = sys.argv[2] if len(sys.argv) > 2 else None
    if os.path.exists(target_md):
        clean_markdown(target_md, output_path=out_path)
    else:
        print(f"❌ 파일 없음: {target_md}")
        sys.exit(1)
