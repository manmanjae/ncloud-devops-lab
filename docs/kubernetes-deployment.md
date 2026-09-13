# Kubernetes 애플리케이션 배포 및 보안 검증

## 개요

Apple Silicon MacBook Air에서 Colima와 kind를 사용해 로컬 Kubernetes
클러스터를 구성하고, 직접 제작한 FastAPI 애플리케이션을 배포했습니다.

단순히 Pod를 실행하는 데 그치지 않고 상태 확인 Probe, 리소스 제한,
최소 권한 보안 정책과 메모리 기반 임시 저장공간을 적용했습니다.

## 클러스터 구성

- Kubernetes: v1.37.0
- control-plane: 1개
- worker: 1개
- 애플리케이션 Pod: 2개
- Service 유형: ClusterIP
- 컨테이너 이미지: `devops-lab-api:0.1.0`

## 배포 전략

Deployment의 replica를 2개로 설정했습니다.

RollingUpdate 전략에는 다음 정책을 적용했습니다.

- `maxUnavailable: 0`
- `maxSurge: 1`
- `revisionHistoryLimit: 3`

업데이트 중 기존 Pod가 중단되지 않도록 유지하면서 새로운 Pod를 먼저
생성하고, 최근 배포 이력 3개를 보존하도록 구성했습니다.

## 상태 확인 Probe

| Probe | 경로 | 목적 |
|---|---|---|
| Startup Probe | `/health` | 애플리케이션 시작 완료 확인 |
| Readiness Probe | `/ready` | 요청을 받을 준비 상태 확인 |
| Liveness Probe | `/health` | 프로세스 정상 동작 확인 |

검증 결과 두 Pod 모두 `Ready=True`, `ContainersReady=True` 상태가 됐으며
재시작 없이 정상 운영됐습니다.

## 리소스 제한

각 Pod에 다음 리소스를 설정했습니다.

| 구분 | CPU | Memory |
|---|---:|---:|
| Request | 50m | 64Mi |
| Limit | 250m | 128Mi |

이를 통해 스케줄러가 필요한 최소 리소스를 판단할 수 있고,
하나의 컨테이너가 과도한 리소스를 사용하는 것을 제한했습니다.

## 컨테이너 보안 정책

다음 `securityContext` 정책을 적용했습니다.

- UID/GID `10001:10001`의 일반 사용자로 실행
- root 사용자 실행 차단
- 권한 상승 차단
- 모든 Linux Capability 제거
- 루트 파일시스템 읽기 전용
- `RuntimeDefault` seccomp 프로필 사용
- Service Account 토큰 자동 마운트 차단
- `/tmp`만 16Mi 크기의 메모리 기반 `emptyDir`로 제공

컨테이너 내부 사용자 확인 결과:

```text
uid=10001(app) gid=10001(app) groups=10001(app)

```

## Service 구성

애플리케이션 Pod 앞에 `ClusterIP` Service를 구성했습니다.

- Service port: `80`
- Container target port: `8000`
- selector: `app.kubernetes.io/name=devops-lab-api`

ClusterIP는 클러스터 내부에서만 접근할 수 있으므로 로컬 검증에는
`kubectl port-forward`를 사용했습니다.

```bash
kubectl port-forward \
  -n devops-lab \
  service/devops-lab-api \
  8000:80
```

## 배포 검증 결과

```text
Deployment Ready: 2/2
Available Pods: 2
Pod Restart Count: 0
Ready: True
ContainersReady: True
PodScheduled: True
SeccompProfile: RuntimeDefault
```

두 Pod 모두 worker 노드에서 실행됐으며 startup, readiness, liveness Probe를
통과했습니다.

## 현재 구성의 제약 사항

현재 클러스터에는 worker 노드가 하나만 있으므로 Pod가 2개여도 두 Pod가
동일한 worker 노드에 배치됩니다. 따라서 Pod 장애에는 대응할 수 있지만
worker 노드 자체의 장애를 견디는 고가용성 구성은 아닙니다.

향후 멀티 worker 클러스터와 Pod Anti-Affinity 또는 Topology Spread
Constraints를 적용하여 노드 단위 장애 대응을 실습할 예정입니다.

## 향후 개선 계획

- Ingress Controller를 통한 외부 접근
- ConfigMap을 이용한 환경설정 분리
- PodDisruptionBudget 적용
- Helm Chart 작성
- Prometheus 및 Grafana 모니터링
- NAVER Cloud NKS 환경으로 이전
