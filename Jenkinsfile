pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Building the project...'
                sh 'whoami'
            }
        }

        stage('Test') {
            steps {
                echo 'Running tests...'
                sh 'ls'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying the application...'
                sh 'pwd'
            }
        }
    }
}
