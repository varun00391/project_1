pipeline {
    agent any

    environment {
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
                        def envVars = [:]
                        DOTENV_VARS.readLines().each { line ->
                            def matcher = line =~ /^(?:export\s+)?([A-Za-z0-9_]+)=(.*)$/
                            if (matcher.matches()) {
                                def key = matcher[0][1]
                                def value = matcher[0][2].trim()
                                envVars[key] = value
                                env[key] = value
                            }
                        }

                        // Optionally, echo some of the loaded variables for debugging
                        echo "DATABASE_URL: ${env.DATABASE_URL ?: 'Not set'}"
                        echo "API_KEY: ${env.API_KEY ?: 'Not set'}"
                        // Store the environment variables as a string for Docker Compose
                        env.DOCKER_COMPOSE_ENV = envVars.collect { key, value -> "${key}=${value}" }.join('\n')
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
                script {
                    def tempEnvFile = sh(script: 'mktemp', returnStdout: true).trim()
                    writeFile file: tempEnvFile, text: env.DOCKER_COMPOSE_ENV

                    sh "${DOCKER} compose --env-file ${tempEnvFile} up -d --build"

                    // Clean up the temporary file
                    sh "rm -f ${tempEnvFile}"
                }
            }
        }

        stage('Verify FastAPI') {
            steps {
                echo '🔍 Verifying FastAPI is up...'
                script {
                    retry(5) {
                        sleep(time: 3, unit: 'SECONDS') // wait a bit before trying
                        sh 'curl -f http://summarization-api:8000/docs'

                    }
                }
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