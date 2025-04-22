pipeline {
    agent any

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Generate .env') {
            steps {
                withCredentials([string(credentialsId: 'GROQ_API_KEY', variable: 'GROQ_KEY')]) {
                    writeFile file: '.env', text: "GROQ_API_KEY=${GROQ_KEY}"
                }
            }
        }

        stage('Build and Run') {
            steps {
                sh '''
                    docker-compose down --remove-orphans
                    docker-compose up --build -d
                '''
            }
        }

        stage('Health Check') {
            steps {
                script {
                    def response = sh(script: 'curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/docs', returnStdout: true).trim()
                    if (response != '200') {
                        error "FastAPI app is not healthy (status code: ${response})"
                    }
                }
            }
        }
    }

    post {
        always {
            echo 'Cleaning up...'
            sh 'docker-compose down --remove-orphans'
            sh 'rm -f .env'
        }
    }
}
