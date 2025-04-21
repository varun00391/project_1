pipeline {
    agent any

    environment {
        DOCKER = 'usr/local/bin/docker'  // /usr/local/bin/docker
    }

    stages {
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
