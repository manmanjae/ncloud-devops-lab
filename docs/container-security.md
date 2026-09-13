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

```

결과:

```text
uid=10001(app) gid=10001(app) groups=10001(app)
```

### 2. 애플리케이션 디렉터리 쓰기 차단 확인

컨테이너의 `/app` 디렉터리에 파일 생성을 시도했습니다.

```bash
docker exec devops-lab-api sh -c 'touch /app/write-test'
```

예상대로 읽기 전용 파일시스템 오류가 발생했습니다.

```text
touch: cannot touch '/app/write-test': Read-only file system
```

이를 통해 애플리케이션 프로세스가 침해되더라도 실행 코드나 설정 파일을
임의로 변경하기 어렵도록 제한된 것을 확인했습니다.

### 3. 임시 디렉터리 쓰기 확인

애플리케이션이 임시 파일을 생성할 수 있도록 `/tmp`만 tmpfs로 제공했습니다.

```bash
docker exec devops-lab-api sh -c \
  'touch /tmp/write-test && ls -l /tmp/write-test'
```

결과:

```text
-rw-r--r-- 1 app app 0 /tmp/write-test
```

애플리케이션 영역은 보호하면서 필요한 임시 쓰기 작업은 허용됨을 확인했습니다.

### 4. 컨테이너 설정 확인

```bash
docker inspect \
  --format 'User={{.Config.User}} ReadOnly={{.HostConfig.ReadonlyRootfs}} CapDrop={{json .HostConfig.CapDrop}} SecurityOpt={{json .HostConfig.SecurityOpt}}' \
  devops-lab-api
```

결과:

```text
User=10001:10001 ReadOnly=true CapDrop=["ALL"] SecurityOpt=["no-new-privileges:true"]
```

## 결론

컨테이너를 root 권한 없이 실행하고 애플리케이션 파일시스템을 읽기 전용으로
제한했습니다. 모든 Linux Capability를 제거하고 추가 권한 상승을 차단했으며,
임시 쓰기 작업은 메모리 기반 `/tmp` 영역에서만 허용했습니다.

향후 동일한 정책을 Kubernetes의 `securityContext`,
`readOnlyRootFilesystem`, `capabilities`, `emptyDir` 설정으로 이전할 예정입니다.
