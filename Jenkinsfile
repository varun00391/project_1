pipeline {
  agent any
  stages {
    stage('Check docker') {
      steps {
        sh 'which docker'
        sh 'docker --version'
      }
    }
  }
}

