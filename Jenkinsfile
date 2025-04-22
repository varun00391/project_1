pipeline {
    agent any

    environment {
        DOCKER_CLI_EXPERIMENTAL = 'enabled'  // Set the environment variable here
    }

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

        
        // stage('Build and Run') {
        //     steps {
        //         // Set DOCKER_CLI_EXPERIMENTAL only for this step
        //         sh 'export DOCKER_CLI_EXPERIMENTAL=enabled && /usr/local/bin/docker-compose down --remove-orphans'
        //         sh 'export DOCKER_CLI_EXPERIMENTAL=enabled && /usr/local/bin/docker-compose up -d --build'

        //     }
        // }

        stage('Build and Run') {
            steps {
                echo 'Stopping existing containers...'
                sh 'export DOCKER_CLI_EXPERIMENTAL=enabled && /usr/local/bin/docker-compose down --remove-orphans'

                echo 'Building and starting containers...'
                sh 'export DOCKER_CLI_EXPERIMENTAL=enabled && /usr/local/bin/docker-compose up -d --build || docker-compose logs'
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
        echo 'Build completed — not cleaning up so containers stay up.'
    }
}

}