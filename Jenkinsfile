pipeline {
    agent any

    environment {
        PATH = PATH   = "/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin" //"/usr/local/bin:$PATH"
        DOCKER = 'usr/local/bin/docker'  // /usr/local/bin/docker
    }

    stages {

        stage {
            steps {
                sh 'echo "PATH=[$PATH]"'
                sh 'which docker || echo "docker not found"'
        }
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Stop Previous Containers') {
            steps {
                echo '🛑 Stopping running containers...'
                sh "${DOCKER} compose down || true"
            }
        }

        stage('Build & Start Services') {
            steps {
                echo '🚀 Building and starting containers...'
                sh "${DOCKER} compose up -d --build"
            }
        }

        stage('Verify FastAPI') {
            steps {
                echo '🔍 Verifying FastAPI is up...'
                sh 'curl -s http://localhost:8000/docs'
            }
        }

        stage('Verify Streamlit') {
            steps {
                echo '🔍 Verifying Streamlit is up...'
                sh 'curl -s http://localhost:8501'
            }
        }
    }

    post {
        failure {
            echo '❌ Something went wrong. Cleaning up...'
            sh "${DOCKER} compose down || true"
        }
    }
}
