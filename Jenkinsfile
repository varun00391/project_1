pipeline {
    agent any

    environment {
        COMPOSE_FILE = 'docker-compose.yml'
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Stop Previous Containers') {
            steps {
                echo "Stopping running containers..."
                sh 'docker compose down || true'
            }
        }

        stage('Build & Start Services') {
            steps {
                echo "Building and starting containers..."
                sh 'docker compose up -d --build'
            }
        }

        stage('Verify FastAPI') {
            steps {
                echo "Checking FastAPI backend..."
                sh 'curl -f http://localhost:8000/docs || echo "FastAPI not responding"'
            }
        }

        stage('Verify Streamlit') {
            steps {
                echo "Checking Streamlit frontend..."
                sh 'curl -f http://localhost:8501 || echo "Streamlit not responding"'
            }
        }
    }

    post {
        success {
            echo "✅ CI/CD pipeline completed successfully!"
        }
        failure {
            echo "❌ Something went wrong. Cleaning up..."
            sh 'docker compose down'
        }
    }
}
