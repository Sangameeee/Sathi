pipeline {
    agent any
    
    environment {
        // Docker connection settings
        DOCKER_HOST = 'unix:///var/run/docker.sock'
        DOCKER_TLS_VERIFY = ''
        DOCKER_CERT_PATH = ''
        
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
                    docker.build("${env.DOCKER_IMAGE}:${env.DOCKER_TAG}", ".")
                }
            }
        }
        
        stage('Test') {
            steps {
                echo '🧪 Testing Docker image...'
                script {
                    def testContainer = docker.image("${env.DOCKER_IMAGE}:${env.DOCKER_TAG}").run(
                        '-e DEBUG=True ' +
                        '-e S_KEY=test-key ' +
                        '-e DATABASE_URL=sqlite:///test.db'
                    )
                    
                    // Wait for container to initialize
                    sleep 5
                    
                    // Get container logs
                    sh "docker logs ${testContainer.id}"
                    
                    // Check if container is healthy
                    def containerStatus = sh(
                        script: "docker inspect ${testContainer.id} --format='{{.State.Running}}'",
                        returnStdout: true
                    ).trim()
                    
                    if (containerStatus != "true") {
                        error("Container failed to start properly")
                    }
                    
                    // Clean up test container
                    testContainer.stop()
                    
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
                        def image = docker.image("${env.DOCKER_IMAGE}:${env.DOCKER_TAG}")
                        image.push()
                        
                        // Also push as latest
                        sh "docker tag ${env.DOCKER_IMAGE}:${env.DOCKER_TAG} ${env.DOCKER_IMAGE}:latest"
                        docker.image("${env.DOCKER_IMAGE}:latest").push()
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
                docker stop test-container 2>/dev/null || true
                docker rm test-container 2>/dev/null || true
                docker logout 2>/dev/null || true
            """
        }
    }
}
