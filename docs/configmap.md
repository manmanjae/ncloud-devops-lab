# Kubernetes ConfigMap 환경설정 분리

## 목적

애플리케이션 설정을 컨테이너 이미지와 분리하여 환경마다 이미지를 다시
빌드하지 않고 설정값을 관리할 수 있도록 ConfigMap을 적용했습니다.

## 구성

`devops-lab-api-config` ConfigMap에서 다음 값을 관리합니다.

| 환경변수 | 값 | 용도 |
|---|---|---|
| `APP_VERSION` | `0.2.0` | 배포 버전 표시 |
| `APP_MESSAGE` | `Hello from Kubernetes ConfigMap` | 루트 API 응답 메시지 |

Deployment에서는 `envFrom.configMapRef`를 사용해 ConfigMap의 모든 값을
컨테이너 환경변수로 주입합니다.

## 애플리케이션 처리

FastAPI 애플리케이션은 `APP_MESSAGE` 환경변수를 읽으며, 값이 없을 경우
`Hello from Kubernetes`를 기본값으로 사용합니다.

환경변수의 유무에 따른 동작을 pytest로 검증했으며 전체 5개 테스트가
통과했습니다.

## 배포 결과

- 컨테이너 이미지: `devops-lab-api:0.2.0`
- Deployment Ready: `2/2`
- Pod Restart Count: `0`
- 두 Pod 모두 worker 노드에서 실행
- 롤링 업데이트 정상 완료

## 검증 결과

Pod에 주입된 환경변수:

```text
APP_VERSION=0.2.0
APP_MESSAGE=Hello from Kubernetes ConfigMap

```

API 응답:

```json
{
  "service": "devops-lab-api",
  "message": "Hello from Kubernetes ConfigMap"
}
```

버전 API 응답에서 `0.2.0` 적용도 확인했습니다.

## 운영 시 주의사항

ConfigMap은 일반 설정값을 관리하는 용도이며 비밀번호, API 키와 같은
민감정보는 Secret 또는 외부 비밀 관리 시스템을 사용해야 합니다.

환경변수로 주입한 ConfigMap 값은 실행 중인 컨테이너에 자동 반영되지
않으므로 설정 변경 후 Pod를 새로 생성하거나 Deployment를 재시작해야 합니다.
