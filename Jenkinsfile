
pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    environment {
        IMAGE_NAME = 'taskflow'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                sh 'git rev-parse --short HEAD'
            }
        }

        stage('Run Automated Tests') {
            steps {
                sh '''
                    docker run --rm \
                      -v "$WORKSPACE:/src:ro" \
                      python:3.12-slim \
                      sh -ec '
                        mkdir -p /tmp/taskflow &&
                        cp -a /src/. /tmp/taskflow/ &&
                        cd /tmp/taskflow &&
                        python -m pip install --no-cache-dir -r requirements-dev.txt &&
                        python -m pytest -v
                      '
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build --pull \
                      -t taskflow:${BUILD_NUMBER} .
                    docker tag taskflow:${BUILD_NUMBER} taskflow:latest
                '''
            }
        }

        stage('Container Smoke Test') {
            steps {
                sh '''
                    set -eu

                    CONTAINER_NAME="taskflow-smoke-${BUILD_NUMBER}"

                    cleanup() {
                        docker rm -f "$CONTAINER_NAME" \
                          >/dev/null 2>&1 || true
                    }
                    trap cleanup EXIT

                    docker run -d \
                      --name "$CONTAINER_NAME" \
                      taskflow:${BUILD_NUMBER}

                    for attempt in $(seq 1 20); do
                        if docker exec "$CONTAINER_NAME" \
                          python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=2)" \
                          >/dev/null 2>&1; then
                            echo "Application health check passed"
                            exit 0
                        fi

                        sleep 2
                    done

                    docker logs "$CONTAINER_NAME"
                    echo "Application smoke test failed"
                    exit 1
                '''
            }
        }

        stage('Deploy Application') {
            steps {
                sh '''
                    set -eu

                    cd "$WORKSPACE"

                    docker compose \
                      --env-file /etc/taskflow/.env \
                      -p taskflow \
                      --profile monitoring \
                      up -d --no-build

                    echo "Waiting for TaskFlow to become healthy..."

                    for attempt in $(seq 1 30); do
                        STATUS=$(docker inspect \
                          --format='{{.State.Health.Status}}' \
                          taskflow-app 2>/dev/null || true)

                        if [ "$STATUS" = "healthy" ]; then
                            echo "TaskFlow deployment successful"
                            exit 0
                        fi

                        sleep 5
                    done

                    docker compose \
                      --env-file /etc/taskflow/.env \
                      -p taskflow \
                      --profile monitoring \
                      ps

                    docker logs taskflow-app
                    echo "Deployment health check failed"
                    exit 1
                '''
            }
        }
    }

    post {
        success {
            echo 'CI passed: tests, image build, and smoke test.'
        }

        failure {
            echo 'CI failed. Check the failed stage and console output.'
        }
    }
}
