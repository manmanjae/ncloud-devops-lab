# Local Kubernetes DevOps Lab

Apple Silicon MacBook Air에서 구축한 로컬 Kubernetes 운영 실습 프로젝트
로컬 클러스터에서 배포, 자동 복구, 네트워크, 모니터링 및 CI/CD를 검증

## Environment

- Apple Silicon arm64
- Memory: 8GB
- Container runtime: Colima
- Kubernetes cluster: kind
- Kubernetes: v1.37.0
- Topology: 1 control-plane, 1 worker

## Completed

- [x] Colima 컨테이너 실행 환경 구성
- [x] kind 2노드 Kubernetes 클러스터 구축
- [x] Nginx Pod 삭제 후 약 6초 내 자동 복구 확인
- [x] FastAPI 상태 확인 API 및 자동 테스트 구현
- [x] Non-root·읽기 전용 Docker 이미지 구성
- [x] GitHub Actions 테스트 및 이미지 빌드 CI 구축
- [x] 자체 API를 Kubernetes Deployment로 배포
- [x] Startup·Readiness·Liveness Probe 구성
- [x] Kubernetes SecurityContext 및 리소스 제한 적용
- [ ] Ingress 구성
- [ ] Helm 패키징
- [ ] 모니터링 및 로깅
- [ ] NAVER Cloud NKS 이전

## Self-healing Test

Deployment에서 replicas를 2로 선언한 상태에서 Pod 하나를 수동 삭제
ReplicaSet이 새로운 Pod를 생성했으며 약 6초 만에 Ready 상태로 복구
