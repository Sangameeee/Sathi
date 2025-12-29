pipeline {
    agent any
    
    environment {
        // Docker Host configuration - UNSET certificate paths
        DOCKER_HOST = '' //fill it as your host
        DOCKER_TLS_VERIFY = ''  // Empty string to completely disable
        DOCKER_CERT_PATH = ''   // Empty to prevent cert lookup
        
        // Docker image details
        DOCKER_IMAGE = 'sancheck30/sathi'
        DOCKER_TAG = '1'
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
                    sh """
                        unset DOCKER_TLS_VERIFY
                        unset DOCKER_CERT_PATH
                        export DOCKER_HOST=${env.DOCKER_HOST}
                        docker build -t ${env.DOCKER_IMAGE}:${env.DOCKER_TAG} .
                    """
                }
            }
        }
        
        stage('Test') {
            steps {
                echo '🧪 Testing Docker image...'
                script {
                    sh """
                        unset DOCKER_TLS_VERIFY
                        unset DOCKER_CERT_PATH
                        export DOCKER_HOST=${env.DOCKER_HOST}
                        
                        docker run -d --name test-container \
                            -e DEBUG=True \
                            -e S_KEY=test-key \
                            -e DATABASE_URL=sqlite:///test.db \
                            ${env.DOCKER_IMAGE}:${env.DOCKER_TAG}
                        
                        sleep 5
                        
                        docker logs test-container
                        
                        if [ "\$(docker inspect test-container --format='{{.State.Running}}')" != "true" ]; then
                            echo "Container failed to start properly"
                            docker stop test-container || true
                            docker rm test-container || true
                            exit 1
                        fi
                        
                        docker stop test-container
                        docker rm test-container
                    """
                    echo "✅ Container starts successfully"
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
                    docker.withRegistry('https://index.docker.io/v1/', env.DOCKER_CREDENTIALS_ID) {
                        sh """
                            unset DOCKER_TLS_VERIFY
                            unset DOCKER_CERT_PATH
                            export DOCKER_HOST=${env.DOCKER_HOST}
                            
                            docker push ${env.DOCKER_IMAGE}:${env.DOCKER_TAG}
                            docker tag ${env.DOCKER_IMAGE}:${env.DOCKER_TAG} ${env.DOCKER_IMAGE}:latest
                            docker push ${env.DOCKER_IMAGE}:latest
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
                echo "✅ Image pushed: ${env.DOCKER_IMAGE}:${env.DOCKER_TAG}"
                echo "To deploy, run: docker pull ${env.DOCKER_IMAGE}:latest && docker-compose up -d"
            }
        }
    }
    
    post {
        success {
            echo '✅ Pipeline completed successfully!'
            echo "Built and pushed: ${env.DOCKER_IMAGE}:${env.DOCKER_TAG}"
        }
        failure {
            echo '❌ Pipeline failed! Check logs above.'
        }
        always {
            echo '🧹 Cleaning up...'
            sh """
                unset DOCKER_TLS_VERIFY
                unset DOCKER_CERT_PATH
                export DOCKER_HOST=${env.DOCKER_HOST}
                docker stop test-container 2>/dev/null || true
                docker rm test-container 2>/dev/null || true
            """
        }
    }
}
