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
                sh 'cmd'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying the application...'
            }
        }
    }
}
