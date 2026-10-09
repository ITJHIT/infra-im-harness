# infra-im-harness

인프라 사업성 검토를 위한 **검증 게이트** 모음.

AI는 그럴듯한 IM을 몇 분 만에 쓴다. 문제는 그럴듯함이 검증이 아니라는 점이다.
이 저장소의 스킬들은 IM을 대신 써 주지 않는다. 초안의 숫자와 논리를 공격해서, 작성자가 설명할 수 없는 문장이 남지 않게 한다.

```
초안 ──▶ 게이트가 공격 ──▶ 작성자가 판정 ──▶ 고친 뒤 다시 게이트
```

## 게이트

| 스킬 | 묻는 질문 |
|---|---|
| [`im-skeleton`](.claude/skills/im-skeleton/SKILL.md) | 어떤 장이 어떤 게이트를 통과해야 하나 (빈칸만 만든다) |
| [`deal-thesis-gate`](.claude/skills/deal-thesis-gate/SKILL.md) | 이 수익은 누가, 왜 지불하나. 빠진 비용은 없나 |
| [`assumption-trace`](.claude/skills/assumption-trace/SKILL.md) | 이 숫자의 1차 출처와 기준연도는 무엇인가 |
| [`stress-gate`](.claude/skills/stress-gate/SKILL.md) | 기준 케이스를 골라낸 것은 아닌가. 하방에서 대출이 버티나 |
| [`model-audit`](.claude/skills/model-audit/SKILL.md) | 같은 가정으로 다시 계산해도 같은 답이 나오나 |
| [`risk-allocation-matrix`](.claude/skills/risk-allocation-matrix/SKILL.md) | 리스크마다 누가 떠안나. 주인 없는 리스크는 무엇인가 |
| [`im-parity`](.claude/skills/im-parity/SKILL.md) | IM 본문, 모델, 가정표의 숫자가 서로 맞나 |

각 스킬 끝에는 **이 스킬이 막는 실사고** 항목이 있다. 가상의 예시가 아니라, 샘플 프로젝트를 만들다가 실제로 저지른 실수다.

## 샘플: 1MW 지상형 태양광

[`samples/solar-1mw/`](samples/solar-1mw/) — 공개 자료만으로 만든 가상 프로젝트.

- [`IM.md`](samples/solar-1mw/IM.md) — 게이트 통과 상태가 표시된 IM 초안
- [`assumptions.md`](samples/solar-1mw/assumptions.md) — 모든 입력값의 1차 출처, 출처 간 충돌과 처리 기록
- [`gate-log.md`](samples/solar-1mw/gate-log.md) — 게이트가 잡은 실수와 조치
- [`model_check.py`](samples/solar-1mw/model_check.py) — 엑셀 모델 검산용 독립 재계산

게이트가 바꾼 결론 하나:

> 첫 모델은 "최저 DSCR은 성능저하가 쌓인 15년 차 근처"라고 답했다. 실제 은행 상품을 확인하니 원금균등 상환만 허용됐고, 그 구조에서는 이자가 가장 큰 **1년 차**가 가장 빠듯했다. 같은 발전소에서 상환 구조만 바꿔도 Equity IRR은 16.1%와 18.3%로 갈리고, Project IRR은 8.6%로 그대로다.

## 사용법

[Claude Code](https://claude.com/claude-code)에서 이 저장소를 열면 `.claude/skills/`의 스킬이 자동으로 인식된다.

```bash
python samples/solar-1mw/model_check.py
```

## 원칙

- 공개 자료로 만든 가상 프로젝트만 다룬다.
- 엑셀 모델은 사람이 직접 만든다. 코드는 그것을 검산할 뿐이다.
- 출처가 충돌하면 고르지 않고 뺀다.
