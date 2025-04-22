pipeline {
    agent any

    environment {
        // Prepend /usr/local/bin so Jenkins can find docker
        PATH   = "/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
        DOCKER = "/usr/local/bin/docker"
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

                stage('Load Environment Variables') {
            steps {
                withCredentials([string(credentialsId: 'DOTENV_FILE_CONTENT', variable: 'DOTENV_VARS')]) {
                    script {
                        echo "⚙️ Loading environment variables from Jenkins credential..."
                        DOTENV_VARS.readLines().each { line ->
                            if (line =~ /^(export )?([A-Za-z0-9_]+)=(.*)$/) {
                                env."${it[2]}" = it[3].trim()
                            }
                        }
                        // Optionally, echo some of the loaded variables for debugging
                        echo "DATABASE_URL: ${env.DATABASE_URL ?: 'Not set'}"
                        echo "API_KEY: ${env.API_KEY ?: 'Not set'}"
                    }
                }
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
