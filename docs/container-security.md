# 컨테이너 보안 검증 (Container Security Validation)

## 개요

FastAPI 애플리케이션을 컨테이너로 실행하고, 최소 권한 원칙에 따라
파일시스템과 프로세스 권한을 제한했습니다. 설정값 확인뿐만 아니라
컨테이너 내부에서 쓰기 작업을 수행하여 보안 정책이 실제로 적용되는지 검증했습니다.

## 이미지 정보

- 이미지: `devops-lab-api:0.1.0`
- 기반 이미지: `python:3.14.7-slim-bookworm`
- 애플리케이션 포트: `8000`
- 실행 사용자: `10001:10001`

## 적용한 보안 정책

| 보안 항목 | 설정 | 검증 결과 |
|---|---|---|
| 일반 사용자 실행(Non-root) | UID/GID `10001:10001` | 통과 |
| 루트 파일시스템 읽기 전용 | `--read-only` | 통과 |
| Linux Capability 제거 | `--cap-drop ALL` | 통과 |
| 추가 권한 상승 차단 | `no-new-privileges:true` | 통과 |
| 임시 저장공간 제한 | `/tmp`에 tmpfs 마운트 | 통과 |
| 애플리케이션 상태 확인 | `/health` endpoint | 통과 |

## 검증 과정

### 1. 일반 사용자 실행 확인

컨테이너 내부 프로세스가 root가 아닌 전용 사용자로 실행되는지 확인했습니다.

```bash
docker exec devops-lab-api id
