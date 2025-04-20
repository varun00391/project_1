pipeline {
    agent any

    environment {
        FASTAPI_URL = 'http://localhost:8000'
        STREAMLIT_URL = 'http://localhost:8501'
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
                sh 'docker compose down || true'
            }
        }

        stage('Build & Start Services') {
            steps {
                echo '🚀 Building and starting containers...'
                sh 'docker compose up -d --build'
            }
        }

        stage('Verify FastAPI') {
            steps {
                echo '🔍 Checking FastAPI health...'
                sh '''
                sleep 5
                if curl --fail $FASTAPI_URL/docs; then
                    echo "✅ FastAPI is running."
                else
                    echo "❌ FastAPI is not reachable!"
                    exit 1
                fi
                '''
            }
        }

        stage('Verify Streamlit') {
            steps {
                echo '🔍 Checking Streamlit health...'
                sh '''
                sleep 5
                if curl --fail $STREAMLIT_URL; then
                    echo "✅ Streamlit is running."
                else
                    echo "❌ Streamlit is not reachable!"
                    exit 1
                fi
                '''
            }
        }
    }

    post {
        failure {
            echo '❌ Something went wrong. Cleaning up...'
            sh 'docker compose down || true'
        }
        success {
            echo '✅ App deployed successfully!'
        }
    }
}

