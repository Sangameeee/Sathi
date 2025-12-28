pipeline {
    agent any
    
    environment {
        // Docker Hub details
        DOCKER_IMAGE = "sancheck30/sathi"
        DOCKER_TAG = "${BUILD_NUMBER}"
        DOCKER_CREDENTIALS_ID = 'dockerhub-credentials'
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo '📥 Checking out code from GitHub...'
                checkout scm
            }
        }
        
       stage('Build') {
            steps {
                echo "🏗️ Building Docker image..."
                script {
                    docker.build("sancheck30/sathi:1", ".")
                }
            }
        }
        
        stage('Test') {
            steps {
                echo '🧪 Testing Docker image...'
                script {
                    sh """
                        # Quick smoke test - check if image was built
                        docker images | grep ${DOCKER_IMAGE}
                        
                        # Test container starts successfully
                        docker run --rm -d \
                          --name test-container \
                          -e DEBUG=True \
                          -e S_KEY=test-key \
                          -e DATABASE_URL=sqlite:///test.db \
                          ${DOCKER_IMAGE}:${DOCKER_TAG}
                        
                        # Wait a bit for startup
                        sleep 10
                        
                        # Check if container is still running
                        docker ps | grep test-container || (echo "Container failed to start" && exit 1)
                        
                        # Show logs
                        docker logs test-container
                        
                        # Stop test container
                        docker stop test-container
                        
                        echo "✅ Container starts successfully"
                    """
                }
            }
        }
        
        stage('Push') {
            when {
                branch 'main'
            }
            steps {
                echo '📤 Pushing to Docker Hub...'
                script {
                    withCredentials([usernamePassword(
                        credentialsId: "${DOCKER_CREDENTIALS_ID}",
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )]) {
                        sh """
                            echo \${DOCKER_PASS} | docker login -u \${DOCKER_USER} --password-stdin
                            docker push ${DOCKER_IMAGE}:${DOCKER_TAG}
                            docker push ${DOCKER_IMAGE}:latest
                            docker logout
                        """
                    }
                }
            }
        }
        
        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                echo '🚀 Deployment Info'
                echo "✅ Image pushed: ${DOCKER_IMAGE}:${DOCKER_TAG}"
                echo "To deploy, run: docker pull ${DOCKER_IMAGE}:latest && docker-compose up -d"
            }
        }
    }
    
    post {
        success {
            echo '✅ Pipeline completed successfully!'
            echo "Built and pushed: ${DOCKER_IMAGE}:${DOCKER_TAG}"
        }
        failure {
            echo '❌ Pipeline failed! Check logs above.'
        }
        always {
            echo '🧹 Cleaning up...'
            sh """
                docker stop test-container 2>/dev/null || true
                docker rm test-container 2>/dev/null || true
                docker logout 2>/dev/null || true
            """
        }
    }
}
