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
- [x] Deployment를 이용한 Nginx Pod 2개 배포
- [x] ClusterIP Service 구성
- [x] Readiness/Liveness Probe 설정
- [x] Pod 삭제 후 자동 복구 확인
- [ ] 애플리케이션 컨테이너 배포
- [ ] Ingress 구성
- [ ] Helm 패키징
- [ ] CI/CD 구축
- [ ] 모니터링 및 로깅
- [ ] NAVER Cloud NKS 이전

## Self-healing Test

Deployment에서 replicas를 2로 선언한 상태에서 Pod 하나를 수동 삭제
ReplicaSet이 새로운 Pod를 생성했으며 약 6초 만에 Ready 상태로 복구
