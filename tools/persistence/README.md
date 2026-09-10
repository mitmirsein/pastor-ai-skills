# 검토한 저장 계획의 재개

`core/_hooks.md` §2.7을 지원하는 선택적 로컬 도구다. 스킬 실행자가 최신 파일을 읽고 병합한 **완성 변경 계획**을 적용한다. 신학적 판단, YAML 병합, 버전 할당, 상태 전이 판단, 인덱스 생성은 도구가 하지 않는다.

계획 JSON은 `operation_id`와 순서 있는 `writes` 배열이다. 각 항목은 레포 상대 `path`, 현재 파일의 `before_sha256`(미존재는 null), UTF-8 `content`, 선택 `kind: artifact`를 가진다. artifact는 기존 파일을 덮어쓸 수 없다. 순서는 산출물 → manifest → 인덱스 → journal이다. 새 작업의 버전 경로는 실행자가 예약하며 같은 저장 재시도에서는 바꾸지 않는다.

```json
{"operation_id":"example-001","writes":[{"path":"outputs/example.md","before_sha256":null,"kind":"artifact","content":"기록 원문\n"}]}
```

```sh
python3 tools/persistence/store.py --root /path/to/workspace --plan /path/to/local-plan.json
```

계획과 영수증은 원문을 포함할 수 있으므로 로컬에서만 보관한다. 영수증은 `outputs/.operations/{operation_id}.json`에 기록된다. 같은 계획을 다시 실행하면 이미 적용된 파일은 건너뛰고 나머지를 쓴다. 다른 변경이 끼었으면 중단한다. 이때 최신 파일을 읽어 병합안을 새로 검토해야 하며 해시만 바꿔 강제 적용하지 않는다. 변경한 계획은 **새 operation_id**를 쓰고 `supersedes: 이전-ID`로 연결한다. 이미 저장된 artifact는 원문·해시를 확인한 뒤 새 계획의 writes에서 제외한다. 변경이 필요한 나머지 파일만 최신 해시와 병합 내용으로 넣는다. 이전 영수증은 수정하지 않는다. 점검자는 새 영수증의 완료 상태와 실제 파일을 대조한 뒤 이전 실패가 복구됐음을 판단한다.

게시 확인으로 기존 산출물의 frontmatter만 바꾸는 계획은 `kind: artifact`를 쓰지 않고 일반 변경으로 제출한다. 제출 전후 본문 바이트가 같은지 실행자가 대조하고 기록한다. 이 도구 자체는 YAML과 본문을 구분하지 않으므로 메타만 바뀐다는 의미 검증을 대신하지 않는다. 결과·인덱스 행과 journal 메모의 중복 제거는 계획 작성자의 책임이다.

정상 종료는 실제 파일별 읽기 대조 후 보고한다. 오류면 영수증의 `completed`와 실제 파일을 대조하여 부분 성공을 알린다. 도구 실행 간에는 루트 단위 잠금을 사용한다. 다른 편집기는 이 잠금을 따르지 않으므로 작업 중 동시 편집을 피하고 충돌 시 병합한다. 프로세스 강제 종료로 `.lock`이 남으면 실행 프로세스가 종료됐는지 확인한 뒤 잠금만 제거하고 같은 계획으로 재개한다. 자동으로 살아 있는 프로세스의 잠금을 지우지 않는다.

검증: `python3 -B -m unittest discover -s tools/persistence/tests`. 테스트는 임시 폴더만 사용하며 인덱스 실패 후 재시도·원문 불변·충돌·경로 이탈을 확인한다. 이 테스트가 자연어 스킬의 상태 판단이나 실제 사용자 효용을 검증하지는 않는다.
