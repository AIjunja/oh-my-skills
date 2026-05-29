# oh-my-skills

[English README](README.md)

## 데모

<video src="docs/assets/oh-my-skills-demo.mp4" controls muted playsinline width="100%"></video>

GitHub에서 영상이 바로 보이지 않으면 아래 파일을 열어주세요.
[docs/assets/oh-my-skills-demo.mp4](docs/assets/oh-my-skills-demo.mp4)

Codex, Claude, Agent Skills의 `SKILL.md` 폴더를 한 번에 관리하는 로컬 GUI/CLI입니다.

oh-my-skills가 답하는 질문은 아주 단순합니다.

> "내 컴퓨터에 어떤 스킬이 깔려 있고, 어떤 스킬을 안전하게 편집할 수 있지?"

로컬 스킬 디렉터리를 스캔하고, 중복을 보여주고, 사용자 소유 스킬을 안전하게 편집할 수 있게 해줍니다. 시스템/플러그인 스킬은 읽기 전용으로 둡니다.

## 기능

- 로컬 브라우저 GUI: 검색, 필터링, 확인, 편집, 생성, 보관
- 영어/한국어 GUI 토글
- 같은 모노 README 스타일을 유지하는 라이트/다크 GUI 테마 토글
- CLI 인벤토리: Markdown 또는 JSON 리포트 내보내기
- Codex, Claude, Agents, 플러그인 캐시 사이의 중복 스킬 탐지
- 안전한 편집: 저장 전 `SKILL.md` 자동 백업
- 안전한 정리: 영구 삭제 대신 보관 폴더로 이동
- 로컬 우선: `127.0.0.1`에서 실행, 계정/클라우드 동기화/DB/텔레메트리 없음
- 가벼운 의존성: Python 표준 라이브러리만 사용

## 기본 스캔 위치

| 출처 | 경로 | 편집 |
| --- | --- | --- |
| `codex-user` | `~/.codex/skills` | 가능 |
| `claude-user` | `~/.claude/skills` | 가능 |
| `agents-user` | `~/.agents/skills` | 가능 |
| `codex-system` | `~/.codex/skills/.system` | 읽기 전용 |
| `plugin-cache` | `~/.codex/plugins/cache` | 읽기 전용 |

## 빠른 시작

### 소스에서 실행

```bash
git clone https://github.com/AIjunja/oh-my-skills.git
cd oh-my-skills
python -m skill_ledger gui
```

터미널에 표시되는 로컬 주소를 브라우저에서 여세요. 기본 주소는 다음과 같습니다.

```text
http://127.0.0.1:8765/
```

`8765` 포트가 사용 중이면 다음 빈 포트를 자동으로 찾습니다.

### GitHub에서 설치

공개 저장소로 올린 뒤에는 이렇게 설치할 수 있습니다.

```bash
pipx install git+https://github.com/AIjunja/oh-my-skills.git
oh-my-skills gui
```

`pipx` 없이 설치하려면:

```bash
python -m pip install git+https://github.com/AIjunja/oh-my-skills.git
oh-my-skills gui
```

기존 호환을 위해 `skill-ledger` 명령도 alias로 남아 있습니다.

### 개발용 설치

```bash
git clone https://github.com/AIjunja/oh-my-skills.git
cd oh-my-skills
python -m pip install -e .
oh-my-skills gui
```

## CLI 사용법

Markdown 인벤토리 생성:

```bash
python -m skill_ledger scan --format markdown --out inventory/skills.md
```

JSON 생성:

```bash
python -m skill_ledger scan --format json --out inventory/skills.json
```

중복과 메타데이터 경고 확인:

```bash
python -m skill_ledger doctor
```

특정 폴더만 스캔:

```bash
python -m skill_ledger scan \
  --root ~/.codex/skills \
  --root ~/.claude/skills \
  --format markdown
```

## GUI 사용법

```bash
python -m skill_ledger gui
```

GUI에서 할 수 있는 일:

- 발견된 모든 스킬 보기
- 이름, 설명, 경로, 출처로 검색
- 출처별 필터링
- `SKILL.md` 확인
- 사용자 소유 스킬 편집
- Codex, Claude, Agents용 새 스킬 생성
- 필요 없는 사용자 스킬 보관
- 인벤토리 리포트 내보내기
- EN/KR 언어 전환
- 라이트/다크 테마 전환

## 브라우저 CTA 설정

상단과 사이드바에 제작자 구독 CTA가 표시됩니다. 기본 문구는 `제작자 구독하기`입니다.

기본으로 표시되는 채널:

- [Threads](https://www.threads.com/@ai_jjuun)
- [Instagram](https://www.instagram.com/ai_jjuun/)
- [YouTube](https://www.youtube.com/@AI%EC%AD%8C)
- [GitHub](https://github.com/AIjunja)

대표 CTA 문구나 URL은 환경변수로 바꿀 수 있습니다.

```bash
OH_MY_SKILLS_CTA_LABEL="제작자 구독하기" \
OH_MY_SKILLS_CTA_URL="https://www.threads.com/@ai_jjuun" \
OH_MY_SKILLS_CTA_NOTE="Threads, Instagram, YouTube, GitHub에서 제작자를 구독해 주세요." \
python -m skill_ledger gui
```

Windows PowerShell:

```powershell
$env:OH_MY_SKILLS_CTA_LABEL = "제작자 구독하기"
$env:OH_MY_SKILLS_CTA_URL = "https://www.threads.com/@ai_jjuun"
$env:OH_MY_SKILLS_CTA_NOTE = "Threads, Instagram, YouTube, GitHub에서 제작자를 구독해 주세요."
python -m skill_ledger gui
```

## 안전 모델

oh-my-skills는 보수적으로 동작합니다.

- `codex-system`, `plugin-cache` 스킬은 읽기 전용입니다.
- 사용자 스킬은 알려진 사용자 스킬 루트 안에서만 편집됩니다.
- 저장 시 `~/.oh-my-skills/backups` 아래에 백업을 만듭니다.
- 보관 시 `~/.oh-my-skills/archive`로 스킬 폴더를 이동합니다.
- 인벤토리 리포트에는 로컬 경로와 프롬프트 내용이 포함될 수 있으므로 `inventory/`는 기본적으로 Git에서 제외됩니다.

## Agent Skill로 사용하기

이 저장소는 루트에 `SKILL.md`를 포함하고 있어서 Agent Skill로도 설치할 수 있습니다.

Codex:

```bash
git clone https://github.com/AIjunja/oh-my-skills.git ~/.codex/skills/oh-my-skills
```

Claude:

```bash
git clone https://github.com/AIjunja/oh-my-skills.git ~/.claude/skills/oh-my-skills
```

Windows PowerShell:

```powershell
git clone https://github.com/AIjunja/oh-my-skills.git "$env:USERPROFILE\.codex\skills\oh-my-skills"
git clone https://github.com/AIjunja/oh-my-skills.git "$env:USERPROFILE\.claude\skills\oh-my-skills"
```

## 관련 프로젝트

- [`openai/skills`](https://github.com/openai/skills): 공식 Codex 스킬 카탈로그
- [`luongnv89/asm`](https://github.com/luongnv89/asm): 범용 스킬 매니저 CLI/TUI
- [`siddhantparadox/codexmanager`](https://github.com/siddhantparadox/codexmanager): Codex 데스크톱 매니저

oh-my-skills는 더 작고 명확한 목적에 집중합니다. 이미 내 컴퓨터에 설치된 스킬을 로컬에서 보고, 정리하고, 안전하게 편집하는 도구입니다.

## 라이선스

MIT
