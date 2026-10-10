# 게이트 로그 — 1MW 지상형 태양광

| 날짜 | 게이트 | 판정 | 발견 → 조치 |
|---|---|---|---|
| 2026-10-01 | assumption-trace | FAIL → PASS | 설비비가 2023년 값(1,416)이었다. 원문 <표 3-6>을 열어 2024년 값(1,281)으로 교체 |
| 2026-10-01 | assumption-trace | FAIL → PASS | 검색 요약의 "육지 첫 출력제어 2026년"을 원문과 대조 → 2024년 4월로 정정 |
| 2026-10-01 | deal-thesis-gate | FAIL → 조건부 | 토지 임차료·법인세 누락 → 추가. 개발비는 아직 0 🔴 → IRR을 '상한'으로 표기 |
| 2026-10-01 | model-audit | FAIL → PASS | 원리금균등 상환 가정 → 실제 상품은 원금균등만 허용. 구조 교체 후 재계산 |
| 2026-10-01 | stress-gate | 진행 중 | 최저 DSCR 위치를 15년 차 → 1년 차로 정정. 복합 하방 시나리오 DSCR 1.06. 대주단 DSCR 기준의 출처는 미확보 |
| 2026-10-01 | risk-allocation-matrix | 🔴 1건 | 출력제어 손실 보상 기준 미정 → 사업자 전액 부담으로 가정 |
| 2026-10-01 | im-parity | FAIL → PASS | 이용률 변경 후 본문에 "15% → 1,314MWh", "1%p ≈ 2.9%p"가 남아 있었음 → 정정 |
| 2026-10-10 | assumption-trace | FAIL → PASS | [infra-assumption-feed](https://github.com/ITJHIT/infra-assumption-feed)로 SMP를 전력거래소 원표와 대조 → 2차 출처(업계 블로그)의 8월 148.91·9월 116.74가 원표 148.39·119.02와 불일치. 원표 값으로 교체, '한 달 31원 하락'을 '29.37원'으로 정정 |
| — | model-audit (엑셀) | 대기 | 작성자가 직접 만드는 엑셀 모델과 `model_check.py` 대조 전 |
