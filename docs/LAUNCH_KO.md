# oh-my-skills 한국어 런칭 메모

## 한 줄 소개

oh-my-skills는 내 컴퓨터에 흩어진 Codex, Claude, Agent Skills를 한 번에 보고
관리하는 로컬 GUI입니다.

## 짧은 소개

AI 코딩 에이전트를 여러 개 쓰다 보면 `SKILL.md`가 여기저기 쌓입니다.
`~/.codex/skills`, `~/.claude/skills`, `~/.agents/skills`, 플러그인 캐시까지
분산되면 내가 어떤 스킬을 만들었는지도 기억이 안 납니다.

oh-my-skills는 이 문제를 로컬 대시보드로 해결합니다.

- 내 PC의 스킬 목록 스캔
- Codex/Claude/Agents 스킬 통합 보기
- 중복 스킬 탐지
- 사용자 스킬 편집
- 저장 전 자동 백업
- 영구 삭제 대신 보관
- 시스템/플러그인 스킬은 읽기 전용
- 계정, 서버, 텔레메트리 없음

## 사용법

```bash
git clone https://github.com/AIjunja/-oh-my-skills.git
cd oh-my-skills
python -m skill_ledger gui
```

브라우저에서 열기:

```text
http://127.0.0.1:8765/
```

## 내 SNS CTA 넣기

```powershell
$env:OH_MY_SKILLS_CTA_LABEL = "제작자 구독하기"
$env:OH_MY_SKILLS_CTA_URL = "https://www.threads.com/@ai_jjuun"
$env:OH_MY_SKILLS_CTA_NOTE = "Threads, Instagram, YouTube, GitHub에서 제작자를 구독해 주세요."
python -m skill_ledger gui
```

## 설치형 사용

```bash
pipx install git+https://github.com/AIjunja/-oh-my-skills.git
oh-my-skills gui
```

## 한국어 홍보글 초안

AI 에이전트 스킬을 많이 만들다 보니 이제 뭐가 어디 있는지도 모르겠어서 만들었습니다.

oh-my-skills는 Codex, Claude, Agent Skills를 한 번에 관리하는 로컬 GUI입니다.

- `~/.codex/skills`, `~/.claude/skills`, `~/.agents/skills` 자동 스캔
- 중복 스킬 탐지
- `SKILL.md` 편집
- 저장 전 백업
- 삭제 대신 보관
- 시스템/플러그인 스킬은 읽기 전용
- 서버 없음, 계정 없음, 텔레메트리 없음

실행:

```bash
python -m skill_ledger gui
```

오픈소스: https://github.com/AIjunja/-oh-my-skills

제작자 채널:

- Threads: https://www.threads.com/@ai_jjuun
- Instagram: https://www.instagram.com/ai_jjuun/
- YouTube: https://www.youtube.com/@AI%EC%AD%8C
- GitHub: https://github.com/AIjunja
